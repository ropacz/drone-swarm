//===================================================================================
// BatRouting.h - Bat Algorithm Routing Protocol for FANETs
//===================================================================================
// Bio-inspired routing protocol using Bat Algorithm metaheuristics
// Features: Frequency modulation, loudness adaptation, pulse rate control
// Application: Multi-hop mesh routing in drone swarm networks
//===================================================================================

#ifndef __DRONE_SWARM_BATROUTING_H_
#define __DRONE_SWARM_BATROUTING_H_

#include <omnetpp.h>
#include <vector>
#include <map>

using namespace omnetpp;

//-----------------------------------------------------------------------------------
// Route Information Structure
//-----------------------------------------------------------------------------------
struct RouteInfo {
    std::vector<int> path;        // Sequence of node IDs forming the route
    double fitness;               // Bat Algorithm fitness value
    double hopCount;              // Number of hops in route
    double linkQuality;           // Average link quality (0-1)
    double energyCost;            // Estimated energy consumption
    simtime_t lastUpdate;         // Timestamp of last update
    
    RouteInfo() : fitness(1e9), hopCount(0), linkQuality(0), energyCost(0) {}
};

//-----------------------------------------------------------------------------------
// Route Discovery Packet (RREQ/RREP)
//-----------------------------------------------------------------------------------
class RouteDiscoveryPacket : public cMessage {
  public:
    std::vector<int> visitedNodes;     // Path history (loop prevention)
    int sourceId;                       // Route request originator
    int destId;                         // Target destination
    double accumulatedFitness;          // Cumulative fitness along path
    
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

//-----------------------------------------------------------------------------------
// Data Packet with Routing Information
//-----------------------------------------------------------------------------------
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

//-----------------------------------------------------------------------------------
// Bat Routing Module
//-----------------------------------------------------------------------------------
class BatRouting : public cSimpleModule
{
  private:
    // === Bat Algorithm Parameters ===
    double frequencyMin, frequencyMax;       // Frequency range [0-2 Hz]
    double currentLoudness, currentPulseRate; // Dynamic adaptation
    double initialLoudness, initialPulseRate; // Initial values
    double alpha, gamma;                      // Adaptation coefficients
    
    // === Routing Parameters ===
    double routingUpdateInterval;            // Route discovery period
    double hopCountWeight;                   // Fitness weight: hop count
    double linkQualityWeight;                // Fitness weight: link quality
    double energyWeight;                     // Fitness weight: energy
    double mobilityWeight;                   // Fitness weight: mobility
    int maxRoutesPerDestination;             // Max alternative routes
    double routeTimeout;                     // Route expiration time
    double communicationRange;               // Radio range (meters)
    
    // === Route Table ===
    std::map<int, std::vector<RouteInfo>> routeTable;  // dest -> routes[]
    std::map<int, simtime_t> neighborLastSeen;         // neighbor -> timestamp
    
    // === Statistics ===
    simsignal_t routeDiscoveredSignal;
    simsignal_t packetRoutedSignal;
    
    // === State ===
    cMessage *routeUpdateTimer;
    int myNodeId;
    
  protected:
    // === Lifecycle ===
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
    
    // === Routing Functions ===
    void discoverRoutes();
    void processRouteDiscovery(RouteDiscoveryPacket *pkt);
    void updateRouteTable(int dest, const RouteInfo &route);
    RouteInfo* selectBestRoute(int dest);
    void routeDataPacket(DataPacket *pkt);
    
    // === Bat Algorithm ===
    double calculateRouteFitness(const RouteInfo &route);
    void optimizeRouteTable();
    void updateBatParameters();
    
    // === Helpers ===
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
