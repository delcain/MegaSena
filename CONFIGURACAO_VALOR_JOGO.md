# 💰 Nova Funcionalidade: Configuração do Valor do Jogo

## ✅ **Implementação Concluída**

### 🎯 **O que foi adicionado:**

#### **1. No arquivo `probability_analyzer.py`:**

- **Atributo `cost_per_game`**: Armazena o valor atual do jogo (padrão: R$ 6,00)
- **Método `set_cost_per_game(cost)`**: Define um novo valor para o jogo
- **Método `get_cost_per_game()`**: Retorna o valor atual configurado
- **Atualização do `calculate_investment_analysis()`**: Usa o valor configurado por padrão

#### **2. No arquivo `main.py`:**

- **Nova opção no menu**: "8. 💰 Configurar valor do jogo"
- **Função `configure_game_cost()`**: Interface interativa para configurar o valor
- **Atualização da análise de probabilidades**: Mostra o valor atual configurado

### 🚀 **Como usar:**

#### **1. Pelo Menu Principal:**
```bash
python main.py
# → Escolha opção 8: 💰 Configurar valor do jogo
# → Digite o novo valor (ex: 7.50)
# → Sistema atualiza automaticamente
```

#### **2. Programaticamente:**
```python
from src.probability_analyzer import MegaSenaProbabilityAnalyzer

analyzer = MegaSenaProbabilityAnalyzer()

# Configurar novo valor
analyzer.set_cost_per_game(7.50)

# Verificar valor atual
valor_atual = analyzer.get_cost_per_game()
print(f"Valor atual: R$ {valor_atual:.2f}")

# Análise usa o valor configurado automaticamente
investment = analyzer.calculate_investment_analysis(100)
```

### 📊 **Funcionalidades da Interface:**

#### **Configuração do Valor:**
- ✅ Mostra valor atual
- ✅ Solicita novo valor
- ✅ Validação de entrada (números positivos)
- ✅ Opção de manter valor atual (ENTER)
- ✅ Cálculo automático de impacto (% de mudança)
- ✅ Exemplo de investimento com novo valor

#### **Exemplo de Uso na Interface:**
```
💰 CONFIGURAÇÃO DO VALOR DO JOGO
================================

💰 Valor atual do jogo: R$ 6.00

💸 Digite o novo valor do jogo (ou ENTER para manter atual): R$ 7.50
✅ Valor do jogo atualizado para: R$ 7.50

📊 IMPACTO DA MUDANÇA:
   💰 Valor anterior: R$ 6.00
   💰 Valor atual: R$ 7.50
   📈 Aumento: 25.0%

💡 EXEMPLO (100 jogos):
   💸 Investimento total: R$ 750.00
   🎯 Retorno esperado: R$ 135.16
   📊 ROI esperado: -81.98%
```

### 🔧 **Detalhes Técnicos:**

#### **Valor Padrão:**
- **R$ 6,00** (valor atual da Mega Sena em 2024)
- Configurável a qualquer momento
- Persiste durante a sessão

#### **Validações:**
- ✅ Valor deve ser maior que zero
- ✅ Aceita formato com vírgula (7,50) ou ponto (7.50)
- ✅ Trata erros de entrada graciosamente

#### **Integração:**
- ✅ **Análise de Probabilidades**: Mostra valor atual e usa para cálculos
- ✅ **Análise de Investimento**: Usa valor configurado automaticamente
- ✅ **Relatórios**: Incluem o valor configurado nos cálculos

### 📈 **Impacto nos Cálculos:**

#### **Exemplo com Diferentes Valores:**

| Valor do Jogo | 100 Jogos | 1000 Jogos | ROI Esperado |
|---------------|-----------|------------|--------------|
| R$ 5,00       | R$ 500    | R$ 5.000   | -72.7%       |
| R$ 6,00       | R$ 600    | R$ 6.000   | -77.5%       |
| R$ 7,50       | R$ 750    | R$ 7.500   | -81.9%       |
| R$ 10,00      | R$ 1.000  | R$ 10.000  | -86.5%       |

### 🎯 **Casos de Uso:**

1. **Atualização de Preços**: Quando a Caixa altera o valor do jogo
2. **Análise Histórica**: Simular com valores antigos
3. **Comparação**: Avaliar impacto de mudanças de preço
4. **Planejamento**: Calcular investimentos com diferentes cenários

### ✅ **Status da Implementação:**

- ✅ **Armazenamento do valor**: Implementado
- ✅ **Interface de configuração**: Implementado  
- ✅ **Validação de entrada**: Implementado
- ✅ **Integração com análises**: Implementado
- ✅ **Cálculo de impacto**: Implementado
- ✅ **Exemplo de investimento**: Implementado
- ✅ **Testes funcionais**: Implementado

---

**A funcionalidade está 100% implementada e testada!** 🎰💰✨

O usuário agora pode:
1. Configurar o valor atual do jogo da Mega Sena
2. Ver o impacto imediato nas análises
3. Comparar cenários com diferentes valores
4. Obter cálculos precisos de investimento