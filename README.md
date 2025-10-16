# 🎰 Mega Sena - Análise Probabilística Avançada

Aplicativo Python completo para análise estatística e probabilística dos dados históricos da Mega Sena.

## ✨ Funcionalidades

### 📥 Coleta de Dados
- ✅ Obtém dados históricos da fonte oficial da Caixa
- ✅ Atualização automática com verificação de novos sorteios
- ✅ Salvamento em JSON e CSV

### 🎲 Análise Probabilística
- ✅ Cálculo de probabilidades específicas
- ✅ Análise de estratégias (pares/ímpares, faixas)
- ✅ Estimativa de chances de repetições
- ✅ Análise de ROI para investimentos

### 📊 Estatística Descritiva
- ✅ Análise de frequências de números
- ✅ Cálculo de atrasos (tempo desde última aparição)
- ✅ Criação de histogramas e gráficos
- ✅ Análise de padrões e correlações

### 🧬 Análise Avançada
- ✅ Simulações Monte Carlo
- ✅ Testes de uniformidade e aleatoriedade
- ✅ Modelagem estocástica
- ✅ Geração de previsões baseadas em múltiplas estratégias

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.7+
- pip (gerenciador de pacotes Python)

### Instalação
```bash
# 1. Clone ou baixe o projeto
git clone https://github.com/delcain/MegaSena
cd megasena

# 2. Instale as dependências
pip install -r requirements.txt
```

### Execução
```bash
# Interface principal interativa
python main.py

# Demonstração de todas as funcionalidades
python demo.py
```

## 📱 Interface do Aplicativo

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

## 🔍 Exemplos de Análises

### Probabilidades Básicas
- Total de combinações possíveis: **50.063.860**
- Probabilidade de acerto: **1 em 50.063.860** (0.000002%)

### Simulação Monte Carlo
- Executa milhares de simulações
- Compara estratégias diferentes
- Calcula distribuições de acertos
- Tempo de execução otimizado

### Estatísticas dos Números
- Números mais/menos frequentes
- Análise de atrasos atuais
- Padrões de aparição
- Correlações entre números

### Previsões Inteligentes
- **Aleatório Ponderado**: Baseado em frequências históricas
- **Números Quentes**: Mais frequentes recentemente  
- **Números Frios**: Com maior atraso
- **Balanceado**: Combinação de estratégias

## 📁 Estrutura do Projeto

```
megasena/
├── src/
│   ├── data_collector.py      # Coleta de dados
│   ├── probability_analyzer.py # Análise probabilística
│   ├── descriptive_stats.py   # Estatísticas descritivas
│   └── advanced_analytics.py  # Análise avançada
├── data/                      # Dados e gráficos
├── main.py                    # Interface principal
├── demo.py                    # Demonstração
└── requirements.txt           # Dependências
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**: Linguagem principal
- **Pandas**: Manipulação de dados
- **NumPy**: Cálculos numéricos  
- **Matplotlib/Seaborn**: Visualizações
- **Requests**: Coleta de dados da API
- **SciPy**: Análises estatísticas avançadas

## 📊 Conceitos Matemáticos Implementados

### Probabilidade
- Combinações C(n,r) = n! / (r! × (n-r)!)
- Probabilidades condicionais
- Distribuições uniformes
- Análise de viés estatístico

### Estatística
- Medidas de tendência central (média, mediana, moda)
- Medidas de dispersão (desvio padrão, variância)
- Testes de hipóteses
- Análise de correlação

### Modelagem Avançada
- Simulações Monte Carlo
- Testes de aleatoriedade
- Modelagem estocástica
- Análise de séries temporais

## ⚠️ Aviso Legal

**Este aplicativo é para fins educacionais e de estudo estatístico.**

- Jogos de loteria são baseados em sorteios aleatórios
- Análises históricas não garantem resultados futuros  
- Jogue com responsabilidade
- O software não incentiva apostas excessivas

## 🎓 Valor Educacional

Este projeto demonstra aplicações práticas de:
- Estatística e probabilidade
- Programação orientada a objetos
- Análise de dados com Python
- Visualização de informações
- APIs e coleta de dados
- Simulações computacionais

## 📈 Resultados Esperados

Após usar o aplicativo, você será capaz de:
- Entender as probabilidades reais da Mega Sena
- Analisar padrões estatísticos nos sorteios
- Comparar eficácia de diferentes estratégias
- Gerar previsões baseadas em dados históricos
- Compreender conceitos de aleatoriedade e uniformidade

## 🤝 Contribuições

Contribuições são bem-vindas! Áreas para melhoria:
- Análises estatísticas adicionais
- Interface gráfica (GUI)
- Suporte a outras loterias
- Otimizações de performance
- Testes automatizados

## 📞 Suporte

Para dúvidas sobre o código ou funcionalidades:
1. Consulte o `MANUAL_DO_USUARIO.md`
2. Execute `python demo.py` para ver exemplos
3. Verifique os comentários no código fonte

---

**Desenvolvido para demonstrar o poder da análise estatística aplicada a jogos de loteria 📊🎲**