"""
Módulo de análise probabilística da Mega Sena.
Calcula probabilidades específicas, repetições e estratégias.

MIT License - Copyright (c) 2025 delcain
Veja LICENSE para detalhes completos.
"""

import math
from itertools import combinations
from collections import Counter
from typing import List, Dict, Tuple, Set
import numpy as np


class MegaSenaProbabilityAnalyzer:
    """Analisador de probabilidades da Mega Sena."""
    
    def __init__(self):
        self.total_numbers = 60  # Números de 1 a 60
        self.numbers_per_draw = 6  # 6 números por sorteio
        self.cost_per_game = 6.0  # Valor padrão do jogo em reais
        
    def factorial(self, n: int) -> int:
        """Calcula fatorial de n."""
        return math.factorial(n)
    
    def combination(self, n: int, r: int) -> int:
        """Calcula combinação C(n,r) = n! / (r! * (n-r)!)."""
        return math.comb(n, r)
    
    def total_combinations(self) -> int:
        """Calcula total de combinações possíveis na Mega Sena."""
        return self.combination(self.total_numbers, self.numbers_per_draw)
    
    def probability_specific_combination(self) -> float:
        """Probabilidade de uma combinação específica ser sorteada."""
        total = self.total_combinations()
        return 1.0 / total
    
    def probability_specific_number(self, historical_data: List[List[int]] = None) -> Dict:
        """
        Calcula probabilidade de um número específico sair.
        
        Args:
            historical_data: Lista de sorteios históricos (opcional)
        
        Returns:
            Dict com probabilidades teóricas e empíricas
        """
        # Probabilidade teórica (cada número tem chance igual)
        theoretical_prob = self.numbers_per_draw / self.total_numbers
        
        result = {
            'probabilidade_teorica': theoretical_prob,
            'probabilidade_teorica_percent': theoretical_prob * 100
        }
        
        # Se há dados históricos, calcular probabilidade empírica
        if historical_data:
            all_numbers = [num for draw in historical_data for num in draw]
            total_draws = len(historical_data)
            number_counts = Counter(all_numbers)
            
            empirical_probs = {}
            for num in range(1, self.total_numbers + 1):
                count = number_counts.get(num, 0)
                empirical_prob = count / (total_draws * self.numbers_per_draw)
                empirical_probs[num] = {
                    'frequencia': count,
                    'probabilidade_empirica': empirical_prob,
                    'probabilidade_empirica_percent': empirical_prob * 100,
                    'diferenca_teorica': empirical_prob - theoretical_prob
                }
            
            result['probabilidades_por_numero'] = empirical_probs
            result['total_sorteios_analisados'] = total_draws
        
        return result
    
    def probability_number_ranges(self, historical_data: List[List[int]] = None) -> Dict:
        """Analisa probabilidades por faixas de números."""
        ranges = {
            'baixos': (1, 30),
            'altos': (31, 60),
            'primeira_dezena': (1, 10),
            'segunda_dezena': (11, 20),
            'terceira_dezena': (21, 30),
            'quarta_dezena': (31, 40),
            'quinta_dezena': (41, 50),
            'sexta_dezena': (51, 60)
        }
        
        result = {}
        
        # Probabilidades teóricas
        for range_name, (start, end) in ranges.items():
            numbers_in_range = end - start + 1
            # Probabilidade de pelo menos um número da faixa ser sorteado
            prob_none = self.combination(self.total_numbers - numbers_in_range, self.numbers_per_draw) / self.total_combinations()
            prob_at_least_one = 1 - prob_none
            
            result[range_name] = {
                'faixa': f"{start}-{end}",
                'numeros_na_faixa': numbers_in_range,
                'prob_pelo_menos_um': prob_at_least_one,
                'prob_pelo_menos_um_percent': prob_at_least_one * 100
            }
        
        # Se há dados históricos, calcular frequências empíricas
        if historical_data:
            for range_name, (start, end) in ranges.items():
                count_with_range = 0
                total_in_range = 0
                
                for draw in historical_data:
                    numbers_in_range = [n for n in draw if start <= n <= end]
                    if numbers_in_range:
                        count_with_range += 1
                    total_in_range += len(numbers_in_range)
                
                empirical_prob = count_with_range / len(historical_data)
                avg_numbers_per_draw = total_in_range / len(historical_data)
                
                result[range_name].update({
                    'freq_empirica_pelo_menos_um': empirical_prob,
                    'freq_empirica_percent': empirical_prob * 100,
                    'media_numeros_por_sorteio': avg_numbers_per_draw,
                    'total_ocorrencias': total_in_range
                })
        
        return result
    
    def probability_even_odd(self, historical_data: List[List[int]] = None) -> Dict:
        """Analisa probabilidades de números pares e ímpares."""
        even_numbers = 30  # 2, 4, 6, ..., 60
        odd_numbers = 30   # 1, 3, 5, ..., 59
        
        result = {}
        
        # Calcular probabilidades para diferentes distribuições
        for even_count in range(7):  # 0 a 6 números pares
            odd_count = 6 - even_count
            
            if odd_count <= odd_numbers and even_count <= even_numbers:
                prob = (self.combination(even_numbers, even_count) * 
                       self.combination(odd_numbers, odd_count)) / self.total_combinations()
                
                result[f"{even_count}_pares_{odd_count}_impares"] = {
                    'pares': even_count,
                    'impares': odd_count,
                    'probabilidade': prob,
                    'probabilidade_percent': prob * 100
                }
        
        # Se há dados históricos, calcular distribuições empíricas
        if historical_data:
            distribution_counts = Counter()
            
            for draw in historical_data:
                even_count = sum(1 for n in draw if n % 2 == 0)
                odd_count = 6 - even_count
                distribution_counts[f"{even_count}_pares_{odd_count}_impares"] += 1
            
            total_draws = len(historical_data)
            for distribution, count in distribution_counts.items():
                if distribution in result:
                    empirical_prob = count / total_draws
                    result[distribution].update({
                        'freq_empirica': empirical_prob,
                        'freq_empirica_percent': empirical_prob * 100,
                        'ocorrencias': count
                    })
        
        return result
    
    def set_cost_per_game(self, cost: float):
        """Define o valor do jogo da Mega Sena."""
        if cost > 0:
            self.cost_per_game = cost
        else:
            raise ValueError("O valor do jogo deve ser maior que zero")
    
    def get_cost_per_game(self) -> float:
        """Retorna o valor atual do jogo."""
        return self.cost_per_game
    
    def analyze_repetitions(self, historical_data: List[List[int]]) -> Dict:
        """Analisa padrões de repetição entre sorteios."""
        if len(historical_data) < 2:
            return {"erro": "Dados insuficientes para análise de repetições"}
        
        repetition_stats = {
            'repeticoes_consecutivas': [],
            'repeticoes_por_intervalo': {},
            'numeros_mais_repetidos': Counter(),
            'sequencias_repetidas': Counter()
        }
        
        # Analisar repetições consecutivas
        for i in range(len(historical_data) - 1):
            current_draw = set(historical_data[i])
            next_draw = set(historical_data[i + 1])
            repeated = current_draw.intersection(next_draw)
            repetition_stats['repeticoes_consecutivas'].append(len(repeated))
            
            for num in repeated:
                repetition_stats['numeros_mais_repetidos'][num] += 1
        
        # Analisar repetições por intervalo (2, 3, 5, 10 sorteios)
        intervals = [2, 3, 5, 10]
        for interval in intervals:
            repetitions = []
            for i in range(len(historical_data) - interval):
                current_draw = set(historical_data[i])
                future_draw = set(historical_data[i + interval])
                repeated = current_draw.intersection(future_draw)
                repetitions.append(len(repeated))
            
            repetition_stats['repeticoes_por_intervalo'][f'intervalo_{interval}'] = {
                'media_repeticoes': np.mean(repetitions) if repetitions else 0,
                'max_repeticoes': max(repetitions) if repetitions else 0,
                'min_repeticoes': min(repetitions) if repetitions else 0,
                'distribuicao': Counter(repetitions)
            }
        
        # Analisar sequências completas repetidas
        for i, draw in enumerate(historical_data):
            draw_tuple = tuple(sorted(draw))
            repetition_stats['sequencias_repetidas'][draw_tuple] += 1
        
        # Estatísticas gerais
        repetition_stats['estatisticas_gerais'] = {
            'media_repeticoes_consecutivas': np.mean(repetition_stats['repeticoes_consecutivas']),
            'max_repeticoes_consecutivas': max(repetition_stats['repeticoes_consecutivas']),
            'sequencias_unicas': len(repetition_stats['sequencias_repetidas']),
            'sequencias_repetidas_completas': sum(1 for count in repetition_stats['sequencias_repetidas'].values() if count > 1)
        }
        
        return repetition_stats
    
    def compare_strategies(self, historical_data: List[List[int]]) -> Dict:
        """Compara diferentes estratégias de jogo."""
        if not historical_data:
            return {"erro": "Dados históricos necessários"}
        
        strategies = {}
        
        # Estratégia 1: Números mais frequentes
        all_numbers = [num for draw in historical_data for num in draw]
        number_counts = Counter(all_numbers)
        most_frequent = [num for num, count in number_counts.most_common(6)]
        
        # Estratégia 2: Números menos frequentes
        least_frequent = [num for num, count in number_counts.most_common()[-6:]]
        
        # Estratégia 3: Mistura balanceada (3 pares + 3 ímpares)
        even_numbers = [n for n in range(2, 61, 2)]
        odd_numbers = [n for n in range(1, 61, 2)]
        balanced_mix = sorted(even_numbers[:3] + odd_numbers[:3])
        
        # Estratégia 4: Distribuição por dezenas
        dezenas_strategy = [5, 15, 25, 35, 45, 55]  # Uma de cada dezena
        
        # Estratégia 5: Números primos
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
        primes_strategy = primes[:6]
        
        strategies_to_test = {
            'mais_frequentes': most_frequent,
            'menos_frequentes': least_frequent,
            'balanceada_par_impar': balanced_mix,
            'uma_por_dezena': dezenas_strategy,
            'numeros_primos': primes_strategy
        }
        
        # Simular performance de cada estratégia
        for strategy_name, numbers in strategies_to_test.items():
            hits = []
            for draw in historical_data:
                matching = len(set(numbers).intersection(set(draw)))
                hits.append(matching)
            
            strategies[strategy_name] = {
                'numeros': numbers,
                'media_acertos': np.mean(hits),
                'max_acertos': max(hits),
                'distribuicao_acertos': Counter(hits),
                'acertos_4_ou_mais': sum(1 for h in hits if h >= 4),
                'taxa_sucesso_4_plus': sum(1 for h in hits if h >= 4) / len(hits) * 100
            }
        
        return strategies
    
    def calculate_investment_analysis(self, num_games: int, cost_per_game: float = None) -> Dict:
        """Analisa retorno de investimento baseado em probabilidades."""
        # Usar o valor configurado se não foi fornecido um específico
        if cost_per_game is None:
            cost_per_game = self.cost_per_game
            
        total_cost = num_games * cost_per_game
        total_combinations = self.total_combinations()
        
        # Probabilidades de acerto
        prob_sena = 1 / total_combinations
        prob_quina = self.combination(6, 5) * self.combination(54, 1) / total_combinations
        prob_quadra = self.combination(6, 4) * self.combination(54, 2) / total_combinations
        
        # Valores médios de prêmios (estimativas baseadas em dados históricos)
        premio_sena_medio = 30000000  # 30 milhões (estimativa)
        premio_quina_medio = 50000    # 50 mil (estimativa)
        premio_quadra_medio = 1000    # 1 mil (estimativa)
        
        # Análise de retorno esperado
        expected_return_sena = num_games * prob_sena * premio_sena_medio
        expected_return_quina = num_games * prob_quina * premio_quina_medio
        expected_return_quadra = num_games * prob_quadra * premio_quadra_medio
        
        total_expected_return = expected_return_sena + expected_return_quina + expected_return_quadra
        
        return {
            'investimento_total': total_cost,
            'numero_jogos': num_games,
            'custo_por_jogo': cost_per_game,
            'probabilidades': {
                'sena': prob_sena,
                'sena_percent': prob_sena * 100,
                'quina': prob_quina,
                'quina_percent': prob_quina * 100,
                'quadra': prob_quadra,
                'quadra_percent': prob_quadra * 100
            },
            'retorno_esperado': {
                'sena': expected_return_sena,
                'quina': expected_return_quina,
                'quadra': expected_return_quadra,
                'total': total_expected_return
            },
            'analise_roi': {
                'retorno_esperado_total': total_expected_return,
                'roi_percent': (total_expected_return - total_cost) / total_cost * 100,
                'break_even_probability': total_cost / premio_sena_medio,
                'jogos_para_sena_esperada': 1 / prob_sena
            }
        }


def main():
    """Função principal para teste do módulo."""
    analyzer = MegaSenaProbabilityAnalyzer()
    
    print("=== ANÁLISE PROBABILÍSTICA DA MEGA SENA ===")
    
    print(f"\n1. Total de combinações possíveis: {analyzer.total_combinations():,}")
    print(f"   Probabilidade de acertar: 1 em {analyzer.total_combinations():,}")
    print(f"   Probabilidade percentual: {analyzer.probability_specific_combination() * 100:.10f}%")
    
    print("\n2. Probabilidade por número:")
    prob_info = analyzer.probability_specific_number()
    print(f"   Probabilidade teórica: {prob_info['probabilidade_teorica']:.4f} ({prob_info['probabilidade_teorica_percent']:.2f}%)")
    
    print("\n3. Análise de faixas de números:")
    ranges = analyzer.probability_number_ranges()
    for range_name, info in ranges.items():
        print(f"   {range_name}: {info['prob_pelo_menos_um_percent']:.2f}% de chance")
    
    print("\n4. Distribuição par/ímpar:")
    even_odd = analyzer.probability_even_odd()
    for dist, info in even_odd.items():
        print(f"   {dist}: {info['probabilidade_percent']:.2f}%")
    
    print("\n5. Análise de investimento (100 jogos):")
    investment = analyzer.calculate_investment_analysis(100)
    print(f"   Investimento: R$ {investment['investimento_total']:.2f}")
    print(f"   Retorno esperado: R$ {investment['retorno_esperado']['total']:.2f}")
    print(f"   ROI esperado: {investment['analise_roi']['roi_percent']:.2f}%")


if __name__ == "__main__":
    main()