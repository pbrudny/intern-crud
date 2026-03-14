#!/bin/bash
# Script to commit changes and deploy to Mikrus VPS
# Usage: ./commit-and-deploy.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Commit and Deploy to Mikrus VPS${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Step 1: Abort any pending merge
echo -e "${YELLOW}Step 1: Cleaning up git state...${NC}"
git merge --abort 2>/dev/null || true

# Step 2: Checkout feature branch
echo -e "${YELLOW}Step 2: Switching to feature branch...${NC}"
git checkout 001-intern-crud-app

# Step 3: Add all changes
echo -e "${YELLOW}Step 3: Staging changes...${NC}"
git add -A

# Step 4: Commit
echo -e "${YELLOW}Step 4: Committing changes...${NC}"
git commit -m "Update deployment for port 5000 and correct VPS details

- Configure deploy-mikrus.sh to use port 5000 (avoid Coolify conflict)
- Update QUICKSTART-MIKRUS.md with correct VPS: steve107.mikrus.xyz:10107
- Update DEPLOYMENT-MIKRUS.md with port configuration note
- Remove Docker/Coolify files
- Add ProxyFix to backend/config.py for Cloudflare Tunnel
- Matches existing Cloudflare Tunnel configuration (port 5000)" || echo "Nothing to commit or already committed"

# Step 5: Push to feature branch
echo -e "${YELLOW}Step 5: Pushing to feature branch...${NC}"
git push origin 001-intern-crud-app

# Step 6: Merge to main
echo -e "${YELLOW}Step 6: Merging to main...${NC}"
git checkout main
git merge 001-intern-crud-app --no-edit
git push origin main

# Step 7: Switch back to feature branch
git checkout 001-intern-crud-app

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Git operations complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Step 8: Ask about deployment
echo -e "${YELLOW}Ready to deploy to Mikrus VPS?${NC}"
echo -e "This will SSH to: ${GREEN}root@steve107.mikrus.xyz -p10107${NC}"
echo -e ""
read -p "Deploy now? (y/n): " DEPLOY

if [ "$DEPLOY" = "y" ]; then
    echo -e "\n${YELLOW}Deploying to Mikrus VPS...${NC}\n"
    
    ssh root@steve107.mikrus.xyz -p10107 << 'ENDSSH'
        echo "Connected to Mikrus VPS!"
        echo "Downloading deployment script..."
        curl -sSL https://raw.githubusercontent.com/pbrudny/intern-crud/main/deploy-mikrus.sh -o /tmp/deploy-mikrus.sh
        chmod +x /tmp/deploy-mikrus.sh
        echo "Running deployment..."
        /tmp/deploy-mikrus.sh
ENDSSH
    
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}Deployment Complete!${NC}"
    echo -e "${GREEN}========================================${NC}\n"
    echo -e "Your app should be live at: ${GREEN}https://intern-crud.codewithpeter.com${NC}"
    echo -e ""
    echo -e "${YELLOW}Note:${NC} Your Cloudflare Tunnel is already configured correctly!"
    echo -e "  - Coolify: dashboard.codewithpeter.com → localhost:8000"
    echo -e "  - Intern-CRUD: intern-crud.codewithpeter.com → localhost:5000"
else
    echo -e "\n${YELLOW}Skipping deployment.${NC}"
    echo -e "To deploy manually later, run:"
    echo -e "  ${GREEN}ssh root@steve107.mikrus.xyz -p10107${NC}"
    echo -e "  ${GREEN}curl -sSL https://raw.githubusercontent.com/pbrudny/intern-crud/main/deploy-mikrus.sh | bash${NC}"
fi

echo -e "\n${GREEN}Done! 🚀${NC}\n"

