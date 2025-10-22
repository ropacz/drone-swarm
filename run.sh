#!/bin/bash
# Run Drone Swarm Simulation with Qtenv

export OMNETPP_ROOT="/Users/rodrigo/omnetpp-workspace/omnetpp-6.2.0"
export INET_PROJ="/Users/rodrigo/omnetpp-workspace/inet-4.5.4"

# Fix for Qt display issues on macOS
export QT_MAC_WANTS_LAYER=1
export QT_AUTO_SCREEN_SCALE_FACTOR=1
export QT_ENABLE_HIGHDPI_SCALING=1
export QT_QPA_PLATFORMTHEME=""
export QT_STYLE_OVERRIDE="Fusion"

echo "==========================================="
echo "Drone Swarm Simulation - OMNeT++ / INET"
echo "==========================================="
echo ""

# Use first argument as config, default to DroneSwarm5km
CONFIG=${1:-DroneSwarm5km}

echo "Configuration: $CONFIG"
echo "Mode: Qtenv (GUI)"
echo ""
echo "Available configuration:"
echo "  DroneSwarm5km - 10 drones, 5km × 5km SAR area"
echo ""

# Run with Qtenv inside opp_env shell
opp_env shell omnetpp-6.2.0 << EOF
cd /Users/rodrigo/omnetpp-workspace/drone-sar/simulations
/Users/rodrigo/omnetpp-workspace/out/clang-release/src/drone-sar -u Qtenv -c $CONFIG \
    -n .:../src:\$INET_PROJ/src \
    --ned-path=.:../src:\$INET_PROJ/src \
    --image-path=\$INET_PROJ/images \
    -l \$INET_PROJ/src/INET \
    omnetpp.ini
EOF
