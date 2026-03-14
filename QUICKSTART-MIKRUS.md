# Quick Start - Deploy to Mikrus VPS with Cloudflare Tunnel

This is a simplified guide for deploying intern-crud to your Mikrus VPS using your existing Cloudflare Tunnel.

## Prerequisites

- ✅ Mikrus VPS with SSH access
- ✅ Cloudflare Tunnel already configured
- ✅ Domain managed by Cloudflare

## Your Current Setup

Based on your config, you have:
- **Tunnel ID**: `307dcf72-cd57-47b5-b763-e60abf641dcc`
- **Credentials**: `/root/.cloudflared/307dcf72-cd57-47b5-b763-e60abf641dcc.json`
- **Existing services**:
  - `dashboard.codewithpeter.com` → `localhost:8000`
  - `intern-crud.codewithpeter.com` → `localhost:5000`

## Deployment Steps

### 1. Connect to Your Mikrus VPS

```bash
ssh root@steve107.mikrus.xyz -p10107
```

### 2. Run Automated Deployment

```bash
# Download and run deployment script
curl -sSL https://raw.githubusercontent.com/pbrudny/intern-crud/main/deploy-mikrus.sh -o /tmp/deploy-mikrus.sh
chmod +x /tmp/deploy-mikrus.sh
/tmp/deploy-mikrus.sh
```

This script will:
- ✅ Install all dependencies (Python, Nginx, etc.)
- ✅ Clone the repository to `/opt/intern-crud`
- ✅ Setup Python virtual environment
- ✅ Generate secure SECRET_KEY
- ✅ Initialize database
- ✅ Create systemd service
- ✅ Configure Nginx
- ✅ Start the application on `localhost:5000` (matches your existing tunnel config!)

### 3. Verify Deployment

```bash
# Check if app is running
systemctl status intern-crud

# Check if it responds locally
curl http://localhost:5000

# Check cloudflared status
systemctl status cloudflared
```

### 5. Access Your Application

Visit: **https://intern-crud.codewithpeter.com**

You should see the login/register page!

## Post-Deployment

### Create First Admin User

1. Go to https://intern-crud.codewithpeter.com
2. Click "Register"
3. Create your account (first user becomes admin automatically)
4. Complete your profile

### Monitor Application

```bash
# View application logs
tail -f /var/log/intern-crud-error.log

# View access logs
tail -f /var/log/intern-crud-access.log

# View cloudflared logs
journalctl -u cloudflared -f

# Check service status
systemctl status intern-crud
```

### Update Application

```bash
cd /opt/intern-crud
git pull origin main
source .venv/bin/activate
uv pip install -e .
cd backend
python3 -m flask db upgrade
systemctl restart intern-crud
```

## Adding More Services to Cloudflare Tunnel

If you want to add more applications to your tunnel:

```bash
# Use the helper script
curl -sSL https://raw.githubusercontent.com/pbrudny/intern-crud/main/cloudflare-tunnel-add-service.sh -o /tmp/add-service.sh
chmod +x /tmp/add-service.sh
/tmp/add-service.sh
```

Or manually edit `/root/.cloudflared/config.yml`:

```yaml
tunnel: 307dcf72-cd57-47b5-b763-e60abf641dcc
credentials-file: /root/.cloudflared/307dcf72-cd57-47b5-b763-e60abf641dcc.json

ingress:
  - hostname: dashboard.codewithpeter.com
    service: http://localhost:8000

  - hostname: intern-crud.codewithpeter.com
    service: http://localhost:8000  # Updated!

  - hostname: another-app.codewithpeter.com
    service: http://localhost:3000  # New service

  - service: http_status:404
```

Then restart: `systemctl restart cloudflared`

## Troubleshooting

### App not accessible via domain

1. **Check if app is running locally:**
   ```bash
   curl http://localhost:5000
   systemctl status intern-crud
   ```

2. **Check cloudflared status:**
   ```bash
   systemctl status cloudflared
   journalctl -u cloudflared -n 50
   ```

3. **Verify tunnel config:**
   ```bash
   cat /root/.cloudflared/config.yml
   ```

4. **Check DNS in Cloudflare:**
   - Go to Cloudflare dashboard → DNS
   - Ensure CNAME record exists for `intern-crud`
   - Target should be: `307dcf72-cd57-47b5-b763-e60abf641dcc.cfargotunnel.com`

### Database errors

```bash
cd /opt/intern-crud/backend
python3 -m flask db upgrade
systemctl restart intern-crud
```

### Permission errors on uploads

```bash
chmod 755 /opt/intern-crud/uploads/resumes
chown -R root:root /opt/intern-crud/uploads
```

## Backup

```bash
# Backup database
cp /opt/intern-crud/backend/instance/intern_crud.db ~/backup-$(date +%Y%m%d).db

# Backup uploads
tar -czf ~/uploads-backup-$(date +%Y%m%d).tar.gz /opt/intern-crud/uploads/
```

## Useful Commands

```bash
# Restart everything
systemctl restart intern-crud cloudflared nginx

# View all logs
tail -f /var/log/intern-crud-*.log

# Check what's listening on ports
netstat -tlnp | grep -E ':(8000|5000)'

# Test app locally
curl -I http://localhost:5000
```

## Summary

Your intern-crud application is now:
- ✅ Running on Mikrus VPS
- ✅ Accessible via Cloudflare Tunnel
- ✅ Secured with HTTPS (automatic)
- ✅ Protected by Cloudflare DDoS protection
- ✅ Auto-restarts on failure
- ✅ Logging to `/var/log/intern-crud-*.log`

**Live at**: https://intern-crud.codewithpeter.com 🚀

For detailed documentation, see [DEPLOYMENT-MIKRUS.md](DEPLOYMENT-MIKRUS.md)

