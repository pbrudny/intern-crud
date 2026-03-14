#!/bin/bash
# Automated deployment script for Mikrus VPS
# Usage: ./deploy-mikrus.sh

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Intern CRUD - Mikrus VPS Deployment${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (use: sudo ./deploy-mikrus.sh)${NC}"
    exit 1
fi

# Step 1: Update system
echo -e "\n${YELLOW}Step 1: Updating system...${NC}"
apt update && apt upgrade -y

# Step 2: Install dependencies
echo -e "\n${YELLOW}Step 2: Installing dependencies...${NC}"
apt install -y python3 python3-pip python3-venv git nginx curl

# Step 3: Install uv
echo -e "\n${YELLOW}Step 3: Installing uv package manager...${NC}"
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Step 4: Clone repository (if not already in /opt/intern-crud)
if [ ! -d "/opt/intern-crud" ]; then
    echo -e "\n${YELLOW}Step 4: Cloning repository...${NC}"
    cd /opt
    git clone https://github.com/pbrudny/intern-crud.git
else
    echo -e "\n${YELLOW}Step 4: Repository already exists, pulling latest...${NC}"
    cd /opt/intern-crud
    git pull origin main
fi

# Step 5: Setup Python environment
echo -e "\n${YELLOW}Step 5: Setting up Python environment...${NC}"
cd /opt/intern-crud
if [ ! -d ".venv" ]; then
    $HOME/.cargo/bin/uv venv
fi
source .venv/bin/activate
$HOME/.cargo/bin/uv pip install -e .
$HOME/.cargo/bin/uv pip install gunicorn

# Step 6: Create .env file
echo -e "\n${YELLOW}Step 6: Creating environment configuration...${NC}"
if [ ! -f ".env" ]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    cat > .env << EOF
SECRET_KEY=$SECRET_KEY
DATABASE_URL=sqlite:///instance/intern_crud.db
FLASK_ENV=production
UPLOAD_FOLDER=/opt/intern-crud/uploads/resumes
MAX_CONTENT_LENGTH=2097152
EOF
    echo -e "${GREEN}✓ Created .env with generated SECRET_KEY${NC}"
else
    echo -e "${YELLOW}! .env already exists, skipping...${NC}"
fi

# Step 7: Initialize database
echo -e "\n${YELLOW}Step 7: Initializing database...${NC}"
cd /opt/intern-crud/backend
python3 -m flask db upgrade

# Step 8: Create upload directory
echo -e "\n${YELLOW}Step 8: Creating upload directory...${NC}"
mkdir -p /opt/intern-crud/uploads/resumes
chmod 755 /opt/intern-crud/uploads/resumes

# Step 9: Create systemd service
echo -e "\n${YELLOW}Step 9: Creating systemd service...${NC}"
cat > /etc/systemd/system/intern-crud.service << 'EOF'
[Unit]
Description=Intern CRUD Flask Application
After=network.target

[Service]
Type=notify
User=root
WorkingDirectory=/opt/intern-crud/backend
Environment="PATH=/opt/intern-crud/.venv/bin"
ExecStart=/opt/intern-crud/.venv/bin/gunicorn \
    --bind 127.0.0.1:5000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile /var/log/intern-crud-access.log \
    --error-logfile /var/log/intern-crud-error.log \
    run:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable intern-crud
systemctl start intern-crud

# Step 10: Configure Nginx
echo -e "\n${YELLOW}Step 10: Configuring Nginx...${NC}"
cat > /etc/nginx/sites-available/intern-crud << 'EOF'
server {
    listen [::]:80;
    listen 80;
    server_name _;

    client_max_body_size 2M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/intern-crud/backend/app/static;
        expires 30d;
    }
}
EOF

ln -sf /etc/nginx/sites-available/intern-crud /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# Final status check
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${YELLOW}Service Status:${NC}"
systemctl status intern-crud --no-pager -l

echo -e "\n${YELLOW}Next Steps:${NC}"
echo -e "1. Setup Mikrus subdomain in panel: https://mikr.us/panel"
echo -e "   - Point subdomain to port 80"
echo -e "   - Your app will be at: https://yourname.m.mikr.us"
echo -e ""
echo -e "2. OR setup Cloudflare for custom domain:"
echo -e "   - Add AAAA record with your VPS IPv6"
echo -e "   - Enable proxy (orange cloud)"
echo -e "   - Your app will be at: https://yourdomain.com"
echo -e ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo -e "  View logs: tail -f /var/log/intern-crud-error.log"
echo -e "  Restart: systemctl restart intern-crud"
echo -e "  Status: systemctl status intern-crud"
echo -e ""
echo -e "${GREEN}Happy hosting! 🚀${NC}\n"

