# Deployment Guide for Mikrus VPS

This guide explains how to deploy the intern-crud application on a Mikrus VPS with IPv6-mostly configuration.

**Note**: The deployment script configures the application to run on `localhost:5000` to avoid conflicts with other services (like Coolify dashboard on port 8000).

## Understanding Mikrus Setup

Mikrus uses **IPv6-mostly** architecture with shared IPv4. You'll receive:
- **VPS ID**: 3-digit number (e.g., 123)
- **Server**: e.g., srv20.mikr.us
- **SSH Port**: `10000 + ID` (e.g., 10123)
- **Custom Ports**: `20000 + ID` and `30000 + ID` (e.g., 20123, 30123)
- **Additional**: 5 extra TCP ports available in panel

## Prerequisites

- Mikrus VPS account with active server
- SSH access to your VPS
- Your VPS ID number
- Basic terminal knowledge

## Deployment Options

### Option 1: Free Mikrus Subdomain (Recommended for Beginners)
- Get free subdomain like `yourapp.m.mikr.us`
- Automatic HTTPS certificate
- No domain purchase needed
- **Best for**: Testing, personal projects, portfolios

### Option 2: Custom Domain via Cloudflare (Recommended for Production)
- Use your own domain (e.g., `intern.yourdomain.com`)
- Free Cloudflare CDN and DDoS protection
- IPv4→IPv6 tunneling handled by Cloudflare
- Automatic SSL/TLS certificates
- **Best for**: Professional projects, production apps

## Step 1: Connect to Your Mikrus VPS

```bash
# Replace 123 with your VPS ID
# Replace srv20 with your server name
ssh root@srv20.mikr.us -p10123
```

## Step 2: Install Dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Python 3.10+ and required tools
apt install -y python3 python3-pip python3-venv git nginx

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

## Step 3: Clone and Setup Application

```bash
# Clone repository
cd /opt
git clone https://github.com/pbrudny/intern-crud.git
cd intern-crud

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e .
uv pip install gunicorn

# Create production environment file
cp .env.example .env
nano .env
```

**Edit `.env` file:**
```bash
# Generate secret key first:
python3 -c "import secrets; print(secrets.token_hex(32))"

# Then add to .env:
SECRET_KEY=<your-generated-secret-key>
DATABASE_URL=sqlite:///instance/intern_crud.db
FLASK_ENV=production
UPLOAD_FOLDER=/opt/intern-crud/uploads/resumes
MAX_CONTENT_LENGTH=2097152
```

## Step 4: Initialize Database

```bash
cd /opt/intern-crud/backend

# Run migrations
python3 -m flask db upgrade

# Create upload directory
mkdir -p /opt/intern-crud/uploads/resumes
chmod 755 /opt/intern-crud/uploads/resumes
```

## Step 5: Create Systemd Service

```bash
nano /etc/systemd/system/intern-crud.service
```

**Add this content:**
```ini
[Unit]
Description=Intern CRUD Flask Application
After=network.target

[Service]
Type=notify
User=root
WorkingDirectory=/opt/intern-crud/backend
Environment="PATH=/opt/intern-crud/.venv/bin"
ExecStart=/opt/intern-crud/.venv/bin/gunicorn \
    --bind 127.0.0.1:8000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile /var/log/intern-crud-access.log \
    --error-logfile /var/log/intern-crud-error.log \
    run:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
systemctl daemon-reload
systemctl enable intern-crud
systemctl start intern-crud
systemctl status intern-crud
```

## Step 6A: Setup with Mikrus Free Subdomain

### 6A.1: Configure Nginx

```bash
nano /etc/nginx/sites-available/intern-crud
```

**Add this configuration:**
```nginx
server {
    listen [::]:80;
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable site:**
```bash
ln -s /etc/nginx/sites-available/intern-crud /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 6A.2: Setup Mikrus Subdomain in Panel

1. Log in to Mikrus panel: https://mikr.us/panel
2. Go to your VPS settings
3. Find "Subdomeny" (Subdomains) section
4. Add new subdomain (e.g., `intern-crud`)
5. Point it to port `80` (where Nginx listens)
6. Save and wait 1-2 minutes for DNS propagation

Your app will be available at: `https://intern-crud.m.mikr.us` (HTTPS automatic!)

## Step 6B: Setup with Custom Domain via Cloudflare Tunnel (Recommended!)

**Cloudflare Tunnel** is the best option for Mikrus - it creates a secure tunnel without exposing ports!

### 6B.1: Install Cloudflared

```bash
# Download and install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
dpkg -i cloudflared-linux-amd64.deb
```

### 6B.2: Authenticate with Cloudflare

```bash
cloudflared tunnel login
```

This opens a browser - log in to Cloudflare and select your domain.

### 6B.3: Create Tunnel

```bash
# Create a new tunnel (replace 'intern-crud' with your preferred name)
cloudflared tunnel create intern-crud

# This creates a credentials file at:
# /root/.cloudflared/<TUNNEL-ID>.json
# Note the TUNNEL-ID shown in output!
```

### 6B.4: Configure Tunnel

```bash
# Create config file
nano /root/.cloudflared/config.yml
```

**Add this configuration:**
```yaml
tunnel: <YOUR-TUNNEL-ID>
credentials-file: /root/.cloudflared/<YOUR-TUNNEL-ID>.json

ingress:
  # Your intern-crud application
  - hostname: intern-crud.yourdomain.com
    service: http://localhost:8000

  # Add more services if needed
  # - hostname: another-app.yourdomain.com
  #   service: http://localhost:3000

  # Catch-all rule (required)
  - service: http_status:404
```

**Example (based on your config):**
```yaml
tunnel: 307dcf72-cd57-47b5-b763-e60abf641dcc
credentials-file: /root/.cloudflared/307dcf72-cd57-47b5-b763-e60abf641dcc.json

ingress:
  - hostname: intern-crud.codewithpeter.com
    service: http://localhost:8000

  - service: http_status:404
```

### 6B.5: Route DNS to Tunnel

```bash
# Replace with your tunnel name and hostname
cloudflared tunnel route dns intern-crud intern-crud.yourdomain.com
```

This automatically creates a CNAME record in Cloudflare DNS.

### 6B.6: Run Tunnel as Service

```bash
# Install as systemd service
cloudflared service install

# Start the service
systemctl start cloudflared
systemctl enable cloudflared

# Check status
systemctl status cloudflared
```

### 6B.7: Verify

Visit `https://intern-crud.yourdomain.com` - your app should be live!

**Benefits of Cloudflare Tunnel:**
- ✅ No need to expose ports (works perfectly with Mikrus shared IPv4)
- ✅ Automatic HTTPS/SSL
- ✅ IPv4→IPv6 tunneling handled automatically
- ✅ DDoS protection
- ✅ No Nginx configuration needed (tunnel connects directly to app)
- ✅ Can run multiple services on same VPS with different subdomains
- ✅ Works even if your VPS only has IPv6

## Step 6C: Setup with Custom Domain via Cloudflare DNS (Alternative)

If you prefer traditional DNS setup instead of tunnels:

### 6C.1: Configure Nginx (Same as 6A.1)

Follow Step 6A.1 above.

### 6C.2: Setup Cloudflare DNS

1. **Add your domain to Cloudflare** (if not already):
   - Go to https://cloudflare.com
   - Add site → Enter your domain
   - Follow DNS migration instructions

2. **Create DNS Record**:
   - Go to DNS settings
   - Add **AAAA record**:
     - Name: `intern-crud` (or `@` for root domain)
     - IPv6 Address: Your Mikrus VPS IPv6 (find in panel)
     - Proxy status: **Proxied** (orange cloud) ✅
     - TTL: Auto

3. **SSL/TLS Settings**:
   - Go to SSL/TLS → Overview
   - Set to **Full** or **Flexible**

4. **Done!** Your app is now at: `https://intern-crud.yourdomain.com`

## Monitoring and Maintenance

### Check Application Status
```bash
systemctl status intern-crud
```

### View Logs
```bash
# Application logs
tail -f /var/log/intern-crud-error.log
tail -f /var/log/intern-crud-access.log

# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### Restart Application
```bash
systemctl restart intern-crud
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

## Backup Strategy

### Database Backup
```bash
# Create backup script
nano /root/backup-intern-crud.sh
```

**Add:**
```bash
#!/bin/bash
BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp /opt/intern-crud/backend/instance/intern_crud.db $BACKUP_DIR/intern_crud_$DATE.db
# Keep only last 7 backups
ls -t $BACKUP_DIR/intern_crud_*.db | tail -n +8 | xargs rm -f
```

**Make executable and add to cron:**
```bash
chmod +x /root/backup-intern-crud.sh
crontab -e
# Add: 0 2 * * * /root/backup-intern-crud.sh
```

## Troubleshooting

### Application won't start
```bash
# Check logs
journalctl -u intern-crud -n 50
# Check if port 8000 is in use
netstat -tlnp | grep 8000
```

### Nginx errors
```bash
# Test configuration
nginx -t
# Check if Nginx is running
systemctl status nginx
```

### Can't access via subdomain
- Wait 2-5 minutes for DNS propagation
- Check Mikrus panel subdomain configuration
- Verify Nginx is listening on port 80: `netstat -tlnp | grep :80`

### Database errors
```bash
# Check database file permissions
ls -la /opt/intern-crud/backend/instance/
# Ensure migrations are applied
cd /opt/intern-crud/backend && python3 -m flask db upgrade
```

## Security Recommendations

1. **Change default SSH port** (in Mikrus panel)
2. **Use strong SECRET_KEY** (generated with secrets module)
3. **Regular updates**: `apt update && apt upgrade`
4. **Monitor logs** for suspicious activity
5. **Enable Cloudflare** for DDoS protection
6. **Regular backups** (automated via cron)

## Performance Tips

- **Workers**: Adjust Gunicorn workers based on RAM (formula: `2 * CPU + 1`)
- **Nginx caching**: Add caching for static files
- **Cloudflare**: Enable caching and minification
- **Database**: Consider PostgreSQL for production (if needed)

## Cost Estimate

- **Mikrus VPS**: 35-99 PLN/year (depending on plan)
- **Domain** (optional): ~50 PLN/year
- **Cloudflare**: FREE
- **Total**: 35-150 PLN/year (~$10-40/year)

## Next Steps

1. ✅ Deploy application
2. ✅ Setup subdomain or Cloudflare
3. ✅ Create first admin user
4. ✅ Test all functionality
5. ✅ Setup automated backups
6. 📊 Monitor performance
7. 🚀 Share with users!

---

**Need help?** Check Mikrus documentation: https://mikr.us/pomoc

