#!/bin/bash

# Run tests for SovDef FileSearch Lite
# Usage: ./scripts/run_tests.sh [all|unit|integration|coverage]

TEST_TYPE=${1:-unit}

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Running SovDef FileSearch Lite Tests${NC}"
echo "====================================="
echo ""

case $TEST_TYPE in
    all)
        echo -e "${BLUE}Running ALL tests (unit + integration)${NC}"
        pytest -v
        ;;

    unit)
        echo -e "${BLUE}Running UNIT tests only${NC}"
        pytest -v -m "not integration"
        ;;

    integration)
        echo -e "${BLUE}Running INTEGRATION tests${NC}"
        if [ -z "$GEMINI_API_KEY" ]; then
            echo -e "${YELLOW}Warning: GEMINI_API_KEY not set${NC}"
            echo "Integration tests require a valid API key"
            exit 1
        fi
        pytest -v -m integration
        ;;

    coverage)
        echo -e "${BLUE}Running tests with COVERAGE report${NC}"
        pytest -v -m "not integration" \
            --cov=sovdef_filesearch_lite \
            --cov-report=html \
            --cov-report=term-missing \
            --cov-report=xml
        echo ""
        echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
        ;;

    *)
        echo "Usage: $0 [all|unit|integration|coverage]"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Tests completed!${NC}"
