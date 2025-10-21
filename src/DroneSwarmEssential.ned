//===================================================================================
// DRONE SWARM NETWORK - Essencial
//===================================================================================

package drone.swarm;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.physicallayer.wireless.ieee80211.packetlevel.Ieee80211ScalarRadioMedium;
import inet.visualizer.canvas.integrated.IntegratedCanvasVisualizer;
import inet.node.inet.AdhocHost;

//===================================================================================
// Drone com OLSR e energia
//===================================================================================
module Drone extends AdhocHost
{
    parameters:
        @display("i=misc/drone");
        
        mobility.typename = default("GaussMarkovMobility");
        numWlanInterfaces = 1;
        
        @networkNode();
}

//===================================================================================
// Base de controle
//===================================================================================
module GCS extends AdhocHost
{
    parameters:
        @display("i=device/antennatower");
        mobility.typename = default("StationaryMobility");
        numWlanInterfaces = 1;
        
        @networkNode();
}

//===================================================================================
// Rede do enxame
//===================================================================================
network DroneSwarmNetwork
{
    parameters:
        int numDrones = default(10);
        int numGCS = default(1);
        @display("bgb=1000,1000");  // Área maior para acomodar coordenadas em metros
        
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=50,50;is=s");
            addStaticRoutes = false;    // OLSR gerencia rotas
        }
        
        radioMedium: Ieee80211ScalarRadioMedium {
            @display("p=50,100;is=s");
        }
        
        visualizer: IntegratedCanvasVisualizer {
            @display("p=50,150;is=s");
        }
        
        drone[numDrones]: Drone;
        gcs[numGCS]: GCS;
}
