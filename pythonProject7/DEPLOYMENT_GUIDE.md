# 🚀 Deployment Guide - Color Detector Pro

Complete guide for deploying Color Detector Pro to various platforms.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Production Deployment](#production-deployment)
   - [Docker](#docker-deployment)
   - [Render.com](#rendercom)
   - [Heroku](#heroku)
   - [AWS EC2](#aws-ec2)
   - [DigitalOcean](#digitalocean)
4. [Configuration](#configuration)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- Python 3.11 or higher
- pip package manager
- Git

### Optional
- Docker & Docker Compose
- PostgreSQL (for production)
- Nginx (as reverse proxy)
- SSL Certificate

---

## Local Development

### Quick Start (Windows)

```powershell
# Run the automated setup script
.\run.ps1
```

### Manual Setup

```bash
# 1. Clone repository
git clone <your-repo-url>
cd pythonProject7

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env - set SECRET_KEY!

# 5. Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# 6. Run application
python app.py
```

Access at: `http://localhost:10000`

---

## Production Deployment

### Docker Deployment

#### Using Docker Compose (Recommended)

```bash
# 1. Set environment variables
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# 2. Build and start
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Stop
docker-compose down
```

#### Manual Docker Build

```bash
# Build image
docker build -t color-detector:latest .

# Run container
docker run -d \
  --name color-detector \
  -p 80:10000 \
  -e SECRET_KEY=your-secret-key \
  -e FLASK_ENV=production \
  -v $(pwd)/data:/app/data \
  color-detector:latest

# Check logs
docker logs -f color-detector
```

---

### Render.com

Perfect for easy, free deployment with automatic HTTPS.

#### Steps

1. **Prepare Repository**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Create Web Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub repository

3. **Configure Service**
   ```yaml
   Name: color-detector-pro
   Region: Choose closest to users
   Branch: main
   Root Directory: (leave empty or pythonProject7)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
   ```

4. **Set Environment Variables**
   ```
   SECRET_KEY=<generate-secure-key>
   FLASK_ENV=production
   DATABASE_URL=<optional-postgres-url>
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete
   - Access your app at the provided URL

#### Render.yaml (Alternative)

Create `render.yaml` in repository root:

```yaml
services:
  - type: web
    name: color-detector-pro
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
```

---

### Heroku

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Deployment Steps

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create color-detector-pro

# 3. Add buildpack
heroku buildpacks:add heroku/python

# 4. Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set FLASK_ENV=production

# 5. Deploy
git push heroku main

# 6. Open app
heroku open

# 7. View logs
heroku logs --tail
```

#### Procfile
```
web: gunicorn app:app
```

---

### AWS EC2

#### Launch Instance

1. **Create EC2 Instance**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.micro (free tier) or t2.small
   - Security Group: Allow ports 22, 80, 443

2. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Setup Server**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3.11 python3-pip python3-venv nginx -y
   
   # Clone repository
   git clone <your-repo-url>
   cd pythonProject7
   
   # Setup virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   nano .env  # Edit configuration
   
   # Initialize database
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

4. **Setup Gunicorn Service**
   ```bash
   sudo nano /etc/systemd/system/color-detector.service
   ```
   
   ```ini
   [Unit]
   Description=Color Detector Pro
   After=network.target
   
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/pythonProject7
   Environment="PATH=/home/ubuntu/pythonProject7/venv/bin"
   ExecStart=/home/ubuntu/pythonProject7/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   sudo systemctl start color-detector
   sudo systemctl enable color-detector
   sudo systemctl status color-detector
   ```

5. **Setup Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/color-detector
   ```
   
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   
   ```bash
   sudo ln -s /etc/nginx/sites-available/color-detector /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

6. **Setup SSL (Optional but Recommended)**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

---

### DigitalOcean

#### Using App Platform (Easiest)

1. Go to DigitalOcean Dashboard
2. Click "Create" → "Apps"
3. Connect GitHub repository
4. Configure:
   - Type: Web Service
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn app:app`
5. Set environment variables
6. Deploy

#### Using Droplet (More Control)

Similar to AWS EC2 deployment above.

---

## Configuration

### Environment Variables

```bash
# Required
SECRET_KEY=<64-character-random-string>
FLASK_ENV=production

# Optional
DEBUG=False
PORT=10000
DATABASE_URL=postgresql://user:pass@host:5432/dbname
LOG_LEVEL=INFO
LOG_FILE=app.log
RATE_LIMIT_PER_MINUTE=60
MAX_CONTENT_LENGTH=16777216
CORS_ORIGINS=https://yourdomain.com
```

### Generate Secret Key

```python
import secrets
print(secrets.token_hex(32))
```

### Database Configuration

#### SQLite (Development)
```python
DATABASE_URL=sqlite:///color_detector.db
```

#### PostgreSQL (Production Recommended)
```python
DATABASE_URL=postgresql://username:password@hostname:5432/database
```

---

## Monitoring

### Health Check Endpoint
```bash
curl http://your-domain.com/health
```

### Application Logs
```bash
# Docker
docker logs -f container-name

# Systemd
sudo journalctl -u color-detector -f

# File
tail -f app.log
```

### Performance Monitoring

Check response time headers:
```bash
curl -I http://your-domain.com/api/info
# Look for X-Response-Time header
```

---

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
lsof -i :10000  # Linux/Mac
netstat -ano | findstr :10000  # Windows

# Kill process
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

#### Camera Not Working
- Check HTTPS (camera requires secure context)
- Verify browser permissions
- Test on different browser

#### Database Errors
```bash
# Reinitialize database
python -c "from app import app, db; app.app_context().push(); db.drop_all(); db.create_all()"
```

#### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Rate Limit Issues
```bash
# Increase limit in .env
RATE_LIMIT_PER_MINUTE=120
```

### Debug Mode

Enable only for troubleshooting:
```bash
DEBUG=True
FLASK_ENV=development
```

### Testing Deployment

```bash
# Run tests
python -m pytest tests/

# Test API
curl -X POST http://localhost:10000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"hex": "#ff0000"}'
```

---

## Performance Optimization

### Production Settings

```python
# Use PostgreSQL instead of SQLite
# Enable caching (Redis)
# Use CDN for static files
# Enable gzip compression
# Configure worker processes based on CPU cores
```

### Gunicorn Configuration

```bash
gunicorn \
  --workers 4 \
  --threads 2 \
  --worker-class gthread \
  --timeout 120 \
  --bind 0.0.0.0:10000 \
  --access-logfile - \
  --error-logfile - \
  app:app
```

---

## Backup & Recovery

### Database Backup
```bash
# SQLite
cp color_detector.db color_detector_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump dbname > backup_$(date +%Y%m%d).sql
```

### Restore
```bash
# SQLite
cp backup.db color_detector.db

# PostgreSQL
psql dbname < backup.sql
```

---

## Security Checklist

- [ ] Strong SECRET_KEY set
- [ ] DEBUG mode disabled
- [ ] HTTPS enabled
- [ ] Firewall configured
- [ ] Rate limiting enabled
- [ ] Database credentials secured
- [ ] Regular updates scheduled
- [ ] Backups automated
- [ ] Monitoring enabled
- [ ] Logs reviewed regularly

---

## Support

For deployment issues:
- Check logs first
- Review this guide
- Open GitHub issue
- Email: [your-support-email]

---

## Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

Last Updated: 2024-01-01
