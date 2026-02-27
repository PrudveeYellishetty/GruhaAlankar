"""Room analysis service using Google Gemini Vision API."""
import os
import logging
from typing import Dict, List, Optional
try:
    import google.genai as genai
except ImportError:
    # Fallback to old package for backward compatibility
    import google.generativeai as genai
from PIL import Image
import io
import base64

logger = logging.getLogger(__name__)

# Configure Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


class RoomAnalysisService:
    """Service for analyzing room images and matching furniture"""

    @staticmethod
    def analyze_room_image(image_data: bytes) -> Dict:
        """
        Analyze a room image and return detailed analysis.
        
        Args:
            image_data: Raw bytes of the image
            
        Returns:
            Dict with room analysis including:
            - room_type: Detected room type (living, bedroom, dining, office)
            - style: Detected style (modern, minimal, traditional, etc.)
            - colors: Dominant colors in the room
            - space_analysis: Assessment of available space
            - lighting: Lighting conditions
            - suggestions: General suggestions
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Use Gemini Flash Latest (supports text and images)
            model = genai.GenerativeModel('models/gemini-flash-latest')
            
            prompt = """Analyze this room image and provide a detailed analysis in the following JSON format:
{
    "room_type": "living/bedroom/dining/office",
    "style": "modern/minimal/traditional/scandinavian/industrial",
    "colors": ["color1", "color2", "color3"],
    "space_size": "small/medium/large",
    "lighting": "bright/natural/dim/artificial",
    "existing_furniture": ["item1", "item2"],
    "color_scheme": "warm/cool/neutral",
    "suggestions": "Brief suggestions for furniture placement"
}

Be specific and accurate. Focus on identifying:
1. The primary function of the room
2. The current design style
3. Available space for new furniture
4. Color palette
5. Existing furniture items"""

            response = model.generate_content([prompt, image])
            
            # Parse the response
            analysis_text = response.text.strip()
            
            # Try to extract JSON from the response
            import json
            import re
            
            # Find JSON in response
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                # Fallback to a structured parse
                analysis = {
                    "room_type": "living",
                    "style": "modern",
                    "colors": ["neutral"],
                    "space_size": "medium",
                    "lighting": "natural",
                    "existing_furniture": [],
                    "color_scheme": "neutral",
                    "suggestions": analysis_text[:200]
                }
            
            logger.info(f"Room analysis complete: {analysis['room_type']} - {analysis['style']}")
            return analysis
            
        except Exception as e:
            logger.error(f"Room analysis failed: {e}")
            raise Exception(f"Failed to analyze room image: {str(e)}")

    @staticmethod
    def match_furniture(room_analysis: Dict, furniture_catalog: List[Dict]) -> List[Dict]:
        """
        Match furniture from catalog based on room analysis.
        
        Args:
            room_analysis: Analysis from analyze_room_image()
            furniture_catalog: List of available furniture items
            
        Returns:
            List of recommended furniture with reasons
        """
        try:
            recommendations = []
            
            # Filter by room type
            room_type = room_analysis.get('room_type', 'living').lower()
            style_preference = room_analysis.get('style', 'modern').lower()
            space_size = room_analysis.get('space_size', 'medium').lower()
            
            # Category mapping
            category_map = {
                'living': ['living', 'lounge'],
                'bedroom': ['bedroom', 'bed'],
                'dining': ['dining', 'kitchen'],
                'office': ['office', 'study', 'desk']
            }
            
            valid_categories = category_map.get(room_type, ['living'])
            
            for item in furniture_catalog:
                score = 0
                reasons = []
                
                # Match category (highest priority)
                if any(cat in item.get('category', '').lower() for cat in valid_categories):
                    score += 50
                    reasons.append(f"Perfect for your {room_type} room")
                
                # Match style
                if style_preference in item.get('style', '').lower():
                    score += 30
                    reasons.append(f"Matches your {style_preference} style")
                
                # Size considerations
                if space_size == 'small':
                    dims = item.get('dimensions', {})
                    width = dims.get('width', 2)
                    depth = dims.get('depth', 2)
                    if width < 1.5 and depth < 1.5:
                        score += 20
                        reasons.append("Compact size fits small spaces")
                elif space_size == 'large':
                    dims = item.get('dimensions', {})
                    width = dims.get('width', 1)
                    depth = dims.get('depth', 1)
                    if width > 2 or depth > 2:
                        score += 20
                        reasons.append("Statement piece for larger rooms")
                else:
                    score += 10
                    reasons.append("Versatile size for medium spaces")
                
                # Add to recommendations if score is good
                if score >= 50:
                    recommendations.append({
                        **item,
                        'recommendation_score': score,
                        'reasons': reasons
                    })
            
            # Sort by score and return top 8
            recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
            return recommendations[:8]
            
        except Exception as e:
            logger.error(f"Furniture matching failed: {e}")
            return []

    @staticmethod
    def generate_detailed_recommendations(room_analysis: Dict, matched_furniture: List[Dict]) -> Dict:
        """
        Generate detailed AI-powered recommendations.
        
        Args:
            room_analysis: Room analysis data
            matched_furniture: Matched furniture items
            
        Returns:
            Dict with detailed recommendations
        """
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            furniture_list = "\n".join([
                f"- {item['name']} ({item['category']}, {item['style']})"
                for item in matched_furniture[:5]
            ])
            
            prompt = f"""Based on this room analysis:
Room Type: {room_analysis.get('room_type')}
Style: {room_analysis.get('style')}
Space Size: {room_analysis.get('space_size')}
Colors: {', '.join(room_analysis.get('colors', []))}

And these furniture options:
{furniture_list}

Provide 3-4 specific, actionable tips for arranging furniture in this room. Each tip should be 1-2 sentences. Focus on:
1. Space utilization
2. Flow and movement
3. Focal points
4. Color coordination

Keep it practical and friendly."""

            response = model.generate_content(prompt)
            tips = response.text.strip().split('\n')
            tips = [tip.strip('- ').strip() for tip in tips if tip.strip()]
            
            return {
                'summary': f"We found {len(matched_furniture)} pieces perfect for your {room_analysis.get('style')} {room_analysis.get('room_type')} room",
                'tips': tips[:4],
                'room_analysis': room_analysis
            }
            
        except Exception as e:
            logger.error(f"Detailed recommendations failed: {e}")
            return {
                'summary': f"We found {len(matched_furniture)} matching furniture pieces for your room",
                'tips': [
                    "Consider the natural flow of movement in your space",
                    "Group furniture to create conversation areas",
                    "Leave adequate space for walking between pieces",
                    "Balance larger pieces with smaller accent furniture"
                ],
                'room_analysis': room_analysis
            }
