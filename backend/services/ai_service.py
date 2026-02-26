"""AI service for Vision and Generative AI operations."""
import os
import json
import logging
from typing import Dict, List, Optional
import requests
from PIL import Image

logger = logging.getLogger(__name__)


class AIService:
    """Handles AI API integrations for room analysis and redesign."""
    
    def __init__(self, api_key: str, provider: str = 'openai'):
        """
        Initialize AI Service.
        
        Args:
            api_key: API key for the AI provider
            provider: 'openai' or 'google' (default: openai)
        """
        self.api_key = api_key
        self.provider = provider
        self.openai_base_url = "https://api.openai.com/v1"
    
    def analyze_room(self, image_path: str) -> Dict:
        """
        Analyze room image using Vision AI.
        
        Returns structured JSON with:
        - room_type: detected room type
        - style: detected interior style
        - empty_spaces: locations suitable for furniture
        - recommendations: suggested furniture with categories
        
        Args:
            image_path: Path to the uploaded room image
        
        Returns:
            Structured analysis result
        """
        try:
            if self.provider == 'openai':
                return self._analyze_room_openai(image_path)
            else:
                raise NotImplementedError(f"Provider {self.provider} not implemented")
        
        except Exception as e:
            logger.error(f"Error analyzing room: {e}")
            raise
    
    def _analyze_room_openai(self, image_path: str) -> Dict:
        """Analyze room using OpenAI Vision API."""
        import base64
        
        # Read and encode image
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Structured prompt for consistent JSON output
        prompt = """Analyze this interior room image and provide a structured assessment.

Return ONLY valid JSON with this exact structure:
{
  "room_type": "living_room|bedroom|kitchen|dining|office",
  "style": "modern|minimal|traditional|industrial|scandinavian",
  "empty_spaces": [
    {
      "location": "description of empty area",
      "suitable_for": ["sofa", "table", "chair"]
    }
  ],
  "recommendations": [
    {
      "furniture_type": "sofa|table|chair|bed|cabinet|lamp",
      "category": "living|bedroom|dining|office",
      "reason": "why this furniture fits",
      "preferred_style": "minimal|modern|traditional"
    }
  ],
  "color_scheme": ["#hexcolor1", "#hexcolor2"],
  "confidence": 0.85
}

Focus on:
1. Accurately identify room type and existing style
2. Find 1-3 empty spaces that could accommodate furniture
3. Suggest 2-4 furniture pieces that would complement the space
4. Extract dominant color palette

Return ONLY the JSON, no additional text."""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000
        }
        
        response = requests.post(
            f"{self.openai_base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract and parse JSON from response
        content = result['choices'][0]['message']['content']
        
        # Clean up response if it contains markdown code blocks
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()
        
        analysis = json.loads(content)
        logger.info(f"Room analysis completed: {analysis.get('room_type')}")
        
        return analysis
    
    def redesign_room(self, image_path: str, preferences: Dict) -> Dict:
        """
        Generate redesigned room images using Generative AI.
        
        Args:
            image_path: Path to original room image
            preferences: User preferences (style, color_scheme, furniture_focus)
        
        Returns:
            Dictionary with generated images and mapped furniture
        """
        try:
            if self.provider == 'openai':
                return self._redesign_room_openai(image_path, preferences)
            else:
                raise NotImplementedError(f"Provider {self.provider} not implemented")
        
        except Exception as e:
            logger.error(f"Error redesigning room: {e}")
            raise
    
    def _redesign_room_openai(self, image_path: str, preferences: Dict) -> Dict:
        """Generate redesign using DALL-E."""
        
        style = preferences.get('style', 'modern')
        color_scheme = preferences.get('color_scheme', 'neutral')
        focus = preferences.get('furniture_focus', 'overall ambiance')
        
        # Construct detailed prompt
        prompt = f"""Interior design: Transform this room into a {style} style interior with {color_scheme} color palette. 
Focus on {focus}. 
Create a cohesive, well-lit space with harmonious furniture placement. 
Keep the room layout recognizable but enhance with tasteful {style} furniture and decor. 
Photorealistic quality, professional interior photography."""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Note: DALL-E 3 doesn't support image variations yet
        # Using text-to-image as workaround for MVP
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "quality": "standard"
        }
        
        response = requests.post(
            f"{self.openai_base_url}/images/generations",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        generated_images = [img['url'] for img in result['data']]
        
        logger.info(f"Generated {len(generated_images)} redesign images")
        
        return {
            "generated_images": generated_images,
            "style": style,
            "prompt_used": prompt,
            "furniture_suggestions": []  # Can be enhanced with second AI call
        }
    
    def map_recommendations_to_assets(self, recommendations: List[Dict], 
                                     available_furniture: List[Dict]) -> List[Dict]:
        """
        Map AI recommendations to actual furniture asset IDs.
        
        Args:
            recommendations: List of AI-suggested furniture
            available_furniture: List of available furniture from Firestore
        
        Returns:
            List of matched assets with IDs and suggested colors
        """
        matched_assets = []
        
        for rec in recommendations:
            furniture_type = rec.get('furniture_type', '').lower()
            category = rec.get('category', '').lower()
            style = rec.get('preferred_style', '').lower()
            
            # Find matching furniture in database
            for item in available_furniture:
                item_name = item.get('name', '').lower()
                item_category = item.get('category', '').lower()
                item_style = item.get('style', '').lower()
                
                # Simple matching logic - can be enhanced with fuzzy matching
                type_match = furniture_type in item_name or furniture_type in item.get('tags', [])
                category_match = category == item_category
                style_match = style == item_style or not style
                
                if type_match and category_match:
                    # Pick a color from available colors
                    available_colors = item.get('available_colors', ['#808080'])
                    suggested_color = available_colors[0]
                    
                    matched_assets.append({
                        'asset_id': item['id'],
                        'color': suggested_color,
                        'reason': rec.get('reason', ''),
                        'confidence': 0.8 if style_match else 0.6
                    })
                    break  # Found a match, move to next recommendation
        
        logger.info(f"Mapped {len(matched_assets)} recommendations to assets")
        return matched_assets
