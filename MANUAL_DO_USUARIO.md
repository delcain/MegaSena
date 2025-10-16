# 🎰 Mega Sena - Análise Probabilística Avançada

## 📋 Descrição do Projeto

Este aplicativo Python oferece análises completas e avançadas dos dados históricos da Mega Sena, implementando:

### 🎯 Funcionalidades Principais

1. **📥 Coleta de Dados Automática**
   - Obtém dados históricos da fonte oficial da Caixa Econômica Federal
   - Atualização automática com verificação de novos sorteios
   - Salvamento em JSON e CSV para análises futuras

2. **🎲 Análise Probabilística**
   - Cálculo de probabilidades específicas para números individuais
   - Análise de estratégias (pares/ímpares, números altos/baixos)
   - Estimativa de chances de repetições entre sorteios
   - Verificação de viés estatístico
   - Análise de retorno de investimento (ROI)

3. **📊 Estatística Descritiva**
   - Contagem de frequências de cada número
   - Análise de atrasos (sorteios desde última aparição)
   - Criação de histogramas e gráficos de visualização
   - Análise de padrões (números consecutivos, somas, dispersão)
   - Correlações entre números

4. **🧬 Teoria Probabilística Avançada**
   - Simulações Monte Carlo para teste de hipóteses
   - Testes de uniformidade de distribuição
   - Testes de aleatoriedade (runs, autocorrelação, gaps)
   - Modelagem estocástica
   - Geração de previsões baseadas em múltiplas estratégias

## 🚀 Como Usar

### Instalação

1. **Clone ou baixe o projeto**
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Execução

#### Aplicativo Principal (Interface Interativa)
```bash
python main.py
```

#### Demonstração de Funcionalidades
```bash
python demo.py
```

#### Módulos Individuais
```bash
# Teste do coletor de dados
python src/data_collector.py

# Teste da análise probabilística
python src/probability_analyzer.py

# Teste da análise avançada
python src/advanced_analytics.py
```

## 📱 Menu do Aplicativo Principal

```
📊 MENU PRINCIPAL:
1. 📥 Atualizar dados históricos
2. 📈 Análise de probabilidades
3. 📊 Estatísticas descritivas
4. 🎯 Análise probabilística avançada
5. 🔮 Gerar previsões
6. 📋 Relatório completo
7. ℹ️  Informações dos dados
0. 🚪 Sair
```

## 🔍 Detalhes das Análises

### 1. Análise de Probabilidades
- **Probabilidades básicas:** Chance de acerto da sena (1 em 50.063.860)
- **Análise por número:** Frequência teórica vs empírica de cada número
- **Estratégias:** Comparação de diferentes abordagens de jogo
- **Par/Ímpar:** Distribuições mais prováveis
- **Investimento:** Análise de ROI para diferentes quantidades de jogos

### 2. Estatísticas Descritivas
- **Frequências:** Números mais e menos sorteados
- **Atrasos:** Tempo desde última aparição de cada número
- **Padrões:** Análise de sequências, somas e dispersões
- **Gráficos:** Histogramas, correlações e visualizações

### 3. Análise Avançada
- **Monte Carlo:** Simulações de milhares de jogos
- **Testes de Aleatoriedade:** Verificação se os sorteios são realmente aleatórios
- **Uniformidade:** Teste se todos os números têm chance igual
- **Previsões:** Geração de jogos baseados em diferentes estratégias

### 4. Estratégias de Previsão
- **Aleatório Ponderado:** Baseado em frequências históricas
- **Números Quentes:** Mais frequentes nos últimos sorteios
- **Números Frios:** Com maior atraso
- **Balanceado:** Combinação de múltiplas estratégias

## 📁 Estrutura do Projeto

```
megasena/
├── src/
│   ├── data_collector.py      # Coleta de dados da Caixa
│   ├── probability_analyzer.py # Análise probabilística
│   ├── descriptive_stats.py   # Estatísticas descritivas
│   └── advanced_analytics.py  # Análise avançada e Monte Carlo
├── data/
│   ├── megasena_historical.json # Dados históricos (JSON)
│   ├── megasena_historical.csv  # Dados históricos (CSV)
│   └── plots/                   # Gráficos gerados
├── main.py                     # Interface principal
├── demo.py                     # Demonstração
├── requirements.txt            # Dependências
└── README.md                   # Este arquivo
```

## 📊 Exemplos de Saída

### Análise de Probabilidades
```
🎯 Total de combinações possíveis: 50,063,860
   Probabilidade de acertar: 1 em 50,063,860
   Probabilidade percentual: 0.0000019974%

🔥 5 números mais frequentes:
   1. Número 10: 285 vezes (1.68%)
   2. Número 05: 283 vezes (1.67%)
   3. Número 33: 281 vezes (1.66%)
```

### Simulação Monte Carlo
```
🎲 Simulações executadas: 100,000
   Melhor resultado: 5 acertos
   Média de acertos: 0.998
   Tempo de execução: 2.45s

📊 Distribuição de acertos:
   0 acertos: 43,596 vezes (43.60%)
   1 acertos: 41,347 vezes (41.35%)
   2 acertos: 13,237 vezes (13.24%)
   3 acertos: 1,732 vezes (1.73%)
   4 acertos: 88 vezes (0.09%)
   5 acertos: 0 vezes (0.00%)
   6 acertos: 0 vezes (0.00%)
```

### Previsões Geradas
```
🔮 PREVISÕES - MÉTODO: Balanceado
   🎫 Jogo 1: 07 - 14 - 25 - 32 - 41 - 58
   🎫 Jogo 2: 03 - 18 - 29 - 36 - 45 - 52
   🎫 Jogo 3: 11 - 22 - 31 - 38 - 47 - 59
```

## ⚠️ Aviso Importante

**Este aplicativo é para fins educacionais e de estudo estatístico.**

- Os jogos de loteria são baseados em sorteios aleatórios
- Análises históricas não garantem resultados futuros
- Jogue com responsabilidade
- Este software não incentiva apostas excessivas

## 🛠️ Dependências

- `requests` - Para coleta de dados da API da Caixa
- `pandas` - Manipulação e análise de dados
- `numpy` - Cálculos numéricos e estatísticos
- `matplotlib` - Criação de gráficos
- `seaborn` - Visualizações estatísticas avançadas
- `scipy` - Funções científicas e estatísticas
- `beautifulsoup4` - Parsing HTML (backup)
- `plotly` - Gráficos interativos
- `colorama` - Cores no terminal

## 🎓 Conceitos Implementados

### Probabilidade
- Combinações matemáticas C(n,r)
- Probabilidades condicionais
- Distribuições uniformes
- Análise de viés estatístico

### Estatística Descritiva
- Medidas de tendência central
- Medidas de dispersão
- Análise de frequências
- Correlações

### Teoria Probabilística Avançada
- Simulação Monte Carlo
- Testes de hipóteses
- Modelagem estocástica
- Geradores pseudoaleatórios

## 📈 Resultados e Insights

O aplicativo permite descobrir:
- Quais números são mais/menos frequentes
- Padrões temporais nos sorteios
- Eficácia de diferentes estratégias
- Comportamento estatístico dos sorteios
- Análise de aleatoriedade dos resultados

## 🤝 Contribuições

Contribuições são bem-vindas! Áreas para melhoria:
- Novos tipos de análise estatística
- Interfaces gráficas mais avançadas
- Análises de outras loterias
- Otimizações de performance
- Testes unitários

## 📄 Licença

Este projeto é de código aberto para fins educacionais.

---

**Desenvolvido com Python 🐍 para análise estatística da Mega Sena 🎰**