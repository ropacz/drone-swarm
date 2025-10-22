//===================================================================================
// BatRouting.ned - Bat Algorithm Routing Module
//===================================================================================

package drone.swarm;

import inet.applications.contract.IApp;

simple BatRouting like IApp
{
    parameters:
        @class(BatRouting);
        @display("i=block/routing");
        
        // Bat Algorithm parameters
        double routingUpdateInterval @unit(s) = default(5s);
        double frequencyMin = default(0.0);
        double frequencyMax = default(2.0);
        double loudness = default(0.9);
        double pulseRate = default(0.5);
        double alpha = default(0.9);
        double gamma = default(0.9);
        
        // Routing weights
        double hopCountWeight = default(1.0);
        double linkQualityWeight = default(1.5);
        double energyWeight = default(1.0);
        double mobilityWeight = default(0.8);
        
        // Route table configuration
        int maxRoutesPerDestination = default(3);
        double routeTimeout @unit(s) = default(30s);
        double communicationRange @unit(m) = default(700m);
        
        @signal[routeDiscovered](type=long);
        @statistic[routeDiscovered](title="Routes Discovered"; record=count,vector);
        @signal[packetRouted](type=long);
        @statistic[packetRouted](title="Packets Routed"; record=count,vector);
        
    gates:
        input socketIn;
        output socketOut;
}
