//===================================================================================
// BatRouting.h - Bat Algorithm Routing Protocol for FANETs
//===================================================================================
// Bio-inspired routing using frequency, loudness, and pulse rate for route
// optimization in drone swarm networks.
//===================================================================================

#ifndef __DRONE_SWARM_BATROUTING_H_
#define __DRONE_SWARM_BATROUTING_H_

#include <omnetpp.h>
#include <vector>
#include <map>

using namespace omnetpp;

// Route information structure
struct RouteInfo {
    std::vector<int> path;
    double fitness;
    double hopCount;
    double linkQuality;
    double energyCost;
    simtime_t lastUpdate;
    
    RouteInfo() : fitness(1e9), hopCount(0), linkQuality(0), energyCost(0) {}
};

// Route discovery packet
class RouteDiscoveryPacket : public cMessage {
  public:
    std::vector<int> visitedNodes;
    int sourceId;
    int destId;
    double accumulatedFitness;
    
    RouteDiscoveryPacket(const char *name=nullptr) : cMessage(name) {
        sourceId = -1;
        destId = -1;
        accumulatedFitness = 0.0;
        setKind(1);
    }
    
    virtual RouteDiscoveryPacket *dup() const override {
        return new RouteDiscoveryPacket(*this);
    }
};

// Data packet with routing information
class DataPacket : public cMessage {
  public:
    int sourceId;
    int destId;
    int currentHop;
    std::vector<int> routePath;
    
    DataPacket(const char *name=nullptr) : cMessage(name) {
        sourceId = -1;
        destId = -1;
        currentHop = 0;
        setKind(2);
    }
    
    virtual DataPacket *dup() const override {
        return new DataPacket(*this);
    }
};

class BatRouting : public cSimpleModule
{
  private:
    // Bat Algorithm parameters
    double frequencyMin, frequencyMax;
    double currentLoudness, currentPulseRate;
    double initialLoudness, initialPulseRate;
    double alpha, gamma;
    
    // Routing parameters
    double routingUpdateInterval;
    double hopCountWeight, linkQualityWeight;
    double energyWeight, mobilityWeight;
    int maxRoutesPerDestination;
    double routeTimeout;
    double communicationRange;
    
    // Route table
    std::map<int, std::vector<RouteInfo>> routeTable;
    std::map<int, simtime_t> neighborLastSeen;
    
    // Statistics
    simsignal_t routeDiscoveredSignal;
    simsignal_t packetRoutedSignal;
    
    // Timers
    cMessage *routeUpdateTimer;
    int myNodeId;
    
  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
    
    // Routing functions
    void discoverRoutes();
    void processRouteDiscovery(RouteDiscoveryPacket *pkt);
    void updateRouteTable(int dest, const RouteInfo &route);
    RouteInfo* selectBestRoute(int dest);
    void routeDataPacket(DataPacket *pkt);
    
    // Bat Algorithm
    double calculateRouteFitness(const RouteInfo &route);
    void optimizeRouteTable();
    void updateBatParameters();
    
    // Helper functions
    double calculateLinkQuality(int nodeA, int nodeB);
    double calculateNodeMobility(int nodeId);
    void broadcastRouteDiscovery(int destId);
    void cleanupExpiredRoutes();
    
  public:
    BatRouting();
    virtual ~BatRouting();
    
    int getMyNodeId() const { return myNodeId; }
    std::vector<int> getNeighborIds();
};

#endif
