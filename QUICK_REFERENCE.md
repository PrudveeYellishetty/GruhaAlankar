# GruhaAlankar - Quick Reference

## 🚀 Quick Start Commands

```bash
# Clone and setup
git clone <repo>
cd GruhaAlankar
./setup.sh

# Backend
cd backend
source venv/bin/activate  # Linux/Mac
python app.py

# Frontend
cd frontend
npm install
npm run dev

# Docker (All-in-one)
docker-compose up -d
```

## 📡 API Quick Reference

```bash
# Health check
curl http://localhost:5000/api/health

# List furniture
curl http://localhost:5000/api/furniture

# Get furniture by ID
curl http://localhost:5000/api/furniture/sofa_001

# Analyze room (with image upload)
curl -X POST -F "image=@room.jpg" http://localhost:5000/api/analyze-room

# Redesign room
curl -X POST \
  -F "image=@room.jpg" \
  -F "style=modern" \
  -F "color_scheme=neutral" \
  http://localhost:5000/api/redesign
```

## 🗂️ Project Structure Summary

```
GruhaAlankar/
├── backend/              # Flask REST API
│   ├── app.py           # Main entry point
│   ├── config/          # Configuration
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   └── seed_furniture.py
│
├── frontend/            # React Web App
│   ├── src/
│   │   ├── components/  # Reusable components
│   │   ├── pages/       # Route pages
│   │   ├── services/    # API client
│   │   └── App.jsx
│   └── package.json
│
├── docker-compose.yml   # Docker setup
├── setup.sh            # Quick setup script
└── README.md           # Main documentation
```

## 🔑 Essential Files to Configure

1. **backend/.env** - API keys and Supabase config
2. **frontend/.env** - API URL

## 📱 Pages & Routes

| Route | Component | Purpose |
|-------|-----------|---------|
| `/` | Home | Landing page |
| `/furniture` | FurnitureList | Browse all furniture |
| `/furniture/:id` | FurnitureDetail | Furniture details |
| `/upload` | UploadRoom | AI analysis/redesign |
| `/suggestions` | AISuggestions | AI results |
| `/ar/:id` | ARViewer | AR experience |

## 🎯 Key Features Implementation

### Manual AR Workflow
1. Browse furniture → 2. Select item → 3. Click "View in AR" → 4. Place in space

### AI Recommendation Workflow
1. Upload room photo → 2. AI analyzes → 3. View suggestions → 4. View in AR

### AI Redesign Workflow
1. Upload photo → 2. Select preferences → 3. Generate → 4. View concepts

## 🛠️ Development Tips

### Backend Development
```bash
# Install new package
pip install package-name
pip freeze > requirements.txt

# Test endpoints
python -m pytest  # (add tests)

# Format code
black .
```

### Frontend Development
```bash
# Install package
npm install package-name

# Production build
npm run build

# Preview build
npm run preview

# Lint
npm run lint
```

### Database Management
```bash
# Seed furniture data
cd backend
python seed_furniture.py

# Access database
# Use Supabase Dashboard
```

## 🐛 Common Issues & Fixes

### Backend won't start
- Check Python version (3.8+)
- Verify virtual environment activated
- Check Supabase credentials in .env
- Review .env configuration

### Frontend build fails
- Delete node_modules, reinstall
- Check .env file exists
- Verify Node.js version (18+)
- Clear npm cache: `npm cache clean --force`

### AR not working
- **Must use HTTPS**
- Test on real Android device (not emulator)
- Check WebXR support: `chrome://webxr-internals`
- Enable camera permissions

### API CORS errors
- Check ALLOWED_ORIGINS in backend/.env
- Verify frontend URL matches
- Restart backend after changes

### Model loading fails
- Check Supabase Storage bucket permissions
- Verify GLB file format
- Check file size (< 8MB)
- Test direct URL access

## 📊 Performance Monitoring

### Backend
```python
# Add timing logs
import time
start = time.time()
# ... code ...
print(f"Took {time.time() - start}s")
```

### Frontend
```javascript
// Check bundle size
npm run build
# Check dist/ folder size

// React DevTools Profiler
// Enable in browser
```

## 🔒 Security Checklist

- [ ] API keys in environment variables only
- [ ] Supabase service role key secured
- [ ] CORS properly configured
- [ ] Input validation on all endpoints
- [ ] HTTPS in production
- [ ] File upload size limits enforced
- [ ] Error messages don't leak sensitive info

## 📈 Optimization Checklist

### Backend
- [ ] Use gunicorn with multiple workers
- [ ] Implement caching (Redis)
- [ ] Optimize Firestore queries
- [ ] Add request rate limiting
- [ ] Monitor AI API costs

### Frontend
- [ ] Lazy load routes
- [ ] Optimize images (WebP)
- [ ] Enable gzip compression
- [ ] Use CDN for static assets
- [ ] Minimize bundle size

### Database
- [ ] Create Firestore indexes
- [ ] Optimize query patterns
- [ ] Use proper data structure
- [ ] Monitor read/write operations

## 🚀 Deployment Quick Links

- **Backend**: [DEPLOYMENT.md](DEPLOYMENT.md#backend-deployment)
- **Frontend**: [DEPLOYMENT.md](DEPLOYMENT.md#frontend-deployment)
- **Docker**: `docker-compose up -d`
- **Heroku**: `git push heroku main`
- **Vercel**: `vercel --prod`

## 📚 Documentation Links

- [Main README](README.md) - Full documentation
- [Backend README](backend/README.md) - API details
- [Frontend README](frontend/README.md) - UI documentation
- [Deployment Guide](DEPLOYMENT.md) - Production setup

## 🆘 Getting Help

1. Check error logs (console, server)
2. Review troubleshooting sections
3. Verify environment configuration
4. Test components independently
5. Check browser DevTools

## 💡 Best Practices

1. **Always use version control**
2. **Never commit credentials**
3. **Test on real devices**
4. **Keep dependencies updated**
5. **Monitor costs and usage**
6. **Document complex logic**
7. **Handle errors gracefully**
8. **Optimize for performance**

---

**Version**: 1.0.0 MVP  
**Last Updated**: February 2026  
**Tech Stack**: Flask, React, Three.js, WebXR, Firebase
