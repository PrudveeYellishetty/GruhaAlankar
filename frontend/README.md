# GruhaAlankar Frontend

React-based web frontend for AI-powered AR interior design platform.

## Features

- 🪑 **Furniture Browsing** - Explore curated 3D furniture collection
- 🤖 **AI Recommendations** - Get intelligent furniture suggestions based on room photos
- 🎨 **AI Redesign** - Generate redesigned room concepts with AI
- 📱 **WebXR AR** - View furniture in real space using augmented reality
- ⚡ **Performance Optimized** - Code splitting, lazy loading, efficient rendering

## Tech Stack

- **React 18** - UI framework
- **React Router** - Navigation
- **Three.js** - 3D rendering
- **WebXR** - AR capabilities
- **Vite** - Build tool
- **Axios** - HTTP client

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

5. **Preview production build:**
   ```bash
   npm run preview
   ```

## Development

### Project Structure

```
src/
├── components/       # Reusable components
│   ├── Layout/      # Layout components (Header, Footer)
│   └── AR/          # AR-specific components
├── pages/           # Page components (routes)
├── services/        # API service layer
├── config/          # Configuration files
├── App.jsx          # Main app component
├── main.jsx         # Entry point
└── index.css        # Global styles
```

### Key Components

- **ARScene** - Three.js + WebXR AR rendering engine
- **FurnitureList** - Filterable furniture grid
- **UploadRoom** - AI analysis interface
- **AISuggestions** - Display AI recommendations

### AR Requirements

WebXR AR requires:
- **HTTPS** - Secure connection
- **Android device** with ARCore
- **Chrome browser** (latest)
- **Camera permissions**

For local HTTPS development:
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes

# Update vite.config.js
server: {
  https: {
    key: fs.readFileSync('key.pem'),
    cert: fs.readFileSync('cert.pem')
  }
}
```

## API Integration

All API calls go through the service layer in `src/services/api.js`:

```javascript
import { furnitureAPI, aiAPI } from './services/api';

// Get furniture
const furniture = await furnitureAPI.getAll({ category: 'living' });

// AI analysis
const result = await aiAPI.analyzeRoom(imageFile);
```

## Performance Optimizations

- **Code Splitting** - Vendor chunks separated
- **Lazy Loading** - Components loaded on demand
- **Asset Optimization** - Images lazy loaded
- **Memory Management** - Three.js cleanup on unmount
- **Bundle Size** - React and Three.js in separate chunks

## Browser Support

- ✅ Chrome (Android) - Full AR support
- ✅ Chrome (Desktop) - Browsing only
- ✅ Firefox - Browsing only
- ✅ Safari - Browsing only
- ⚠️ AR requires WebXR-capable devices

## Deployment

### Static Hosting (Netlify, Vercel, etc.)

```bash
npm run build
# Deploy dist/ folder
```

### Environment Variables

Set in deployment:
- `VITE_API_URL` - Backend API URL

## Troubleshooting

### AR Not Working

1. Check HTTPS connection
2. Verify device ARCore support
3. Enable camera permissions
4. Use Chrome browser
5. Check WebXR API availability

### Model Loading Issues

1. Verify model URL accessibility
2. Check CORS headers on storage
3. Ensure GLB format (not GLTF)
4. Verify model size (< 8MB recommended)

## Development Tips

- Use browser DevTools for debugging
- Test AR on real Android device
- Monitor network tab for API calls
- Check console for Three.js warnings
- Use React DevTools for component hierarchy

## Contributing

1. Follow existing code structure
2. Keep components modular
3. Add error handling
4. Clean up Three.js resources
5. Test on mobile devices

## License

Proprietary - GruhaAlankar 2026
