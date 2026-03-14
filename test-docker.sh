#!/bin/bash
# Test Docker build and run locally before deploying to Coolify

set -e

echo "🐳 Testing Docker build for Coolify deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Generate a test secret key
TEST_SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")

echo -e "${YELLOW}Step 1: Building Docker image...${NC}"
docker build -t intern-crud:test .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Docker build successful${NC}"
else
    echo -e "${RED}✗ Docker build failed${NC}"
    exit 1
fi

echo -e "\n${YELLOW}Step 2: Starting container...${NC}"
docker run -d \
    --name intern-crud-test \
    -p 8000:8000 \
    -e SECRET_KEY="$TEST_SECRET" \
    -e DATABASE_URL="sqlite:///instance/intern_crud.db" \
    -e FLASK_ENV="production" \
    intern-crud:test

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Container started${NC}"
else
    echo -e "${RED}✗ Container failed to start${NC}"
    exit 1
fi

echo -e "\n${YELLOW}Step 3: Waiting for application to start...${NC}"
sleep 10

echo -e "\n${YELLOW}Step 4: Testing health check...${NC}"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
    echo -e "${GREEN}✓ Application is responding (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}✗ Application health check failed (HTTP $HTTP_CODE)${NC}"
    echo -e "\n${YELLOW}Container logs:${NC}"
    docker logs intern-crud-test
    docker stop intern-crud-test
    docker rm intern-crud-test
    exit 1
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✓ All tests passed!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}Application is running at:${NC} http://localhost:8000"
echo -e "\n${YELLOW}To view logs:${NC}"
echo -e "  docker logs -f intern-crud-test"
echo -e "\n${YELLOW}To stop and cleanup:${NC}"
echo -e "  docker stop intern-crud-test"
echo -e "  docker rm intern-crud-test"
echo -e "  docker rmi intern-crud:test"
echo -e "\n${YELLOW}To test with docker-compose:${NC}"
echo -e "  docker-compose up -d"
echo -e "  docker-compose logs -f"
echo -e "  docker-compose down"
echo -e "\n${GREEN}Ready for Coolify deployment! 🚀${NC}"

