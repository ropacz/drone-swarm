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

source "$OMNETPP_ROOT/setenv" -f

cd simulations

echo "==========================================="
echo "Drone Swarm Simulation - OMNeT++ / INET"
echo "==========================================="
echo ""

# Use first argument as config, default to Base
CONFIG=${1:-Base}

echo "Configuração: $CONFIG"
echo "Modo: Qtenv (GUI)"
echo ""

# Run with Qtenv
../out/clang-release/src/drone-sar -u Qtenv -c $CONFIG \
    -n .:../src:$INET_PROJ/src \
    --image-path=$INET_PROJ/images \
    -l $INET_PROJ/src/INET \
    omnetpp.ini
