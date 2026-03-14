# Coolify Deployment Guide

This guide will help you deploy the intern-crud application on your VPS using Coolify.

## Prerequisites

- A VPS with Coolify installed
- Git repository access (GitHub)
- Domain name (optional, but recommended)

## Step 1: Prepare Your Repository

The repository is already configured with:
- ✅ `Dockerfile` - Container configuration
- ✅ `docker-compose.yml` - Service orchestration
- ✅ `.dockerignore` - Build optimization
- ✅ `requirements.txt` - Production dependencies

## Step 2: Coolify Setup

### 2.1 Create a New Project in Coolify

1. Log in to your Coolify dashboard
2. Click **"+ New"** → **"Project"**
3. Give it a name (e.g., "intern-crud")

### 2.2 Add a New Resource

1. Inside your project, click **"+ New Resource"**
2. Select **"Public Repository"**
3. Enter your repository URL: `https://github.com/pbrudny/intern-crud.git`
4. Select branch: `main`
5. Click **"Continue"**

### 2.3 Configure Build Settings

Coolify will auto-detect the Dockerfile. Configure:

- **Build Pack**: Docker
- **Dockerfile Location**: `./Dockerfile`
- **Port**: `8000`
- **Health Check Path**: `/`

### 2.4 Set Environment Variables

In Coolify, add these environment variables:

```bash
# Required - Generate a strong secret key
SECRET_KEY=your-super-secret-key-here-change-this

# Database (SQLite by default, stored in volume)
DATABASE_URL=sqlite:///instance/intern_crud.db

# Flask Environment
FLASK_ENV=production

# Upload Configuration
UPLOAD_FOLDER=/app/uploads/resumes
MAX_CONTENT_LENGTH=2097152
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2.5 Configure Persistent Storage

Add these volumes in Coolify:

1. **Database Volume**:
   - Source: `intern-crud-db`
   - Destination: `/app/backend/instance`

2. **Uploads Volume**:
   - Source: `intern-crud-uploads`
   - Destination: `/app/uploads`

### 2.6 Configure Domain (Optional)

1. In the resource settings, go to **"Domains"**
2. Add your domain (e.g., `intern-crud.yourdomain.com`)
3. Enable **"Generate Let's Encrypt Certificate"** for HTTPS

## Step 3: Deploy

1. Click **"Deploy"** in Coolify
2. Monitor the build logs
3. Wait for the deployment to complete (usually 2-5 minutes)

## Step 4: Post-Deployment

### 4.1 Verify Deployment

Visit your application URL. You should see the login/register page.

### 4.2 Create First Admin User

1. Click **"Register"**
2. Create your account (first user becomes admin automatically)
3. Complete your profile

### 4.3 Monitor Logs

In Coolify, you can view:
- **Build Logs**: Check for build errors
- **Application Logs**: Monitor runtime issues
- **Metrics**: CPU, Memory, Network usage

## Troubleshooting

### Build Fails

**Check build logs in Coolify**:
- Ensure all dependencies are in `requirements.txt`
- Verify Dockerfile syntax
- Check Python version compatibility

### Application Won't Start

**Common issues**:
1. **Missing SECRET_KEY**: Ensure it's set in environment variables
2. **Port conflicts**: Verify port 8000 is exposed
3. **Database errors**: Check volume permissions

**View logs**:
```bash
# In Coolify, go to Logs → Application Logs
```

### Database Not Persisting

**Verify volumes are mounted**:
- Check Coolify volume configuration
- Ensure `/app/backend/instance` is mounted
- Restart the application

### File Uploads Failing

**Check upload volume**:
- Verify `/app/uploads` volume is mounted
- Check directory permissions
- Ensure `MAX_CONTENT_LENGTH` is set correctly

## Updating the Application

### Method 1: Auto-Deploy (Recommended)

1. In Coolify, enable **"Auto Deploy"** for the main branch
2. Push changes to GitHub
3. Coolify will automatically rebuild and deploy

### Method 2: Manual Deploy

1. Push changes to GitHub
2. Go to Coolify dashboard
3. Click **"Redeploy"**

## Environment-Specific Configuration

### Production Optimizations

The application is configured for production with:
- ✅ Gunicorn WSGI server (4 workers)
- ✅ Health checks enabled
- ✅ Logging to stdout/stderr
- ✅ Non-root user for security
- ✅ Persistent volumes for data

### Scaling

To handle more traffic, adjust in Dockerfile:
```dockerfile
# Change --workers value (current: 4)
gunicorn --bind 0.0.0.0:8000 --workers 8 ...
```

Then redeploy in Coolify.

## Security Checklist

- [ ] Strong `SECRET_KEY` set (not the default)
- [ ] HTTPS enabled (Let's Encrypt certificate)
- [ ] Database volume is persistent
- [ ] Upload directory has proper permissions
- [ ] Environment variables are not committed to Git
- [ ] Regular backups configured (Coolify backup feature)

## Backup Strategy

### Database Backup

In Coolify:
1. Go to **"Backups"**
2. Enable **"Scheduled Backups"**
3. Set frequency (e.g., daily)
4. Configure backup destination (S3, local, etc.)

### Manual Backup

```bash
# SSH into your VPS
docker cp <container-id>:/app/backend/instance/intern_crud.db ./backup-$(date +%Y%m%d).db
```

## Support

For issues:
1. Check Coolify logs
2. Review application logs
3. Verify environment variables
4. Check volume mounts

## Next Steps

After successful deployment:
1. Test all CRUD operations
2. Upload a test resume
3. Create multiple user accounts
4. Monitor performance metrics
5. Set up automated backups

