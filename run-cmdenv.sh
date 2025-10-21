#!/bin/bash
# Run Drone Swarm Simulation with Cmdenv (console mode)

export OMNETPP_ROOT="/Users/rodrigo/omnetpp-workspace/omnetpp-6.2.0"
export INET_PROJ="/Users/rodrigo/omnetpp-workspace/inet-4.5.4"

source "$OMNETPP_ROOT/setenv" -f

cd simulations

echo "==========================================="
echo "Drone Swarm Simulation - Console Mode"
echo "==========================================="
echo ""

# Use first argument as config, default to Base
CONFIG=${1:-Base}

echo "Configuração: $CONFIG"
echo "Modo: Cmdenv (console)"
echo ""

# Run with Cmdenv
../out/clang-release/src/drone-sar -u Cmdenv -c $CONFIG \
    -n .:../src:$INET_PROJ/src \
    -l $INET_PROJ/src/INET \
    omnetpp.ini
