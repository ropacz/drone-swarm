# 🚁 DRONE SWARM - Simulação de Enxame de Drones

## 🎯 Foco: Tecnologias Apropriadas para Enxames Reais

**Filosofia:** Apenas o necessário, com escolhas técnicas justificadas.

---

## 🚀 Como Executar

### Compilar o projeto:
```bash
make makefiles
make
```

### Executar com interface gráfica (Qtenv):
```bash
./run.sh [Config]
```

### Executar em modo console (Cmdenv):
```bash
./run-cmdenv.sh [Config]
```

**Configurações disponíveis:**
- `Base` (padrão) - 10 drones
- `Small` - 5 drones
- `Large` - 20 drones
- `HighSpeed` - Velocidade aumentada
- `Formation` - Formação em grid

**Exemplo:**
```bash
./run.sh Base          # GUI com 10 drones
./run-cmdenv.sh Large  # Console com 20 drones
```

---

## 🔧 DECISÕES TÉCNICAS FUNDAMENTAIS

### 1️⃣ **Roteamento: OLSR (não AODV)**

**Por quê OLSR?**
- ✅ **Proativo**: Rotas sempre disponíveis (zero latência de descoberta)
- ✅ **MPR (Multi-Point Relay)**: Reduz flooding em topologia densa
- ✅ **Mesh natural**: Ideal para comunicação frequente entre todos
- ✅ **Real world**: Usado em projetos como Serval Mesh, ComMotion

**Quando AODV?**
- ❌ Enxames = comunicação constante
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