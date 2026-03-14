#!/bin/bash
# Helper script to add intern-crud to existing Cloudflare Tunnel
# Usage: ./cloudflare-tunnel-add-service.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Add Intern-CRUD to Cloudflare Tunnel${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo -e "${RED}cloudflared is not installed!${NC}"
    echo -e "${YELLOW}Installing cloudflared...${NC}"
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    dpkg -i cloudflared-linux-amd64.deb
    rm cloudflared-linux-amd64.deb
    echo -e "${GREEN}✓ cloudflared installed${NC}"
fi

# Find existing config
CONFIG_FILE="/root/.cloudflared/config.yml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}No existing Cloudflare Tunnel config found at $CONFIG_FILE${NC}"
    echo -e "${YELLOW}Please run full Cloudflare Tunnel setup first.${NC}"
    exit 1
fi

echo -e "${YELLOW}Current Cloudflare Tunnel configuration:${NC}"
cat "$CONFIG_FILE"
echo ""

# Get user input
read -p "Enter hostname for intern-crud (e.g., intern-crud.yourdomain.com): " HOSTNAME
read -p "Enter local port where intern-crud runs [default: 8000]: " PORT
PORT=${PORT:-8000}

# Backup existing config
cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
echo -e "${GREEN}✓ Backed up existing config${NC}"

# Check if hostname already exists
if grep -q "hostname: $HOSTNAME" "$CONFIG_FILE"; then
    echo -e "${YELLOW}! Hostname $HOSTNAME already exists in config${NC}"
    read -p "Do you want to update it? (y/n): " UPDATE
    if [ "$UPDATE" != "y" ]; then
        echo -e "${RED}Aborted${NC}"
        exit 1
    fi
    # Remove existing entry
    sed -i "/hostname: $HOSTNAME/,+1d" "$CONFIG_FILE"
fi

# Add new service before the catch-all rule
# Find the line with "- service: http_status:404"
LINE_NUM=$(grep -n "service: http_status:404" "$CONFIG_FILE" | cut -d: -f1)

if [ -z "$LINE_NUM" ]; then
    echo -e "${RED}Could not find catch-all rule in config${NC}"
    exit 1
fi

# Insert new service before catch-all
sed -i "${LINE_NUM}i\\  - hostname: $HOSTNAME\n    service: http://localhost:$PORT\n" "$CONFIG_FILE"

echo -e "\n${GREEN}✓ Updated Cloudflare Tunnel configuration${NC}"
echo -e "\n${YELLOW}New configuration:${NC}"
cat "$CONFIG_FILE"

# Restart cloudflared service
echo -e "\n${YELLOW}Restarting cloudflared service...${NC}"
systemctl restart cloudflared
sleep 2
systemctl status cloudflared --no-pager -l

# Get tunnel info
TUNNEL_ID=$(grep "^tunnel:" "$CONFIG_FILE" | awk '{print $2}')
TUNNEL_NAME=$(cloudflared tunnel info "$TUNNEL_ID" 2>/dev/null | grep "Name:" | awk '{print $2}' || echo "unknown")

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Configuration Complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${YELLOW}Next Steps:${NC}"
echo -e "1. Create DNS record (if not already done):"
echo -e "   ${GREEN}cloudflared tunnel route dns $TUNNEL_NAME $HOSTNAME${NC}"
echo -e ""
echo -e "2. Or manually in Cloudflare dashboard:"
echo -e "   - Go to DNS settings"
echo -e "   - Add CNAME record:"
echo -e "     Name: ${GREEN}$(echo $HOSTNAME | cut -d. -f1)${NC}"
echo -e "     Target: ${GREEN}$TUNNEL_ID.cfargotunnel.com${NC}"
echo -e "     Proxy: ${GREEN}Enabled (orange cloud)${NC}"
echo -e ""
echo -e "3. Wait 1-2 minutes for DNS propagation"
echo -e ""
echo -e "4. Visit: ${GREEN}https://$HOSTNAME${NC}"
echo -e ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo -e "  View tunnel status: ${GREEN}cloudflared tunnel info $TUNNEL_ID${NC}"
echo -e "  View logs: ${GREEN}journalctl -u cloudflared -f${NC}"
echo -e "  Restart tunnel: ${GREEN}systemctl restart cloudflared${NC}"
echo -e ""
echo -e "${GREEN}Done! 🚀${NC}\n"

