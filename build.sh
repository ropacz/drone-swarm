#!/bin/bash
# Build script for drone-sar simulation
# Requires opp_env to be installed

set -e

echo "=========================================="
echo "Building Drone SAR Simulation"
echo "=========================================="

# Enter opp_env shell and build
opp_env shell omnetpp-6.2.0 << 'EOF'
cd /Users/rodrigo/omnetpp-workspace/drone-sar/src
make MODE=release
echo "Build completed successfully!"
EOF
