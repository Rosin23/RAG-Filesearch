#!/bin/bash

# Start FLAMEHAVEN FileSearch API Server
# Usage: ./scripts/start_server.sh [dev|prod]

MODE=${1:-dev}

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting FLAMEHAVEN FileSearch API Server${NC}"
echo "=========================================="

# Check if API key is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${YELLOW}Warning: GEMINI_API_KEY not set${NC}"
    echo "Please set your API key:"
    echo "  export GEMINI_API_KEY='your-api-key'"
    exit 1
fi

# Load .env if it exists
if [ -f .env ]; then
    echo "Loading environment from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "API Key: ${GEMINI_API_KEY:0:10}..."
echo "Mode: $MODE"
echo ""

if [ "$MODE" == "prod" ]; then
    echo "Starting in PRODUCTION mode..."
    echo "Workers: 4"
    echo "Host: 0.0.0.0"
    echo "Port: 8000"
    echo ""
    uvicorn flamehaven_filesearch.api:app \
        --host 0.0.0.0 \
        --port 8000 \
        --workers 4 \
        --log-level info
else
    echo "Starting in DEVELOPMENT mode..."
    echo "Auto-reload: enabled"
    echo "Host: 0.0.0.0"
    echo "Port: 8000"
    echo ""
    echo "API Docs: http://localhost:8000/docs"
    echo "Health Check: http://localhost:8000/health"
    echo ""
    uvicorn flamehaven_filesearch.api:app \
        --reload \
        --host 0.0.0.0 \
        --port 8000 \
        --log-level debug
fi
