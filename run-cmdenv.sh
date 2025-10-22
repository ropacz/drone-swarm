#!/bin/bash
# Run Drone Swarm Simulation with Cmdenv (console mode)

export OMNETPP_ROOT="/Users/rodrigo/omnetpp-workspace/omnetpp-6.2.0"
export INET_PROJ="/Users/rodrigo/omnetpp-workspace/inet-4.5.4"

echo "==========================================="
echo "Drone Swarm Simulation - Console Mode"
echo "==========================================="
echo ""

# Use first argument as config, default to DroneSwarm5km
CONFIG=${1:-DroneSwarm5km}

echo "Configuration: $CONFIG"
echo "Mode: Cmdenv (console)"
echo ""
echo "Available configuration:"
echo "  DroneSwarm5km - 10 drones, 5km × 5km SAR area"
echo ""

# Run with Cmdenv inside opp_env shell
opp_env shell omnetpp-6.2.0 << EOF
cd /Users/rodrigo/omnetpp-workspace/drone-sar/simulations
../out/clang-release/src/drone-sar -u Cmdenv -c $CONFIG \
    -n .:../src:\$INET_PROJ/src \
    --ned-path=.:../src:\$INET_PROJ/src \
    -l \$INET_PROJ/src/INET \
    omnetpp.ini
EOF
