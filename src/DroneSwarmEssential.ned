//===================================================================================
// DRONE SWARM NETWORK - Flying Ad-Hoc Network (FANET) Simulation
//===================================================================================
// Author: Rodrigo Paczkovski
// Institution: University of Santa Catarina (UFSC)
// Program: Master's in Computer Science
// Date: October 2025
// Repository: github.com/ropacz/drone-swarm
// 
// Description:
//   OMNeT++/INET-based simulation framework for UAV swarm coordination
//   in Search and Rescue (SAR) operations using IEEE 802.11 ad-hoc networking.
//
// References:
//   [1] Bekmezci et al. (2013) "Flying Ad-Hoc Networks (FANETs): A survey"
//   [2] Yanmaz et al. (2018) "Drone networks: Communications, coordination, and sensing"
//   [3] INET Framework 4.5.4 - https://inet.omnetpp.org/
//   [4] OMNeT++ 6.2.0 - https://omnetpp.org/
//===================================================================================

package drone.swarm;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.physicallayer.wireless.ieee80211.packetlevel.Ieee80211ScalarRadioMedium;
import inet.visualizer.canvas.integrated.IntegratedCanvasVisualizer;
import inet.node.inet.AdhocHost;

//===================================================================================
// MODULE: Drone (UAV)
//===================================================================================
// Mobile node with mesh routing and wireless communication
// Base: INET AdhocHost (standard for MANET/FANET nodes)
// Routing: AODV (Ad-hoc On-Demand Distance Vector) for multi-hop mesh
//===================================================================================
module Drone extends AdhocHost
{
    parameters:
        @display("i=misc/drone");
        mobility.typename = default("GaussMarkovMobility");
        numWlanInterfaces = 1;
        hasUdp = true;
        hasIpv4 = true;
        hasTcp = false;
        @networkNode();
}

//===================================================================================
// MODULE: Ground Control Station (GCS)
//===================================================================================
// Stationary base station for monitoring and control
// Routing: AODV enabled for mesh network participation
//===================================================================================
module GCS extends AdhocHost
{
    parameters:
        @display("i=device/antennatower");
        mobility.typename = default("StationaryMobility");
        numWlanInterfaces = 1;
        hasUdp = true;
        hasIpv4 = true;
        @networkNode();
}

//===================================================================================
// NETWORK: Drone Swarm Network
//===================================================================================
// Ad-hoc mesh topology for UAV swarm coordination
// Ref: [1] Bekmezci et al. (2013) "Flying Ad-Hoc Networks (FANETs): A survey"
//===================================================================================
network DroneSwarmNetwork
{
    parameters:
        int numDrones = default(15);        // Swarm size (optimized for 4km² area)
        int numGCS = default(1);            // Ground control stations
        
        // Canvas: 4km × 4km (1:1 coordinate mapping with 100m grid)
        // Ref: [3] Hayat et al. (2016) "Survey on UAV networks for disaster relief"
        @display("bgb=4000,4000;bgg=100,1,grey95");
        @figure[title](type=text; pos=2000,100; anchor=c; text="FANET Drone Swarm - SAR Operations"; font="Arial,18,bold"; color=darkblue);
        
    submodules:
        //-------------------------------------------------------------------------------
        // Network Infrastructure
        //-------------------------------------------------------------------------------
        configurator: Ipv4NetworkConfigurator {
            @display("p=50,50;is=s");
            addStaticRoutes = false;
            addDefaultRoutes = false;
            addSubnetRoutes = false;
        }
        
        radioMedium: Ieee80211ScalarRadioMedium {
            @display("p=50,100;is=s");
        }
        
        visualizer: IntegratedCanvasVisualizer {
            @display("p=50,150;is=s");
        }
        
        //-------------------------------------------------------------------------------
        // Drones and GCS
        //-------------------------------------------------------------------------------
        drone[numDrones]: Drone;
        gcs[numGCS]: GCS;
}
