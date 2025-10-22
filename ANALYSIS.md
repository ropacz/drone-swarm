# 📊 Análise de Resultados

## 🚀 Início Rápido

```bash
# 1. Instalar dependências (apenas primeira vez)
pip install matplotlib numpy

# 2. Analisar resultados
./analyze.sh all
```

## Requisitos

- Python 3.7+
- matplotlib
- numpy

## Uso

```bash
# Wrapper simplificado (recomendado)
./analyze.sh all                              # Todas configurações
./analyze.sh DroneSwarm5km                    # Específica

# Python direto
python3 analyze_results.py --all              # Todas
python3 analyze_results.py --config DroneSwarm5km  # Específica
python3 analyze_results.py --help             # Ajuda
```

## Gráficos Gerados

O script gera automaticamente 5 visualizações focadas no **Bat Algorithm para FANETs**:

### 📊 1. **UAV Route Discovery** (`bat_routes_per_drone.png`)
- **Foco:** Desempenho individual de cada UAV no enxame
- **Visualização:** Gráfico de barras com gradiente de cores
- **Inclui:** 
  - Barras de erro (desvio padrão entre runs)
  - Linha de média do enxame
  - Legendas explicativas sobre Bat Algorithm
  - Rodapé com parâmetros: loudness, pulse rate, frequency

### 📈 2. **Statistical Distribution** (`bat_distribution.png`)
- **Foco:** Distribuição estatística da descoberta de rotas
- **Visualização:** Histograma com 25 bins e gradiente azul
- **Inclui:**
  - Marcadores de média e mediana
  - Caixa de estatísticas completa (min, max, std, sample)
  - Contexto SAR e parâmetros do Bat Algorithm

### 📦 3. **Consistency Analysis** (`bat_consistency.png`)
- **Foco:** Consistência do algoritmo entre diferentes execuções
- **Visualização:** Box plot com cores indicando performance
- **Inclui:**
  - Quartis (Q1, Q2, Q3) e whiskers (1.5×IQR)
  - Coeficiente de variação (CV)
  - Interpretação de consistência de roteamento

### 🎯 4. **Swarm Efficiency** (`bat_efficiency.png`)
- **Foco:** Eficiência coletiva do enxame
- **Visualização:** Dupla - acumulação + contribuição individual
- **Inclui:**
  - Gráfico esquerdo: capacidade acumulada da rede
  - Gráfico direito: contribuição individual (verde=acima média, vermelho=abaixo)
  - Percentuais de cobertura

### 🌡️ 5. **Performance Heatmap** (`bat_heatmap.png`)
- **Foco:** Visão espacial-temporal do desempenho
- **Visualização:** Mapa de calor UAVs × Runs
- **Inclui:**
  - Colormap RdYlGn (vermelho-amarelo-verde)
  - Anotações numéricas em cada célula
  - Estatísticas de desempenho do enxame
  - Contexto de missão SAR

## Estatísticas Calculadas

O script imprime automaticamente um resumo estatístico:

```
📊 Routes Discovered:
   Mean:   134.10      # Média de rotas descobertas
   Median: 128.50      # Valor mediano
   Std:    134.23      # Desvio padrão
   Range:  [0, 281]    # Intervalo [mínimo, máximo]
   Total:  2682        # Total acumulado
```

## Estrutura de Arquivos

```
drone-sar/
├── analyze_results.py          # Script principal de análise
├── simulations/
│   └── results/                # Resultados .sca e .vec do OMNeT++
│       ├── DroneSwarm5km-#0.sca
│       ├── DroneSwarm5km-#1.sca
│       └── ...
└── analysis/                   # Gráficos gerados (criado automaticamente)
    ├── routes_per_drone.png
    ├── route_distribution.png
    ├── route_variability.png
    ├── comparative_metrics.png
    └── performance_heatmap.png
```

## Customização

### Modificar resolução das imagens:

Edite as constantes no início do arquivo `analyze_results.py`:

```python
FIGURE_DPI = 300          # Aumentar para melhor qualidade
FIGURE_SIZE = (12, 8)     # Tamanho em polegadas (largura, altura)
```

### Adicionar novas métricas:

Procure por métricas em arquivos `.sca` com:

```bash
grep "^scalar" simulations/results/*.sca | head -20
```

Adicione novas métricas no método `print_summary()`:

```python
metrics = [
    ('routeDiscovered:count', 'Routes Discovered'),
    ('packetRouted:count', 'Packets Routed'),
    ('suaMetrica:count', 'Sua Nova Métrica'),  # Adicionar aqui
]
```

## Exemplos de Uso

### Análise por configuração separada:

```bash
# Analisar apenas DroneSwarm2km
python3 analyze_results.py --config DroneSwarm2km --output analysis/2km

# Analisar apenas DroneSwarm5km
python3 analyze_results.py --config DroneSwarm5km --output analysis/5km

# Comparar resultados lado a lado
open analysis/2km/routes_per_drone.png analysis/5km/routes_per_drone.png
```

### Pipeline completo de simulação + análise:

```bash
#!/bin/bash
# run_and_analyze.sh

# 1. Rodar simulações
./run-cmdenv.sh DroneSwarm5km

# 2. Analisar resultados
python3 analyze_results.py --config DroneSwarm5km

# 3. Abrir visualizações
open analysis/DroneSwarm5km/*.png
```

## Interpretação dos Resultados

### ✅ Bom desempenho:
- Baixa variabilidade entre runs (box plot compacto)
- Distribuição normal/uniforme das rotas descobertas
- Todos os drones com valores similares

### ⚠️ Possíveis problemas:
- Alta variabilidade entre runs → Algoritmo instável
- Drones com zero rotas → Problemas de mobilidade/alcance
- Outliers frequentes → Comportamento imprevisível

## Formato dos Arquivos .sca

Os arquivos `.sca` (scalar) do OMNeT++ têm o formato:

```
scalar DroneSwarmNetwork.drone[0].batRouting routeDiscovered:count 266
attr recordingmode count
attr title "Routes Discovered, count"
```

O script processa automaticamente:
- **Module path:** `drone[0].batRouting`
- **Metric name:** `routeDiscovered:count`
- **Value:** `266`

## Troubleshooting

| Problema | Solução |
|----------|---------|
| No .sca files found | Execute `./run-cmdenv.sh DroneSwarm5km` primeiro |
| ModuleNotFoundError | Execute `pip3 install matplotlib numpy` |
| Gráficos vazios | Verifique se há resultados em `simulations/results/` |

## Formato de Saída

- **Resolução:** 300 DPI (pronto para publicação)
- **Formato:** PNG (suporte a PDF/SVG modificando o código)
- **Localização:** `analysis/*.png`
