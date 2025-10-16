"""
Módulo de teoria probabilística avançada para Mega Sena.
Implementa simulações Monte Carlo, análises de distribuições e modelagem estocástica.
"""

import random
import numpy as np
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional
import math
from itertools import combinations
import time


class MegaSenaAdvancedAnalytics:
    """Análises probabilísticas avançadas para Mega Sena."""
    
    def __init__(self, seed: Optional[int] = None):
        if seed:
            random.seed(seed)
            np.random.seed(seed)
    
    def monte_carlo_simulation(self, 
                             num_simulations: int = 100000,
                             strategy: str = "random",
                             custom_numbers: List[int] = None) -> Dict:
        """
        Executa simulação Monte Carlo para diferentes estratégias.
        
        Args:
            num_simulations: Número de simulações a executar
            strategy: Estratégia a simular ('random', 'custom', 'most_frequent', etc.)
            custom_numbers: Números específicos para estratégia 'custom'
        """
        print(f"Iniciando simulação Monte Carlo com {num_simulations:,} iterações...")
        start_time = time.time()
        
        results = {
            'simulacoes_executadas': num_simulations,
            'estrategia': strategy,
            'resultados_por_acerto': Counter(),
            'melhor_resultado': 0,
            'historico_melhores': [],
            'distribuicao_acertos': [],
            'numeros_mais_sorteados': Counter(),
            'tempo_execucao': 0
        }
        
        # Definir números baseados na estratégia
        if strategy == "custom" and custom_numbers:
            player_numbers = custom_numbers[:6]
        elif strategy == "most_frequent":
            # Simular números mais frequentes (baseado em padrão típico)
            player_numbers = [4, 5, 10, 23, 33, 42]
        elif strategy == "least_frequent":
            # Simular números menos frequentes
            player_numbers = [13, 22, 28, 36, 47, 59]
        elif strategy == "balanced":
            # Estratégia balanceada (pares/ímpares, distribuição)
            player_numbers = [7, 14, 25, 32, 41, 58]
        else:  # random
            player_numbers = None
        
        # Executar simulações
        for i in range(num_simulations):
            if i % 10000 == 0 and i > 0:
                progress = (i / num_simulations) * 100
                print(f"Progresso: {progress:.1f}%")
            
            # Gerar sorteio simulado
            winning_numbers = sorted(random.sample(range(1, 61), 6))
            
            # Gerar jogo do jogador
            if player_numbers is None:
                # Estratégia aleatória
                player_draw = sorted(random.sample(range(1, 61), 6))
            else:
                player_draw = player_numbers
            
            # Contar acertos
            matches = len(set(winning_numbers).intersection(set(player_draw)))
            results['resultados_por_acerto'][matches] += 1
            results['distribuicao_acertos'].append(matches)
            
            # Atualizar melhor resultado
            if matches > results['melhor_resultado']:
                results['melhor_resultado'] = matches
                results['historico_melhores'].append((i, matches, winning_numbers.copy()))
            
            # Contar números sorteados
            for num in winning_numbers:
                results['numeros_mais_sorteados'][num] += 1
        
        end_time = time.time()
        results['tempo_execucao'] = end_time - start_time
        
        # Calcular estatísticas
        results['estatisticas'] = self._calculate_simulation_stats(results)
        
        print(f"Simulação concluída em {results['tempo_execucao']:.2f} segundos")
        return results
    
    def _calculate_simulation_stats(self, results: Dict) -> Dict:
        """Calcula estatísticas da simulação Monte Carlo."""
        total_sims = results['simulacoes_executadas']
        acertos = results['distribuicao_acertos']
        
        stats = {
            'media_acertos': np.mean(acertos),
            'desvio_padrao_acertos': np.std(acertos),
            'mediana_acertos': np.median(acertos),
            'moda_acertos': Counter(acertos).most_common(1)[0][0],
            'percentis': {
                '25': np.percentile(acertos, 25),
                '50': np.percentile(acertos, 50),
                '75': np.percentile(acertos, 75),
                '90': np.percentile(acertos, 90),
                '95': np.percentile(acertos, 95)
            },
            'probabilidades_observadas': {},
            'probabilidades_teoricas': {}
        }
        
        # Calcular probabilidades observadas vs teóricas
        for acertos_num in range(7):
            observed_prob = results['resultados_por_acerto'][acertos_num] / total_sims
            theoretical_prob = self._theoretical_probability(acertos_num)
            
            stats['probabilidades_observadas'][acertos_num] = observed_prob
            stats['probabilidades_teoricas'][acertos_num] = theoretical_prob
        
        return stats
    
    def _theoretical_probability(self, matches: int) -> float:
        """Calcula probabilidade teórica de acertar exatamente 'matches' números."""
        if matches > 6:
            return 0.0
        
        # C(6, matches) * C(54, 6-matches) / C(60, 6)
        numerator = math.comb(6, matches) * math.comb(54, 6 - matches)
        denominator = math.comb(60, 6)
        
        return numerator / denominator
    
    def uniform_distribution_test(self, historical_data: List[List[int]]) -> Dict:
        """Testa se os sorteios seguem distribuição uniforme."""
        if not historical_data:
            return {"erro": "Dados históricos necessários"}
        
        # Contar frequências
        all_numbers = [num for draw in historical_data for num in draw]
        frequency_counter = Counter(all_numbers)
        
        # Estatísticas observadas
        observed_frequencies = [frequency_counter.get(i, 0) for i in range(1, 61)]
        expected_frequency = len(all_numbers) / 60
        
        # Teste Qui-quadrado
        chi_square = sum((obs - expected_frequency) ** 2 / expected_frequency 
                        for obs in observed_frequencies)
        
        # Graus de liberdade
        degrees_freedom = 59  # 60 números - 1
        
        # Coeficiente de variação
        cv = np.std(observed_frequencies) / np.mean(observed_frequencies)
        
        # Teste de Kolmogorov-Smirnov (simplificado)
        sorted_freqs = sorted(observed_frequencies)
        expected_uniform = [expected_frequency] * 60
        ks_statistic = max(abs(obs - exp) for obs, exp in zip(sorted_freqs, sorted(expected_uniform)))
        
        return {
            'teste_uniformidade': {
                'chi_quadrado': chi_square,
                'graus_liberdade': degrees_freedom,
                'coef_variacao': cv,
                'ks_estatistica': ks_statistic,
                'frequencia_esperada': expected_frequency,
                'frequencia_min': min(observed_frequencies),
                'frequencia_max': max(observed_frequencies),
                'desvio_padrao': np.std(observed_frequencies),
                'amplitude': max(observed_frequencies) - min(observed_frequencies)
            },
            'interpretacao': self._interpret_uniformity_test(chi_square, cv, ks_statistic),
            'frequencias_observadas': dict(enumerate(observed_frequencies, 1))
        }
    
    def _interpret_uniformity_test(self, chi_square: float, cv: float, ks_stat: float) -> Dict:
        """Interpreta resultados do teste de uniformidade."""
        # Valores críticos aproximados (para orientação)
        chi_critical_95 = 77.93  # Para 59 graus de liberdade, α=0.05
        cv_threshold = 0.1  # Coeficiente de variação baixo indica uniformidade
        
        interpretation = {
            'uniformidade_chi2': chi_square < chi_critical_95,
            'uniformidade_cv': cv < cv_threshold,
            'nivel_uniformidade': 'alta' if cv < 0.05 else 'média' if cv < 0.15 else 'baixa',
            'conclusao': ''
        }
        
        if interpretation['uniformidade_chi2'] and interpretation['uniformidade_cv']:
            interpretation['conclusao'] = "Os dados sugerem distribuição uniforme"
        elif interpretation['uniformidade_chi2'] or interpretation['uniformidade_cv']:
            interpretation['conclusao'] = "Os dados apresentam uniformidade moderada"
        else:
            interpretation['conclusao'] = "Os dados não apresentam distribuição uniforme"
        
        return interpretation
    
    def randomness_tests(self, historical_data: List[List[int]]) -> Dict:
        """Executa testes de aleatoriedade nos sorteios."""
        if not historical_data:
            return {"erro": "Dados históricos necessários"}
        
        tests = {
            'teste_runs': self._runs_test(historical_data),
            'teste_autocorrelacao': self._autocorrelation_test(historical_data),
            'teste_gaps': self._gaps_test(historical_data),
            'teste_poker': self._poker_test(historical_data)
        }
        
        return tests
    
    def _runs_test(self, historical_data: List[List[int]]) -> Dict:
        """Teste de runs para verificar aleatoriedade."""
        # Converter sorteios em sequência binária baseada na mediana
        all_numbers = [num for draw in historical_data for num in draw]
        median = np.median(all_numbers)
        
        binary_sequence = [1 if num > median else 0 for num in all_numbers]
        
        # Contar runs
        runs = 1
        for i in range(1, len(binary_sequence)):
            if binary_sequence[i] != binary_sequence[i-1]:
                runs += 1
        
        n1 = sum(binary_sequence)  # Número de 1s
        n0 = len(binary_sequence) - n1  # Número de 0s
        
        # Estatística esperada para sequência aleatória
        expected_runs = (2 * n0 * n1) / (n0 + n1) + 1
        variance_runs = (2 * n0 * n1 * (2 * n0 * n1 - n0 - n1)) / ((n0 + n1) ** 2 * (n0 + n1 - 1))
        
        # Z-score
        z_score = (runs - expected_runs) / math.sqrt(variance_runs) if variance_runs > 0 else 0
        
        return {
            'runs_observados': runs,
            'runs_esperados': expected_runs,
            'variancia': variance_runs,
            'z_score': z_score,
            'p_valor_aproximado': 2 * (1 - abs(z_score) / 1.96) if abs(z_score) <= 1.96 else 0,
            'aleatorio': abs(z_score) < 1.96
        }
    
    def _autocorrelation_test(self, historical_data: List[List[int]]) -> Dict:
        """Teste de autocorrelação para detectar padrões temporais."""
        all_numbers = [num for draw in historical_data for num in draw]
        
        # Calcular autocorrelação para diferentes lags
        autocorrelations = {}
        for lag in [1, 2, 3, 5, 10]:
            if len(all_numbers) > lag:
                corr = np.corrcoef(all_numbers[:-lag], all_numbers[lag:])[0, 1]
                autocorrelations[f'lag_{lag}'] = corr if not np.isnan(corr) else 0
        
        # Teste global de independência
        max_autocorr = max(abs(corr) for corr in autocorrelations.values())
        
        return {
            'autocorrelacoes': autocorrelations,
            'max_autocorrelacao': max_autocorr,
            'independente': max_autocorr < 0.1,
            'interpretacao': 'Independente' if max_autocorr < 0.1 else 'Possível dependência temporal'
        }
    
    def _gaps_test(self, historical_data: List[List[int]]) -> Dict:
        """Teste de gaps entre aparições dos números."""
        gaps_analysis = {}
        
        for num in range(1, 61):
            appearances = []
            for i, draw in enumerate(historical_data):
                if num in draw:
                    appearances.append(i)
            
            if len(appearances) > 1:
                gaps = [appearances[i] - appearances[i-1] - 1 for i in range(1, len(appearances))]
                
                if gaps:
                    gaps_analysis[num] = {
                        'gaps': gaps,
                        'gap_medio': np.mean(gaps),
                        'gap_desvio': np.std(gaps),
                        'gap_max': max(gaps),
                        'gap_min': min(gaps)
                    }
        
        # Estatísticas globais
        all_gaps = [gap for data in gaps_analysis.values() for gap in data['gaps']]
        
        return {
            'gaps_por_numero': gaps_analysis,
            'estatisticas_globais': {
                'gap_medio_global': np.mean(all_gaps) if all_gaps else 0,
                'gap_desvio_global': np.std(all_gaps) if all_gaps else 0,
                'total_gaps_analisados': len(all_gaps)
            }
        }
    
    def _poker_test(self, historical_data: List[List[int]]) -> Dict:
        """Teste poker para padrões nos sorteios."""
        patterns = Counter()
        
        for draw in historical_data:
            # Analisar padrões baseados nos últimos dígitos
            last_digits = [num % 10 for num in draw]
            digit_counts = Counter(last_digits)
            
            # Classificar padrão
            counts = sorted(digit_counts.values(), reverse=True)
            if counts == [6]:
                pattern = "todos_iguais"
            elif counts == [2, 2, 2]:
                pattern = "tres_pares"
            elif counts == [3, 3]:
                pattern = "dois_triplos"
            elif counts[0] == 4:
                pattern = "quadrupla"
            elif counts[0] == 3:
                pattern = "tripla"
            elif counts[0] == 2:
                pattern = "par"
            else:
                pattern = "todos_diferentes"
            
            patterns[pattern] += 1
        
        total_draws = len(historical_data)
        pattern_probs = {pattern: count/total_draws for pattern, count in patterns.items()}
        
        return {
            'padroes_observados': dict(patterns),
            'probabilidades_padroes': pattern_probs,
            'padroes_mais_comuns': patterns.most_common(3)
        }
    
    def generate_predictions(self, 
                           historical_data: List[List[int]], 
                           method: str = "weighted_random",
                           num_predictions: int = 5) -> List[List[int]]:
        """
        Gera previsões baseadas em análise histórica.
        
        Methods:
        - weighted_random: Baseado em frequências históricas
        - hot_numbers: Números mais frequentes recentemente
        - cold_numbers: Números com maior atraso
        - balanced: Combinação de estratégias
        """
        if not historical_data:
            return []
        
        predictions = []
        
        for _ in range(num_predictions):
            if method == "weighted_random":
                prediction = self._weighted_random_prediction(historical_data)
            elif method == "hot_numbers":
                prediction = self._hot_numbers_prediction(historical_data)
            elif method == "cold_numbers":
                prediction = self._cold_numbers_prediction(historical_data)
            elif method == "balanced":
                prediction = self._balanced_prediction(historical_data)
            else:
                prediction = sorted(random.sample(range(1, 61), 6))
            
            predictions.append(prediction)
        
        return predictions
    
    def _weighted_random_prediction(self, historical_data: List[List[int]]) -> List[int]:
        """Predição baseada em frequências ponderadas."""
        all_numbers = [num for draw in historical_data for num in draw]
        frequency_counter = Counter(all_numbers)
        
        # Criar lista ponderada
        weighted_numbers = []
        for num in range(1, 61):
            weight = frequency_counter.get(num, 1)  # Pelo menos peso 1
            weighted_numbers.extend([num] * weight)
        
        # Selecionar 6 números únicos
        selected = []
        while len(selected) < 6:
            num = random.choice(weighted_numbers)
            if num not in selected:
                selected.append(num)
        
        return sorted(selected)
    
    def _hot_numbers_prediction(self, historical_data: List[List[int]]) -> List[int]:
        """Predição baseada nos números mais quentes (últimos 20 sorteios)."""
        recent_data = historical_data[-20:] if len(historical_data) >= 20 else historical_data
        recent_numbers = [num for draw in recent_data for num in draw]
        frequency_counter = Counter(recent_numbers)
        
        # Pegar os mais frequentes e completar aleatoriamente se necessário
        hot_numbers = [num for num, count in frequency_counter.most_common(10)]
        
        selected = random.sample(hot_numbers, min(6, len(hot_numbers)))
        while len(selected) < 6:
            num = random.randint(1, 60)
            if num not in selected:
                selected.append(num)
        
        return sorted(selected)
    
    def _cold_numbers_prediction(self, historical_data: List[List[int]]) -> List[int]:
        """Predição baseada nos números mais frios (maior atraso)."""
        # Calcular atrasos
        delays = {}
        for num in range(1, 61):
            for i, draw in enumerate(reversed(historical_data)):
                if num in draw:
                    delays[num] = i
                    break
            else:
                delays[num] = len(historical_data)  # Nunca apareceu
        
        # Ordenar por atraso
        cold_numbers = sorted(delays.keys(), key=lambda x: delays[x], reverse=True)
        
        # Selecionar alguns dos mais atrasados
        selected = cold_numbers[:6]
        
        return sorted(selected)
    
    def _balanced_prediction(self, historical_data: List[List[int]]) -> List[int]:
        """Predição balanceada combinando múltiplas estratégias."""
        # 2 números quentes
        hot_pred = self._hot_numbers_prediction(historical_data)[:2]
        
        # 2 números frios
        cold_pred = self._cold_numbers_prediction(historical_data)[:2]
        
        # 2 números aleatórios ponderados
        remaining = []
        while len(remaining) < 2:
            num = random.randint(1, 60)
            if num not in hot_pred and num not in cold_pred and num not in remaining:
                remaining.append(num)
        
        prediction = hot_pred + cold_pred + remaining
        return sorted(prediction)


def main():
    """Função principal para teste do módulo."""
    analytics = MegaSenaAdvancedAnalytics(seed=42)
    
    print("=== ANÁLISE PROBABILÍSTICA AVANÇADA DA MEGA SENA ===")
    
    # Simulação Monte Carlo
    print("\n1. Executando simulação Monte Carlo...")
    monte_carlo_result = analytics.monte_carlo_simulation(10000, strategy="random")
    
    print(f"   Simulações executadas: {monte_carlo_result['simulacoes_executadas']:,}")
    print(f"   Melhor resultado: {monte_carlo_result['melhor_resultado']} acertos")
    print(f"   Média de acertos: {monte_carlo_result['estatisticas']['media_acertos']:.2f}")
    print(f"   Tempo de execução: {monte_carlo_result['tempo_execucao']:.2f}s")
    
    # Dados de exemplo
    sample_data = [
        [4, 5, 30, 33, 41, 52],
        [10, 11, 16, 20, 27, 58],
        [1, 5, 11, 16, 20, 56],
        [7, 12, 31, 33, 42, 51],
        [2, 8, 15, 17, 49, 57]
    ] * 50
    
    print("\n2. Teste de uniformidade:")
    uniformity = analytics.uniform_distribution_test(sample_data)
    if "teste_uniformidade" in uniformity:
        test = uniformity['teste_uniformidade']
        print(f"   Chi-quadrado: {test['chi_quadrado']:.2f}")
        print(f"   Coeficiente de variação: {test['coef_variacao']:.4f}")
        print(f"   Conclusão: {uniformity['interpretacao']['conclusao']}")
    
    print("\n3. Testes de aleatoriedade:")
    randomness = analytics.randomness_tests(sample_data)
    print(f"   Teste de runs: {'Aleatório' if randomness['teste_runs']['aleatorio'] else 'Não aleatório'}")
    print(f"   Autocorrelação máxima: {randomness['teste_autocorrelacao']['max_autocorrelacao']:.4f}")
    
    print("\n4. Gerando previsões:")
    predictions = analytics.generate_predictions(sample_data, method="balanced", num_predictions=3)
    for i, pred in enumerate(predictions, 1):
        print(f"   Previsão {i}: {pred}")


if __name__ == "__main__":
    main()