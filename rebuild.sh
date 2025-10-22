#!/bin/bash
# Clean and rebuild script for drone-sar simulation

set -e

echo "=========================================="
echo "Cleaning and Rebuilding Drone SAR"
echo "=========================================="

# Enter opp_env shell and clean/rebuild
opp_env shell omnetpp-6.2.0 << 'EOF'
cd /Users/rodrigo/omnetpp-workspace/drone-sar

# Clean old build
echo "Cleaning old build..."
rm -rf out
cd src
make clean || true

# Regenerate Makefile with correct INET paths
echo "Regenerating Makefile..."
opp_makemake -f --deep -O ../out -KINET_PROJ=/Users/rodrigo/omnetpp-workspace/inet-4.5.4 -DINET_IMPORT -I/Users/rodrigo/omnetpp-workspace/inet-4.5.4/src -L/Users/rodrigo/omnetpp-workspace/inet-4.5.4/src -lINET

# Build in release mode
echo "Building project..."
make MODE=release

echo ""
echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="
EOF
