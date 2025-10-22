# UAV Swarm Simulation - Bat Algorithm Routing for FANETs

[![OMNeT++](https://img.shields.io/badge/OMNeT++-6.2.0-blue)](https://omnetpp.org/)
[![INET](https://img.shields.io/badge/INET-4.5.4-green)](https://inet.omnetpp.org/)
[![License](https://img.shields.io/badge/license-Academic-orange)](LICENSE)

## 🎯 Overview

Discrete-event simulation framework for **Flying Ad-Hoc Networks (FANETs)** implementing **Bat Algorithm** bio-inspired routing for UAV swarm coordination. Developed for academic research in multi-hop drone mesh networking.

### ✨ Key Features

- 🦇 **Bat Algorithm Routing**: Bio-inspired metaheuristic with frequency modulation, loudness adaptation, and pulse rate control
- ✈️ **3D Mobility**: Gauss-Markov model with realistic UAV flight dynamics (15 m/s cruise speed)
- 📡 **IEEE 802.11a @ 5.8 GHz**: Industry-standard wireless mesh networking
- 📊 **Multi-Criteria Optimization**: Hop count, link quality, energy cost, and mobility-aware routing
- 🎯 **SAR Operations**: Search and Rescue mission scenarios over 4km × 4km areas
- 📈 **Statistics Collection**: Route discovery, packet routing, and Bat Algorithm performance metrics

---

## 📋 System Requirements

### Software
- **OMNeT++** 6.2.0 or higher
- **INET Framework** 4.5.4
- **C++17** compatible compiler (GCC 9+ / Clang 10+)
- **Qt5** (optional, for GUI visualization)

### Recommended Hardware
- **CPU**: 4+ cores
- **RAM**: 8 GB minimum (16 GB for large swarms)
- **Storage**: 1 GB (framework + results)

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/ropacz/drone-swarm.git
cd drone-swarm
```

### 2. Build Project
```bash
./build.sh
```

### 3. Compile
```bash
./rebuild.sh  # Clean build with INET dependencies
# or
./build.sh    # Incremental build
```

---

## Running Simulations

### Quick Start (GUI Mode)
```bash
./run.sh DroneSwarm5km
```

### Console Mode (Faster)
```bash
./run-cmdenv.sh DroneSwarm5km
```

### Output Files
Results are saved in `simulations/results/`:
- `*.sca`: Scalar statistics (averages, counts)
- `*.vec`: Vector data (time series)
- `*.vci`: Vector index files

### 📊 Results Analysis

Generate Bat Algorithm performance visualizations:

```bash
./analyze.sh all                              # All configs
./analyze.sh DroneSwarm5km                    # Specific config
```

**5 publication-ready figures:** UAV performance, statistical distribution, consistency analysis, swarm efficiency, performance heatmap. See [ANALYSIS.md](ANALYSIS.md) for details.

---

## Routing Protocol - Bat Algorithm

The simulation uses a **bio-inspired routing protocol** based on the Bat Algorithm, optimizing routes using:

- **Frequency**: Diversity in route exploration
- **Loudness**: Exploitation vs exploration balance
- **Pulse Rate**: Route discovery probability

### Multi-Criteria Optimization
Routes are evaluated based on:
- Hop count (weight: 1.0)
- Link quality (weight: 1.5)
- Energy cost (weight: 1.0)
- Node mobility (weight: 0.8)

### Configuration
Edit `src/omnetpp.ini` to adjust Bat Algorithm parameters:

```ini
*.drone[*].batRouting.pulseRate = 0.5          # Discovery probability
*.drone[*].batRouting.loudness = 0.9           # Exploration rate
*.drone[*].batRouting.routingUpdateInterval = 5s
*.drone[*].batRouting.maxRoutesPerDestination = 3
```

---

## Simulation Parameters

### Network Topology
| Parameter | Value | Justification |
|-----------|-------|---------------|
| Swarm size | 10 UAVs | Balanced for 4 km² area |
| Operational area | 4 km² | SAR operation zone |
| Altitude range | 50-120 m | FAA Part 107 compliant |
| GCS nodes | 1 | Single ground control station |

### Mobility Model (Gauss-Markov)
| Parameter | Value | Reference |
|-----------|-------|-----------|
| Cruise speed | 15 m/s (54 km/h) | DJI Mavic 3 specs |
| Alpha (correlation) | 0.9 | Smooth coordinated movement |
| Update interval | 500 ms | Realistic trajectory updates |

### Wireless Communication
| Parameter | Value | Standard/Reference |
|-----------|-------|--------------------|
| Frequency | 5.8 GHz | ISM band, FCC Part 15.247 [6] |
| Tx power | 100 mW (20 dBm) | Legal unlicensed limit [7] |
| Bandwidth | 20 MHz | IEEE 802.11a/ac |
| Receiver sensitivity | -92 dBm | Typical WiFi chips [8] |

### Application Layer
| Parameter | Value | Justification |
|-----------|-------|---------------|
| Telemetry rate | 10 Hz | MAVLink standard [9] |
| Packet size | 150 bytes | Position + velocity + status |
| Protocol | UDP multicast | Efficient broadcast [10] |

---

## Configuration Scenarios

### Base Configuration (Standard)
```ini
[Config Base]
*.numDrones = 10
Area: 2km × 2km (4 km²)
Speed: 15 m/s
```
**Use:** Standard swarm for general research and algorithm validation.

### SmallArea (Quick Testing)
```ini
[Config SmallArea]
*.numDrones = 10
Area: 1km × 1km (1 km²)
Speed: 15 m/s
```
**Use:** Fast testing and debugging. Smaller area for quick iterations.

### FloodSAR (Disaster Response)
```ini
[Config FloodSAR]
*.numDrones = 15
Area: 2km × 2km (4 km²)
Speed: 12 m/s (scanning)
```
**Use:** Realistic flood disaster SAR mission. Optimized for victim search.

---

## Academic References

### Primary Citations

1. **Brust et al. (2017)** - "Target tracking optimization of UAV swarms based on dual-decomposition"  
   *IEEE Conference on Computer Communications Workshops*

2. **Bekmezci et al. (2013)** - "Flying Ad-Hoc Networks (FANETs): A survey"  
   *Ad Hoc Networks, Elsevier*

3. **Yanmaz et al. (2018)** - "Drone networks: Communications, coordination, and sensing"  
   *Ad Hoc Networks, Elsevier*

4. **Camp et al. (2002)** - "A survey of mobility models for ad hoc network research"  
   *Wireless Communications and Mobile Computing*

5. **RFC 3626** - "Optimized Link State Routing Protocol (OLSR)"  
   *IETF Network Working Group*

### Technical Standards

- **IEEE 802.11-2016**: Wireless LAN MAC and PHY specifications
- **FAA Part 107**: Small Unmanned Aircraft Systems regulations
- **FCC Part 15.247**: Operation in 5.725-5.850 GHz band
- **MAVLink Protocol**: Micro air vehicle communication standard

### Commercial References

- DJI Mavic 3 Technical Specifications
- Pixhawk Autopilot Documentation
- Auterion Skynode Platform Specifications

---

## Project Structure

```
drone-sar/
├── src/
│   ├── DroneSwarmEssential.ned    # Network topology definition
│   ├── omnetpp.ini                # Simulation parameters
│   ├── package.ned                # Package declaration
│   └── Makefile                   # Build configuration
├── simulations/
│   ├── omnetpp.ini                # Simulation entry point
│   ├── package.ned
│   └── results/                   # Output directory (auto-generated)
├── run.sh                         # GUI execution script
├── run-cmdenv.sh                  # Console execution script
├── Makefile                       # Top-level build file
├── .gitignore
└── README.md
```

---

## Metrics and Analysis

### Key Performance Indicators (KPIs)

The simulation tracks the following metrics for research analysis:

1. **Packet Delivery Ratio (PDR)**
   ```
   PDR = (Packets Received) / (Packets Sent) × 100%
   ```

2. **End-to-End Delay**
   - Average latency for telemetry packets
   - Critical for real-time coordination

3. **Network Throughput**
   - Aggregate data rate across swarm
   - Per-link and network-wide measurements

4. **Radio State Analysis**
   - Idle / Tx / Rx time distribution
   - Channel utilization metrics

### Post-Simulation Analysis

Use OMNeT++ analysis tools:
```bash
# Open in IDE Analysis Tool
omnetpp simulations/results/Base-*.sca

# Or use Python/R for custom analysis
# Scalar data: CSV export from .sca files
# Vector data: Parse .vec files with scavetool
```

---

## Customization Guide

### Adding New Mobility Patterns

Edit `src/omnetpp.ini`:
```ini
*.drone[*].mobility.typename = "MassMobility"  # Or other INET mobility models
```

Available models: RandomWaypointMobility, CircleMobility, LinearMobility, etc.

### Changing Communication Parameters

Modify transmit power for range studies:
```ini
*.drone[*].wlan[0].radio.transmitter.power = 200mW  # 23 dBm
```

### Adding Energy Models

Integrate INET energy storage:
```ned
module Drone extends AdhocHost {
    parameters:
        energyStorage.typename = "SimpleEpEnergyStorage";
        energyStorage.nominalCapacity = 108000J;  # 30 Wh battery
}
```

---

## Troubleshooting

### Common Issues

**Problem**: `ERROR: Network 'DroneSwarmNetwork' not found`  
**Solution**: Check package name in .ned files matches .ini reference

**Problem**: Large .vec files (>100 MB)  
**Solution**: Results are in `.gitignore`. Use `result-dir` to organize output.

**Problem**: Compilation errors  
**Solution**: Verify INET path in environment:
```bash
export INET_PROJ=/path/to/inet-4.x
```

---

## Citation

If you use this simulation framework in your research, please cite:

```bibtex
@misc{droneswarm2025,
  author = {[Your Name]},
  title = {UAV Swarm Simulation Framework for FANET Research},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/ropacz/drone-swarm}
}
```

---

## License

This project is licensed under the **Academic Free License** - see LICENSE file for details.

**For commercial use**, contact the authors for licensing terms.

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewMobility`)
3. Commit changes with clear messages
4. Submit a pull request

---

## Contact

**Author**: [Your Name]  
**Institution**: [Your University]  
**Email**: [your.email@university.edu]  
**Research Group**: [Lab/Research Group Name]

---

## Acknowledgments

- **OMNeT++ Community** for the excellent simulation framework
- **INET Framework Team** for comprehensive protocol implementations
- **[Your Advisor/Supervisor]** for research guidance

---

**Last Updated**: October 2025
- ✅ Comunicação esporádica ponto-a-ponto

```ini
*.drone[*].hasOlsr = true
*.drone[*].routing.olsr.helloInterval = 2s
```

---

### 2️⃣ **Comunicação: WiFi 5.8 GHz**

**Por quê 5.8 GHz?**
- ✅ **Menos congestionado** que 2.4 GHz
- ✅ **Padrão FPV**: DJI, Walksnail, HDZero
- ✅ **Range adequado**: 300-500m (suficiente para enxames)
- ✅ **Legal**: Permitido em vários países sem licença

**Alternativas consideradas:**
- 2.4 GHz: Mais range, mas interferência alta
- LoRa: Range alto, mas bandwidth baixo
- LTE/5G: Depende de infraestrutura

```ini
*.drone[*].wlan[0].radio.carrierFrequency = 5.8GHz
*.drone[*].wlan[0].radio.transmitter.power = 100mW     # 20 dBm
```

---

### 3️⃣ **Propagação: Two-Ray (não Free Space)**

**Por quê Two-Ray?**
- ✅ **Reflexão no solo**: Crítico para 40-120m de altitude
- ✅ **Mais realista**: Free Space superestima cobertura
- ✅ **Validado**: Usado em estudos de drones comerciais

**Comparação:**

| Modelo | Uso | Realismo |
|--------|-----|----------|
| Free Space | Satélites, >1km | Baixo |
| **Two-Ray** | **Drones 40-120m** | **Alto** |
| Log-Distance | Ambientes urbanos | Médio |

```ini
*.radioMedium.pathLossType = "TwoRayGroundReflection"
```

---

### 4️⃣ **Bateria: 30 Wh (não 100 Wh)**

**Por quê 30 Wh?**
- ✅ **Realista**: DJI Mini 3 = 30 Wh, Mavic = 45 Wh
- ✅ **15-20 min voo**: Tempo real para 250-500g
- ✅ **Comercial**: Maioria dos drones consumer

**100 Wh é para:**
- Drones industriais (>2kg)
- Missões longas especializadas
- Não representa enxames típicos

```ini
*.drone[*].energyStorage.nominalCapacity = 108000J  # 30 Wh
```

**Consumo baseado em dados reais:**
- Hover: 100W (6W/célula × 3S × 5A)
- Voo: 130W (média com deslocamento)
- Transmissão: +3W

---

### 5️⃣ **Mobilidade: Gauss-Markov Alpha=0.8**

**Por quê Alpha alto?**
- ✅ **Coesão**: Enxames precisam se manter próximos
- ✅ **Coordenação**: Movimento suave e previsível
- ✅ **Realismo**: Simula controle cooperativo

**Efeito do Alpha:**

| Alpha | Comportamento | Uso |
|-------|---------------|-----|
| 0.5 | Aleatório | Exploração |
| **0.8** | **Coordenado** | **Enxames** |
| 0.95 | Rígido | Formação fixa |

```ini
*.drone[*].mobility.alpha = 0.8
*.drone[*].mobility.speedMean = 15mps  # 54 km/h - eficiente
```

---

### 6️⃣ **Tráfego: Multicast (não Unicast)**

**Por quê Multicast?**
- ✅ **Eficiência**: Um pacote para todos
- ✅ **Coordenação**: Estado compartilhado
- ✅ **Overhead baixo**: Vs. N unicasts

**Protocolo de estado:**
- Posição (x,y,z): 12 bytes
- Velocidade (vx,vy,vz): 12 bytes
- Orientação: 4 bytes
- Estado/missão: 20 bytes
- Header: 100 bytes
- **Total: ~150 bytes @ 10 Hz = 12 kbps/drone**

```ini
*.drone[*].app[0].destAddresses = "224.0.0.1"  # Multicast
*.drone[*].app[0].messageLength = 150B
*.drone[*].app[0].sendInterval = 100ms         # 10 Hz
```

---

## 📊 COMPARAÇÃO: Apropriado vs. Teórico

| Parâmetro | Teórico | **Apropriado** | Justificativa |
|-----------|---------|----------------|---------------|
| **Roteamento** | AODV | **OLSR** | Mesh denso |
| **Frequência** | 2.4 GHz | **5.8 GHz** | Menos interferência |
| **Propagação** | Free Space | **Two-Ray** | Reflexão solo |
| **Bateria** | 100 Wh | **30 Wh** | Drones comerciais |
| **Potência** | 30 dBm | **20 dBm (100mW)** | Legal/comercial |
| **Drones** | 25 | **10** | Gerenciável |
| **Alpha** | 0.75 | **0.8** | Coesão |
| **Velocidade** | 20 m/s | **15 m/s** | Eficiente |

---

## 🎮 CENÁRIOS INCLUÍDOS

### **Base** - Padrão
```bash
./swarm -u Cmdenv -c Base
```
- 10 drones
- Velocidade 15 m/s
- 5 minutos

### **Small** - Enxame Pequeno
```bash
./swarm -u Cmdenv -c Small
```
- 5 drones
- Testes rápidos

### **Large** - Enxame Grande
```bash
./swarm -u Cmdenv -c Large
```
- 20 drones
- Estresse de rede

### **HighSpeed** - Alta Velocidade
```bash
./swarm -u Cmdenv -c HighSpeed
```
- 25 m/s (90 km/h)
- Teste de mobilidade

### **Formation** - Formação em Grid
```bash
./swarm -u Cmdenv -c Formation
```
- Posição inicial organizada
- Alpha 0.9 (mantém formação)

---

## 📈 MÉTRICAS RELEVANTES

### **Conectividade do Enxame**
- Quantos drones estão conectados?
- Há particionamento da rede?

### **Latência de Atualização**
- Delay das mensagens de estado
- Frequência de recepção (10 Hz?)

### **Overhead de Roteamento**
- Pacotes OLSR vs. dados
- Eficiência do MPR

### **Autonomia**
- Tempo até bateria crítica
- Consumo por fase

### **Throughput Efetivo**
- Taxa de dados úteis
- PDR (Packet Delivery Ratio)

---

## 🔍 O QUE FOI REMOVIDO E POR QUÊ

### ❌ **AODV**
- Não apropriado para mesh denso
- Latência de descoberta inaceitável

### ❌ **Free Space Propagation**
- Irreal para drones <150m
- Ignora reflexão crítica

### ❌ **Bateria 100 Wh**
- Não representa mercado
- Peso excessivo

### ❌ **Vítimas/Sensores/Água**
- Foco = enxame puro
- Expansível depois

### ❌ **Potência 30 dBm**
- Ilegal sem licença
- Desnecessário

### ❌ **25+ Drones no Base**
- Simulação lenta
- 10 suficiente para análise

---

## 💡 TECNOLOGIAS MODERNAS CONSIDERADAS

### ✅ **Incluídas:**
- OLSR (roteamento mesh maduro)
- 5.8 GHz (padrão FPV)
- Two-Ray (modelo validado)
- Multicast (eficiência)

### 🔮 **Futuro (não essencial agora):**
- B.A.T.M.A.N. routing (mais moderno que OLSR)
- WiFi 6/6E (6 GHz)
- AI-based mobility
- Swarming algorithms (flocking, consensus)

---

## 📚 REFERÊNCIAS TÉCNICAS

### Roteamento Mesh:
- RFC 3626 - OLSR
- B.A.T.M.A.N. protocol papers
- Serval Project documentation

### Propagação:
- Two-Ray Ground Reflection Model (Rappaport)
- ITU-R P.528 (air-to-ground)

### Hardware Real:
- DJI specifications
- Pixhawk/ArduPilot telemetry
- RFD900x datasheet
- ESP32 WiFi specifications

### Enxames:
- Swarm intelligence algorithms
- Craig Reynolds "Boids" (flocking)
- Multi-agent coordination

---

## 🚀 PRÓXIMOS PASSOS

### **Para Expandir:**

1. **Algoritmos de Formação**
   ```cpp
   // Flocking behavior
   // Leader-follower
   // Consensus-based
   ```

2. **Missões Cooperativas**
   - Coverage paths
   - Target tracking
   - Area scanning

3. **Falhas e Recuperação**
   - Drone failure handling
   - Network partitioning
   - Battery emergency

4. **Integração Sensores**
   - Camera payloads
   - LiDAR sensing
   - GPS/IMU data

---

## ✅ VALIDAÇÃO

**Esta configuração é apropriada porque:**

✅ Usa hardware/software que existe (DJI, Pixhawk)  
✅ Parâmetros de drones comerciais reais  
✅ Protocolos provados em campo (OLSR)  
✅ Modelos de propagação validados  
✅ Consumo energético realista  
✅ Escalável e expansível  

---

## 📞 ARQUIVOS

- **[omnetpp_essential.ini](computer:///mnt/user-data/outputs/omnetpp_essential.ini)** - Configuração (~200 linhas)
- **[DroneSwarmEssential.ned](computer:///mnt/user-data/outputs/DroneSwarmEssential.ned)** - Topologia (~50 linhas)

**Total: ~250 linhas de código essencial e apropriado**

---

**✨ Configuração baseada em tecnologias reais e apropriadas para enxames modernos!** 🐝

**Filosofia: "Simples o suficiente, mas não mais simples" - Einstein**