#!/bin/bash
#===================================================================================
# analyze.sh - Quick wrapper for analyze_results.py
#===================================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================${NC}"
echo -e "${BLUE}  Drone SAR Results Analyzer${NC}"
echo -e "${BLUE}=================================${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 not found!${NC}"
    exit 1
fi

# Check if dependencies are installed
python3 -c "import matplotlib, numpy" 2>/dev/null || {
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip3 install matplotlib numpy --quiet
    echo -e "${GREEN}✅ Dependencies installed${NC}"
    echo ""
}

# Parse arguments
CONFIG="${1:-all}"

if [ "$CONFIG" = "all" ]; then
    echo -e "${GREEN}📊 Analyzing all configurations...${NC}"
    python3 analyze_results.py --all
else
    echo -e "${GREEN}📊 Analyzing configuration: $CONFIG${NC}"
    python3 analyze_results.py --config "$CONFIG"
fi

echo ""
echo -e "${GREEN}✅ Analysis complete!${NC}"

# Try to open results on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    if [ "$CONFIG" = "all" ]; then
        OUTPUT_DIR="analysis"
    else
        OUTPUT_DIR="analysis/$CONFIG"
    fi
    
    if [ -d "$OUTPUT_DIR" ]; then
        echo -e "${BLUE}📂 Opening results folder...${NC}"
        open "$OUTPUT_DIR"
    fi
fi
