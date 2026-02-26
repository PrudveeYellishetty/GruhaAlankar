# Production Deployment Guide

## Prerequisites

- Domain name with SSL certificate
- Cloud hosting account (GCP, AWS, or Heroku)
- Supabase project configured
- OpenAI API key

## Option 1: Deploy with Docker

### 1. Build Images

```bash
# Backend
cd backend
docker build -t gruhaalankar-backend .

# Frontend
cd frontend
docker build -t gruhaalankar-frontend .
```

### 2. Run with Docker Compose

```bash
# Configure environment
cp .env.example .env
# Edit .env with production values

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### 3. Access Application

- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## Option 2: Deploy to Google Cloud

### Backend (Cloud Run)

```bash
cd backend

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy gruhaalankar-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SUPABASE_URL=YOUR_SUPABASE_URL \
  --set-secrets OPENAI_API_KEY=openai-key:latest,SUPABASE_SERVICE_ROLE_KEY=supabase-key:latest

# Get URL
gcloud run services describe gruhaalankar-api --format='value(status.url)'
```

### Frontend (Vercel/Netlify)

```bash
cd frontend

# Build
npm run build

# Deploy to Vercel
vercel --prod

# Or deploy to Netlify
netlify deploy --prod --dir=dist
```

## Option 3: Deploy to Heroku

### Backend

```bash
cd backend

# Create app
heroku create gruhaalankar-api

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key
heroku config:set SUPABASE_URL=your_supabase_url
heroku config:set SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

### Frontend (Vercel)

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Set environment variable
vercel env add VITE_API_URL production
```

## Option 4: Traditional VPS (Ubuntu)

### Backend Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Clone repository
git clone YOUR_REPO
cd GruhaAlankar/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env

# Install supervisor for process management
sudo apt install supervisor -y

# Create supervisor config
sudo nano /etc/supervisor/conf.d/gruhaalankar.conf
```

Supervisor config:
```ini
[program:gruhaalankar]
directory=/path/to/GruhaAlankar/backend
command=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/gruhaalankar.err.log
stdout_logfile=/var/log/gruhaalankar.out.log
```

```bash
# Start service
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start gruhaalankar
```

### Frontend Setup (Nginx)

```bash
cd frontend

# Build
npm run build

# Copy to web root
sudo cp -r dist/* /var/www/html/

# Configure Nginx
sudo nano /etc/nginx/sites-available/gruhaalankar
```

Nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/gruhaalankar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## SSL/HTTPS Setup (Required for AR)

### Using Let's Encrypt (Free)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Using Cloudflare (Easy)

1. Add your domain to Cloudflare
2. Update nameservers
3. Enable "Always Use HTTPS"
4. Enable "Automatic HTTPS Rewrites"

## Environment Variables Checklist

### Backend (.env)
- [ ] SUPABASE_URL
- [ ] SUPABASE_SERVICE_ROLE_KEY
- [ ] OPENAI_API_KEY
- [ ] SECRET_KEY (generate new for production)
- [ ] FLASK_ENV=production
- [ ] ALLOWED_ORIGINS (production URLs)

### Frontend (.env)
- [ ] VITE_API_URL (production API URL with HTTPS)

## Post-Deployment

### 1. Test Backend API

```bash
curl https://your-api-domain.com/api/health
```

### 2. Test Frontend

- Visit your domain
- Check browser console for errors
- Test furniture browsing
- Test AR on Android device with HTTPS

### 3. Monitor Logs

```bash
# Docker
docker-compose logs -f

# Supervisor
sudo tail -f /var/log/gruhaalankar.out.log

# Nginx
sudo tail -f /var/log/nginx/access.log
```

### 4. Setup Monitoring

- Supabase Dashboard for PostgreSQL metrics
- Cloud provider monitoring dashboards
- Set up error alerts
- Monitor API usage and costs

## Scaling Considerations

### Backend
- Use load balancer for multiple instances
- Configure auto-scaling based on CPU/memory
- Enable CDN for static assets
- Implement Redis for caching

### Frontend
- Enable CDN (Cloudflare, Cloudfront)
- Optimize images (WebP, lazy loading)
- Enable HTTP/2
- Minimize bundle size

### Database
- Indexes already defined in supabase_schema.sql
- Monitor read/write operations
- Set up backup strategy
- Consider connection pooling

## Troubleshooting

### AR Not Working in Production
- ✅ Verify HTTPS is enabled
- ✅ Check SSL certificate validity
- ✅ Test on real Android device
- ✅ Check CORS headers

### API Errors
- Check logs for stack traces
- Verify environment variables
- Test Supabase connection
- Validate API keys

### Frontend Build Errors
- Clear node_modules and reinstall
- Check for environment variable issues
- Verify API URL is correct
- Test build locally first

## Rollback Strategy

```bash
# Docker
docker-compose down
docker-compose up -d --force-recreate

# Git-based
git checkout previous-version
git push heroku main --force

# Keep previous version tagged
git tag v1.0.0
```

## Security Checklist

- [ ] All API keys in environment variables
- [ ] HTTPS enabled everywhere
- [ ] CORS properly configured
- [ ] Supabase RLS policies configured
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (using ORMs)
- [ ] XSS protection enabled
- [ ] Regular dependency updates

## Cost Optimization

- Use Supabase free tier limits wisely
- Implement caching to reduce AI API calls
- Optimize image sizes before upload
- Use serverless for backend (auto-scaling)
- Monitor and set budget alerts

---

**Need Help?** Check troubleshooting section in main README.md
