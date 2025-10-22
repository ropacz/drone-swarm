//===================================================================================
// BatRouting.cc - Bat Algorithm Routing Implementation
//===================================================================================

#include "BatRouting.h"
#include "inet/mobility/base/MovingMobilityBase.h"
#include "inet/networklayer/common/L3AddressResolver.h"
#include "inet/common/ModuleAccess.h"
#include "inet/common/packet/Packet.h"
#include <algorithm>

using namespace inet;

Define_Module(BatRouting);

BatRouting::BatRouting()
{
    routeUpdateTimer = nullptr;
    myNodeId = -1;
}

BatRouting::~BatRouting()
{
    cancelAndDelete(routeUpdateTimer);
}

void BatRouting::initialize()
{
    cModule *parent = getParentModule();
    if (!parent) {
        EV_ERROR << "BatRouting: Cannot find parent module" << endl;
        return;
    }
    myNodeId = parent->getIndex();
    
    // Bat Algorithm parameters
    frequencyMin = par("frequencyMin");
    frequencyMax = par("frequencyMax");
    initialLoudness = par("loudness");
    initialPulseRate = par("pulseRate");
    currentLoudness = initialLoudness;
    currentPulseRate = initialPulseRate;
    alpha = par("alpha");
    gamma = par("gamma");
    
    // Routing parameters
    routingUpdateInterval = par("routingUpdateInterval");
    hopCountWeight = par("hopCountWeight");
    linkQualityWeight = par("linkQualityWeight");
    energyWeight = par("energyWeight");
    mobilityWeight = par("mobilityWeight");
    maxRoutesPerDestination = par("maxRoutesPerDestination");
    routeTimeout = par("routeTimeout");
    communicationRange = par("communicationRange");
    
    // Register signals
    routeDiscoveredSignal = registerSignal("routeDiscovered");
    packetRoutedSignal = registerSignal("packetRouted");
    
    // Schedule first route discovery
    routeUpdateTimer = new cMessage("routeUpdate");
    scheduleAt(simTime() + uniform(2, 3), routeUpdateTimer);
    
    EV << "BatRouting: Node " << myNodeId << " initialized" << endl;
}

void BatRouting::handleMessage(cMessage *msg)
{
    if (msg == routeUpdateTimer) {
        discoverRoutes();
        optimizeRouteTable();
        cleanupExpiredRoutes();
        scheduleAt(simTime() + routingUpdateInterval, routeUpdateTimer);
    }
    else if (auto routePkt = dynamic_cast<RouteDiscoveryPacket*>(msg)) {
        processRouteDiscovery(routePkt);
    }
    else if (auto dataPkt = dynamic_cast<DataPacket*>(msg)) {
        routeDataPacket(dataPkt);
    }
    else {
        delete msg;
    }
}

void BatRouting::discoverRoutes()
{
    cModule *network = getParentModule()->getParentModule();
    if (!network) return;
    
    int numNodes = network->getSubmoduleVectorSize("drone");
    
    for (int destId = 0; destId < numNodes; destId++) {
        if (destId == myNodeId) continue;
        
        double frequency = frequencyMin + (frequencyMax - frequencyMin) * uniform(0, 1);
        
        if (uniform(0, 1) < currentPulseRate) {
            broadcastRouteDiscovery(destId);
        }
    }
    
    updateBatParameters();
}

void BatRouting::broadcastRouteDiscovery(int destId)
{
    RouteDiscoveryPacket *pkt = new RouteDiscoveryPacket("RouteDiscovery");
    pkt->sourceId = myNodeId;
    pkt->destId = destId;
    pkt->visitedNodes.push_back(myNodeId);
    pkt->accumulatedFitness = 0.0;
    
    char msgName[32];
    sprintf(msgName, "RREQ %d->%d", myNodeId, destId);
    pkt->setName(msgName);
    
    EV << "BatRouting: Broadcasting " << msgName << endl;
    emit(routeDiscoveredSignal, 1);
    
    delete pkt;
}

void BatRouting::processRouteDiscovery(RouteDiscoveryPacket *pkt)
{
    // Check for loops
    for (int nodeId : pkt->visitedNodes) {
        if (nodeId == myNodeId) {
            delete pkt;
            return;
        }
    }
    
    pkt->visitedNodes.push_back(myNodeId);
    
    // Update fitness
    if (pkt->visitedNodes.size() > 1) {
        int prevNode = pkt->visitedNodes[pkt->visitedNodes.size() - 2];
        double linkQuality = calculateLinkQuality(prevNode, myNodeId);
        pkt->accumulatedFitness += (1.0 / (linkQuality + 0.1)) * hopCountWeight;
    }
    
    // Reached destination
    if (pkt->destId == myNodeId) {
        RouteInfo route;
        route.path = pkt->visitedNodes;
        route.hopCount = pkt->visitedNodes.size() - 1;
        route.fitness = pkt->accumulatedFitness;
        route.lastUpdate = simTime();
        
        cModule *parent = getParentModule();
        if (parent) {
            cModule *network = parent->getParentModule();
            if (network) {
                cModule *sourceDrone = network->getSubmodule("drone", pkt->sourceId);
                if (sourceDrone) {
                    cModule *sourceRoutingModule = sourceDrone->getSubmodule("batRouting");
                    if (sourceRoutingModule) {
                        try {
                            BatRouting *sourceRouting = check_and_cast<BatRouting*>(sourceRoutingModule);
                            sourceRouting->updateRouteTable(myNodeId, route);
                        } catch (const std::exception &e) {
                            EV_WARN << "BatRouting: Error updating route table" << endl;
                        }
                    }
                }
            }
        }
        
        emit(routeDiscoveredSignal, 1);
        delete pkt;
        return;
    }
    
    // Forward with loudness probability
    if (pkt->visitedNodes.size() < 10 && uniform(0, 1) < currentLoudness) {
        EV << "BatRouting: Forwarding RREQ " << pkt->sourceId << "->" << pkt->destId << endl;
    }
    
    delete pkt;
}

void BatRouting::updateRouteTable(int dest, const RouteInfo &route)
{
    auto &routes = routeTable[dest];
    routes.push_back(route);
    
    std::sort(routes.begin(), routes.end(), 
        [](const RouteInfo &a, const RouteInfo &b) {
            return a.fitness < b.fitness;
        });
    
    if (routes.size() > (size_t)maxRoutesPerDestination) {
        routes.resize(maxRoutesPerDestination);
    }
}

RouteInfo* BatRouting::selectBestRoute(int dest)
{
    auto it = routeTable.find(dest);
    if (it == routeTable.end() || it->second.empty()) {
        return nullptr;
    }
    return &(it->second[0]);
}

void BatRouting::routeDataPacket(DataPacket *pkt)
{
    emit(packetRoutedSignal, 1);
    
    RouteInfo *route = selectBestRoute(pkt->destId);
    if (route) {
        pkt->routePath = route->path;
        pkt->currentHop = 0;
    }
    
    delete pkt;
}

double BatRouting::calculateRouteFitness(const RouteInfo &route)
{
    double fitness = route.hopCount * hopCountWeight;
    fitness += (1.0 / (route.linkQuality + 0.1)) * linkQualityWeight;
    fitness += route.energyCost * energyWeight;
    
    for (size_t i = 0; i < route.path.size(); i++) {
        double mobility = calculateNodeMobility(route.path[i]);
        fitness += mobility * mobilityWeight;
    }
    
    return fitness;
}

void BatRouting::optimizeRouteTable()
{
    for (auto &entry : routeTable) {
        auto &routes = entry.second;
        
        for (auto &route : routes) {
            route.fitness = calculateRouteFitness(route);
        }
        
        std::sort(routes.begin(), routes.end(),
            [](const RouteInfo &a, const RouteInfo &b) {
                return a.fitness < b.fitness;
            });
    }
}

void BatRouting::updateBatParameters()
{
    currentLoudness = alpha * currentLoudness;
    currentPulseRate = initialPulseRate * (1.0 - exp(-gamma * simTime().dbl()));
    
    if (currentLoudness < 0.1) currentLoudness = 0.1;
    if (currentPulseRate > 0.95) currentPulseRate = 0.95;
}

double BatRouting::calculateLinkQuality(int nodeA, int nodeB)
{
    cModule *parent = getParentModule();
    if (!parent) return 0.0;
    
    cModule *network = parent->getParentModule();
    if (!network) return 0.0;
    
    cModule *droneA = network->getSubmodule("drone", nodeA);
    cModule *droneB = network->getSubmodule("drone", nodeB);
    if (!droneA || !droneB) return 0.0;
    
    cModule *mobA = droneA->getSubmodule("mobility");
    cModule *mobB = droneB->getSubmodule("mobility");
    if (!mobA || !mobB) return 0.0;
    
    try {
        MovingMobilityBase *mA = check_and_cast<MovingMobilityBase*>(mobA);
        MovingMobilityBase *mB = check_and_cast<MovingMobilityBase*>(mobB);
        
        double dist = mA->getCurrentPosition().distance(mB->getCurrentPosition());
        return std::max(0.0, 1.0 - (dist / communicationRange));
    } catch (const std::exception &e) {
        return 0.0;
    }
}

double BatRouting::calculateNodeMobility(int nodeId)
{
    return 0.1;
}

void BatRouting::cleanupExpiredRoutes()
{
    for (auto it = routeTable.begin(); it != routeTable.end(); ) {
        auto &routes = it->second;
        
        routes.erase(
            std::remove_if(routes.begin(), routes.end(),
                [this](const RouteInfo &route) {
                    return (simTime() - route.lastUpdate) > routeTimeout;
                }),
            routes.end()
        );
        
        if (routes.empty()) {
            it = routeTable.erase(it);
        } else {
            ++it;
        }
    }
}

std::vector<int> BatRouting::getNeighborIds()
{
    std::vector<int> neighbors;
    
    cModule *parent = getParentModule();
    if (!parent) return neighbors;
    
    cModule *network = parent->getParentModule();
    if (!network) return neighbors;
    
    cModule *myMobModule = parent->getSubmodule("mobility");
    if (!myMobModule) return neighbors;
    
    MovingMobilityBase *myMob = check_and_cast<MovingMobilityBase*>(myMobModule);
    
    int numNodes = network->getSubmoduleVectorSize("drone");
    for (int i = 0; i < numNodes; i++) {
        if (i == myNodeId) continue;
        
        cModule *otherDrone = network->getSubmodule("drone", i);
        if (otherDrone) {
            cModule *otherMobModule = otherDrone->getSubmodule("mobility");
            if (otherMobModule) {
                MovingMobilityBase *otherMob = check_and_cast<MovingMobilityBase*>(otherMobModule);
                
                double dist = myMob->getCurrentPosition().distance(otherMob->getCurrentPosition());
                if (dist < communicationRange) {
                    neighbors.push_back(i);
                }
            }
        }
    }
    
    return neighbors;
}

void BatRouting::finish()
{
    EV << "BatRouting: Node " << myNodeId << " - Routes in table: " 
       << routeTable.size() << endl;
}

// UdpSocket::ICallback implementations
void BatRouting::socketDataArrived(UdpSocket *sock, Packet *packet)
{
    EV << "BatRouting: Received packet " << packet->getName() << endl;
    delete packet;
}

void BatRouting::socketErrorArrived(UdpSocket *sock, Indication *indication)
{
    EV_WARN << "BatRouting: Socket error" << endl;
    delete indication;
}

void BatRouting::socketClosed(UdpSocket *sock)
{
    EV << "BatRouting: Socket closed" << endl;
}
