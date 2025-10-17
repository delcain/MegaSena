#!/usr/bin/env python3
"""
Mega Sena - Análise de Teoria de Jogos e Estratégias

Este módulo implementa estratégias avançadas baseadas em teoria de jogos,
incluindo estratégias ótimas, análise de equilíbrio e otimização de portfólio.

MIT License
Copyright (c) 2025 delcain
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize, differential_evolution
from scipy.stats import pearsonr, spearmanr
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class MegaSenaGameTheoryAnalyzer:
    """Analisador de teoria de jogos para Mega Sena."""
    
    def __init__(self):
        """Inicializa o analisador."""
        self.historical_data = []
        self.df = None
        self.correlation_matrix = None
        self.frequency_matrix = None
        self.target_numbers = 6  # Número padrão de dezenas para jogar
        
    def prepare_game_theory_data(self, historical_data):
        """Prepara dados para análise de teoria de jogos."""
        self.historical_data = historical_data
        
        # Criar DataFrame com análises estratégicas
        data = []
        for i, numbers in enumerate(historical_data):
            # Se numbers for uma lista de números (estrutura simples)
            if isinstance(numbers, list):
                sorted_numbers = sorted(numbers)
            # Se numbers for um dicionário (estrutura completa)
            elif isinstance(numbers, dict) and 'numbers' in numbers:
                sorted_numbers = sorted(numbers['numbers'])
            else:
                continue  # Pular entradas inválidas
            
            # Métricas estratégicas
            sum_numbers = sum(sorted_numbers)
            range_numbers = max(sorted_numbers) - min(sorted_numbers)
            gaps = [sorted_numbers[j+1] - sorted_numbers[j] for j in range(len(sorted_numbers)-1)]
            avg_gap = np.mean(gaps)
            max_gap = max(gaps)
            
            # Distribuição por dezenas
            dezenas = [0] * 6  # 01-10, 11-20, ..., 51-60
            for num in sorted_numbers:
                dezena_idx = min((num - 1) // 10, 5)
                dezenas[dezena_idx] += 1
            
            # Paridade
            pares = sum(1 for n in sorted_numbers if n % 2 == 0)
            impares = 6 - pares
            
            # Números consecutivos
            consecutivos = sum(1 for j in range(len(sorted_numbers)-1) if sorted_numbers[j+1] - sorted_numbers[j] == 1)
            
            data.append({
                'sorteio_id': i + 1,  # ID sequencial
                'numbers': sorted_numbers,
                'sum_numbers': sum_numbers,
                'range_numbers': range_numbers,
                'avg_gap': avg_gap,
                'max_gap': max_gap,
                'pares': pares,
                'impares': impares,
                'consecutivos': consecutivos,
                'dezena_1': dezenas[0],
                'dezena_2': dezenas[1], 
                'dezena_3': dezenas[2],
                'dezena_4': dezenas[3],
                'dezena_5': dezenas[4],
                'dezena_6': dezenas[5]
            })
        
        self.df = pd.DataFrame(data)
        return self.df
    
    def calculate_number_correlations(self):
        """Calcula correlações entre números."""
        # Matrix de co-ocorrência
        cooccurrence = np.zeros((60, 60))
        
        for numbers in self.historical_data:
            # Tratar diferentes estruturas de dados
            if isinstance(numbers, list):
                number_list = numbers
            elif isinstance(numbers, dict) and 'numbers' in numbers:
                number_list = numbers['numbers']
            else:
                continue
                
            for i in range(len(number_list)):
                for j in range(i+1, len(number_list)):
                    num1, num2 = number_list[i] - 1, number_list[j] - 1  # 0-indexado
                    cooccurrence[num1][num2] += 1
                    cooccurrence[num2][num1] += 1
        
        # Normalizar por frequência individual
        frequencies = np.zeros(60)
        for numbers in self.historical_data:
            if isinstance(numbers, list):
                number_list = numbers
            elif isinstance(numbers, dict) and 'numbers' in numbers:
                number_list = numbers['numbers']
            else:
                continue
                
            for num in number_list:
                frequencies[num - 1] += 1
        
        # Calcular correlação
        correlation_matrix = np.zeros((60, 60))
        total_sorteios = len(self.historical_data)
        
        for i in range(60):
            for j in range(60):
                if i != j and frequencies[i] > 0 and frequencies[j] > 0:
                    expected = (frequencies[i] * frequencies[j]) / (total_sorteios * 6)
                    observed = cooccurrence[i][j]
                    if expected > 0:
                        correlation_matrix[i][j] = (observed - expected) / expected
        
        self.correlation_matrix = correlation_matrix
        return correlation_matrix
    
    def optimal_number_selection(self, strategy='balanced'):
        """Seleção ótima de números baseada em teoria de jogos."""
        if self.correlation_matrix is None:
            self.calculate_number_correlations()
        
        strategies = {}
        
        # Estratégia 1: Minimizar correlação (diversificação máxima)
        if strategy in ['balanced', 'min_correlation']:
            def objective_min_corr(selection):
                indices = [int(x) for x in selection]
                total_corr = 0
                count = 0
                for i in range(len(indices)):
                    for j in range(i+1, len(indices)):
                        total_corr += abs(self.correlation_matrix[indices[i]][indices[j]])
                        count += 1
                return total_corr / count if count > 0 else 0
            
            # Otimização usando algoritmo genético com constraint de unicidade
            def objective_with_constraint(selection):
                indices = [int(x) for x in selection]
                # Penalizar números duplicados
                unique_indices = list(set(indices))
                if len(unique_indices) < self.target_numbers:
                    return 1000  # Penalidade alta para duplicatas
                
                total_corr = 0
                count = 0
                for i in range(len(unique_indices)):
                    for j in range(i+1, len(unique_indices)):
                        total_corr += abs(self.correlation_matrix[unique_indices[i]][unique_indices[j]])
                        count += 1
                return total_corr / count if count > 0 else 0
            
            bounds = [(0, 59) for _ in range(self.target_numbers)]
            result = differential_evolution(
                objective_with_constraint,
                bounds,
                maxiter=200,
                popsize=30,
                seed=42,
                integrality=[True] * self.target_numbers
            )
            
            # Garantir números únicos
            indices = [int(x) for x in result.x]
            unique_indices = list(set(indices))
            while len(unique_indices) < self.target_numbers:
                # Adicionar números aleatórios únicos
                available = [i for i in range(60) if i not in unique_indices]
                if available:
                    unique_indices.append(np.random.choice(available))
            
            optimal_selection = sorted([x + 1 for x in unique_indices[:self.target_numbers]])
            strategies['min_correlation'] = {
                'numbers': optimal_selection,
                'correlation_score': result.fun,
                'description': 'Números com menor correlação entre si'
            }
        
        # Estratégia 2: Máxima cobertura de dezenas
        if strategy in ['balanced', 'max_coverage']:
            def objective_max_coverage(selection):
                indices = [int(x) for x in selection]
                dezenas_covered = set()
                for idx in indices:
                    num = idx + 1
                    dezena = min((num - 1) // 10, 5)
                    dezenas_covered.add(dezena)
                return -len(dezenas_covered)  # Negativos para maximizar
            
            bounds = [(0, 59) for _ in range(self.target_numbers)]
            result = differential_evolution(
                objective_max_coverage,
                bounds,
                maxiter=100,
                popsize=15,
                seed=43,
                integrality=[True] * self.target_numbers
            )
            
            optimal_selection = sorted([int(x) + 1 for x in result.x])
            strategies['max_coverage'] = {
                'numbers': optimal_selection,
                'coverage_score': -result.fun,
                'description': 'Máxima cobertura de dezenas'
            }
        
        # Estratégia 3: Equilíbrio frequência/correlação
        if strategy in ['balanced', 'frequency_balance']:
            # Calcular frequências
            frequencies = np.zeros(60)
            for numbers in self.historical_data:
                if isinstance(numbers, list):
                    number_list = numbers
                elif isinstance(numbers, dict) and 'numbers' in numbers:
                    number_list = numbers['numbers']
                else:
                    continue
                    
                for num in number_list:
                    frequencies[num - 1] += 1
            
            freq_normalized = frequencies / np.max(frequencies)
            
            def objective_balanced(selection):
                indices = [int(x) for x in selection]
                
                # Componente de correlação
                total_corr = 0
                count = 0
                for i in range(len(indices)):
                    for j in range(i+1, len(indices)):
                        total_corr += abs(self.correlation_matrix[indices[i]][indices[j]])
                        count += 1
                avg_corr = total_corr / count if count > 0 else 0
                
                # Componente de frequência (preferir números não muito frequentes)
                freq_penalty = np.mean([freq_normalized[idx] for idx in indices])
                
                return avg_corr + 0.3 * freq_penalty
            
            bounds = [(0, 59) for _ in range(self.target_numbers)]
            result = differential_evolution(
                objective_balanced,
                bounds,
                maxiter=100,
                popsize=15,
                seed=44,
                integrality=[True] * self.target_numbers
            )
            
            optimal_selection = sorted([int(x) + 1 for x in result.x])
            strategies['frequency_balance'] = {
                'numbers': optimal_selection,
                'balance_score': result.fun,
                'description': 'Equilíbrio entre frequência e correlação'
            }
        
        return strategies
    
    def nash_equilibrium_analysis(self):
        """Análise de equilíbrio de Nash adaptada para Mega Sena."""
        # Simular jogadores com diferentes estratégias
        players = {
            'conservative': {'freq_weight': 0.8, 'corr_weight': 0.2},
            'aggressive': {'freq_weight': 0.2, 'corr_weight': 0.8},
            'balanced': {'freq_weight': 0.5, 'corr_weight': 0.5}
        }
        
        if self.correlation_matrix is None:
            self.calculate_number_correlations()
        
        # Calcular frequências
        frequencies = np.zeros(60)
        for numbers in self.historical_data:
            if isinstance(numbers, list):
                number_list = numbers
            elif isinstance(numbers, dict) and 'numbers' in numbers:
                number_list = numbers['numbers']
            else:
                continue
                
            for num in number_list:
                frequencies[num - 1] += 1
        
        freq_normalized = frequencies / np.max(frequencies)
        
        equilibrium_strategies = {}
        
        for player_name, weights in players.items():
            def utility_function(selection):
                indices = [int(x) for x in selection]
                
                # Utilidade baseada em frequência (conservador prefere números frequentes)
                freq_utility = np.mean([freq_normalized[idx] for idx in indices])
                
                # Utilidade baseada em diversificação (baixa correlação)
                corr_penalty = 0
                count = 0
                for i in range(len(indices)):
                    for j in range(i+1, len(indices)):
                        corr_penalty += abs(self.correlation_matrix[indices[i]][indices[j]])
                        count += 1
                avg_corr = corr_penalty / count if count > 0 else 0
                
                # Função de utilidade combinada
                utility = (weights['freq_weight'] * freq_utility - 
                          weights['corr_weight'] * avg_corr)
                
                return -utility  # Negativo para maximizar
            
            bounds = [(0, 59) for _ in range(self.target_numbers)]
            result = differential_evolution(
                utility_function,
                bounds,
                maxiter=100,
                popsize=15,
                seed=45 + hash(player_name) % 100,
                integrality=[True] * self.target_numbers
            )
            
            optimal_numbers = sorted([int(x) + 1 for x in result.x])
            equilibrium_strategies[player_name] = {
                'numbers': optimal_numbers,
                'utility': -result.fun,
                'strategy_weights': weights,
                'description': f'Estratégia {player_name} em equilíbrio'
            }
        
        return equilibrium_strategies
    
    def minimax_strategy(self):
        """Estratégia minimax para minimizar perdas máximas."""
        if self.correlation_matrix is None:
            self.calculate_number_correlations()
        
        # Calcular métricas de risco para cada número
        frequencies = np.zeros(60)
        for numbers in self.historical_data:
            if isinstance(numbers, list):
                number_list = numbers
            elif isinstance(numbers, dict) and 'numbers' in numbers:
                number_list = numbers['numbers']
            else:
                continue
                
            for num in number_list:
                frequencies[num - 1] += 1
        
        # Variância de frequência como medida de risco
        mean_freq = np.mean(frequencies)
        risk_scores = np.abs(frequencies - mean_freq) / mean_freq
        
        def minimax_objective(selection):
            indices = [int(x) for x in selection]
            
            # Risco máximo na seleção
            max_risk = np.max([risk_scores[idx] for idx in indices])
            
            # Correlação como risco adicional
            max_corr = 0
            for i in range(len(indices)):
                for j in range(i+1, len(indices)):
                    corr = abs(self.correlation_matrix[indices[i]][indices[j]])
                    max_corr = max(max_corr, corr)
            
            return max_risk + 0.5 * max_corr
        
        bounds = [(0, 59) for _ in range(self.target_numbers)]
        result = differential_evolution(
            minimax_objective,
            bounds,
            maxiter=100,
            popsize=15,
            seed=46,
            integrality=[True] * self.target_numbers
        )
        
        minimax_numbers = sorted([int(x) + 1 for x in result.x])
        
        return {
            'numbers': minimax_numbers,
            'max_risk': result.fun,
            'description': 'Estratégia que minimiza o risco máximo',
            'risk_scores': [risk_scores[num-1] for num in minimax_numbers]
        }
    
    def portfolio_optimization(self, num_combinations=5):
        """Otimização de portfólio com múltiplas combinações."""
        if self.correlation_matrix is None:
            self.calculate_number_correlations()
        
        # Calcular retorno esperado (inverso da frequência normalizada)
        frequencies = np.zeros(60)
        for numbers in self.historical_data:
            if isinstance(numbers, list):
                number_list = numbers
            elif isinstance(numbers, dict) and 'numbers' in numbers:
                number_list = numbers['numbers']
            else:
                continue
                
            for num in number_list:
                frequencies[num - 1] += 1
        
        # Retorno esperado = 1 / (frequência normalizada + 0.1)
        max_freq = np.max(frequencies)
        expected_returns = 1 / ((frequencies / max_freq) + 0.1)
        
        # Variância = correlação média com outros números
        variances = np.zeros(60)
        for i in range(60):
            variances[i] = np.mean(np.abs(self.correlation_matrix[i]))
        
        def portfolio_objective(weights):
            # Markowitz: maximizar retorno - penalizar risco
            portfolio_return = np.sum(weights * expected_returns)
            portfolio_risk = np.sqrt(np.sum(weights**2 * variances))
            
            # Sharpe ratio modificado
            return -(portfolio_return / (portfolio_risk + 0.01))
        
        def constraint_sum_to_target(weights):
            return np.sum(weights) - self.target_numbers
        
        def constraint_each_max_1(weights):
            return 1 - np.max(weights)
        
        portfolios = []
        
        for i in range(num_combinations):
            # Ponto inicial aleatório
            x0 = np.random.random(60)
            x0 = self.target_numbers * x0 / np.sum(x0)  # Normalizar para somar target_numbers
            
            constraints = [
                {'type': 'eq', 'fun': constraint_sum_to_target},
                {'type': 'ineq', 'fun': constraint_each_max_1}
            ]
            
            bounds = [(0, 1) for _ in range(60)]
            
            result = minimize(
                portfolio_objective,
                x0,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                # Selecionar os números com maiores pesos
                sorted_indices = np.argsort(result.x)[::-1]
                selected_numbers = sorted([int(sorted_indices[j]) + 1 for j in range(self.target_numbers)])
                
                # Calcular métricas do portfólio
                selected_weights = [result.x[num-1] for num in selected_numbers]
                portfolio_return = np.sum([result.x[j] * expected_returns[j] for j in range(60)])
                portfolio_risk = np.sqrt(np.sum([result.x[j]**2 * variances[j] for j in range(60)]))
                
                portfolios.append({
                    'combination': i + 1,
                    'numbers': selected_numbers,
                    'weights': selected_weights,
                    'expected_return': portfolio_return,
                    'risk': portfolio_risk,
                    'sharpe_ratio': -result.fun,
                    'optimization_success': True
                })
        
        # Ordenar por Sharpe ratio
        portfolios.sort(key=lambda x: x['sharpe_ratio'], reverse=True)
        
        return portfolios
    
    def cluster_based_strategy(self, n_clusters=None):
        """Estratégia baseada em clustering de números."""
        if n_clusters is None:
            n_clusters = min(self.target_numbers, 6)  # Usar no máximo 6 clusters
            
        # Preparar features para clustering
        features = []
        
        # Calcular frequências
        frequencies = np.zeros(60)
        co_occurrences = np.zeros((60, 60))
        
        for numbers in self.historical_data:
            if isinstance(numbers, list):
                number_list = numbers
            elif isinstance(numbers, dict) and 'numbers' in numbers:
                number_list = numbers['numbers']
            else:
                continue
                
            for num in number_list:
                frequencies[num - 1] += 1
            
            # Co-ocorrências
            for i in range(len(number_list)):
                for j in range(i+1, len(number_list)):
                    co_occurrences[number_list[i]-1][number_list[j]-1] += 1
                    co_occurrences[number_list[j]-1][number_list[i]-1] += 1
        
        # Features: frequência + soma de co-ocorrências
        for i in range(60):
            freq = frequencies[i]
            total_cooccur = np.sum(co_occurrences[i])
            features.append([freq, total_cooccur, i+1])  # número como feature
        
        features = np.array(features)
        
        # Normalizar features
        scaler = StandardScaler()
        features_normalized = scaler.fit_transform(features[:, :-1])  # Excluir número
        
        # Clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(features_normalized)
        
        # Selecionar um número de cada cluster
        cluster_strategy = []
        cluster_info = []
        
        for cluster_id in range(n_clusters):
            cluster_numbers = [i+1 for i in range(60) if clusters[i] == cluster_id]
            
            if cluster_numbers:
                # Selecionar número com melhor balance freq/co-occur no cluster
                cluster_features = [features[i-1] for i in cluster_numbers]
                
                # Score: freq normalizada + co-occur normalizada
                best_score = -1
                best_number = cluster_numbers[0]
                
                for i, num in enumerate(cluster_numbers):
                    freq_norm = cluster_features[i][0] / np.max(frequencies)
                    cooccur_norm = cluster_features[i][1] / np.max([f[1] for f in cluster_features])
                    score = 0.6 * freq_norm + 0.4 * cooccur_norm
                    
                    if score > best_score:
                        best_score = score
                        best_number = num
                
                cluster_strategy.append(best_number)
                cluster_info.append({
                    'cluster': cluster_id,
                    'numbers_in_cluster': cluster_numbers,
                    'selected': best_number,
                    'score': best_score
                })
        
        # Se não temos números suficientes, completar com os melhores restantes
        while len(cluster_strategy) < self.target_numbers:
            remaining = [i+1 for i in range(60) if i+1 not in cluster_strategy]
            if remaining:
                # Adicionar número com melhor frequência
                best_freq = -1
                best_remaining = remaining[0]
                for num in remaining:
                    if frequencies[num-1] > best_freq:
                        best_freq = frequencies[num-1]
                        best_remaining = num
                cluster_strategy.append(best_remaining)
            else:
                break
        
        return {
            'numbers': sorted(cluster_strategy[:self.target_numbers]),
            'clusters': cluster_info,
            'n_clusters': n_clusters,
            'description': f'Estratégia baseada em {n_clusters} clusters para {self.target_numbers} números'
        }
    
    def _clean_numpy_types(self, obj):
        """Converte tipos numpy para tipos Python nativos."""
        if isinstance(obj, dict):
            return {key: self._clean_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._clean_numpy_types(item) for item in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    def generate_game_theory_report(self, historical_data):
        """Gera relatório completo de teoria de jogos."""
        print("🎲 Executando análise de teoria de jogos...")
        
        # Preparar dados
        self.prepare_game_theory_data(historical_data)
        
        # Executar todas as análises
        optimal_strategies = self.optimal_number_selection('balanced')
        nash_equilibrium = self.nash_equilibrium_analysis()
        minimax_result = self.minimax_strategy()
        portfolio_results = self.portfolio_optimization(3)
        cluster_strategy = self.cluster_based_strategy()
        
        report = {
            'summary': {
                'total_sorteios_analisados': len(historical_data),
                'numero_estrategias_geradas': len(optimal_strategies) + len(nash_equilibrium) + 3,
                'melhor_portfolio_sharpe': portfolio_results[0]['sharpe_ratio'] if portfolio_results else 0,
                'estrategia_recomendada': portfolio_results[0]['numbers'] if portfolio_results else []
            },
            'optimal_strategies': optimal_strategies,
            'nash_equilibrium': nash_equilibrium,
            'minimax_strategy': minimax_result,
            'portfolio_optimization': portfolio_results,
            'cluster_strategy': cluster_strategy,
            'correlation_insights': self._analyze_correlations(),
            'strategy_comparison': self._compare_strategies(
                optimal_strategies, nash_equilibrium, minimax_result, 
                portfolio_results, cluster_strategy
            )
        }
        
        # Limpar tipos numpy do relatório
        report = self._clean_numpy_types(report)
        
        return report
    
    def _analyze_correlations(self):
        """Analisa correlações entre números."""
        if self.correlation_matrix is None:
            return {}
        
        # Encontrar pares mais/menos correlacionados
        correlations = []
        for i in range(60):
            for j in range(i+1, 60):
                correlations.append({
                    'pair': (i+1, j+1),
                    'correlation': self.correlation_matrix[i][j]
                })
        
        correlations.sort(key=lambda x: x['correlation'])
        
        return {
            'most_negatively_correlated': correlations[:5],
            'most_positively_correlated': correlations[-5:],
            'average_correlation': np.mean([c['correlation'] for c in correlations]),
            'correlation_std': np.std([c['correlation'] for c in correlations])
        }
    
    def _compare_strategies(self, optimal, nash, minimax, portfolio, cluster):
        """Compara diferentes estratégias."""
        strategies = {}
        
        # Optimal strategies
        for name, strategy in optimal.items():
            strategies[f'optimal_{name}'] = strategy['numbers']
        
        # Nash equilibrium
        for name, strategy in nash.items():
            strategies[f'nash_{name}'] = strategy['numbers']
        
        # Minimax
        strategies['minimax'] = minimax['numbers']
        
        # Portfolio (melhor)
        if portfolio:
            strategies['portfolio_best'] = portfolio[0]['numbers']
        
        # Cluster
        strategies['cluster'] = cluster['numbers']
        
        # Calcular diversidade entre estratégias
        diversity_matrix = {}
        strategy_names = list(strategies.keys())
        
        for i, name1 in enumerate(strategy_names):
            for j, name2 in enumerate(strategy_names):
                if i < j:
                    numbers1 = set(strategies[name1])
                    numbers2 = set(strategies[name2])
                    intersection = len(numbers1.intersection(numbers2))
                    diversity = 6 - intersection  # Quanto menor intersecção, maior diversidade
                    diversity_matrix[f'{name1}_vs_{name2}'] = {
                        'common_numbers': intersection,
                        'diversity_score': diversity
                    }
        
        return {
            'strategies': strategies,
            'diversity_analysis': diversity_matrix,
            'total_unique_numbers': len(set().union(*strategies.values())),
            'recommendation': self._get_strategy_recommendation(strategies)
        }
    
    def _get_strategy_recommendation(self, strategies):
        """Recomenda a melhor estratégia baseada em critérios múltiplos."""
        scores = {}
        
        for name, numbers in strategies.items():
            score = 0
            
            # Critério 1: Distribuição por dezenas
            dezenas = [0] * 6
            for num in numbers:
                dezena_idx = min((num - 1) // 10, 5)
                dezenas[dezena_idx] += 1
            
            # Penalizar concentração excessiva (adaptado para target_numbers)
            max_concentracao = max(dezenas)
            # Score baseado na distribuição: melhor quando mais distribuído
            dezena_balance = min(6, self.target_numbers) - max_concentracao
            score += max(0, dezena_balance)
            
            # Critério 2: Paridade (adaptado para target_numbers)
            pares = sum(1 for n in numbers if n % 2 == 0)
            ideal_pares = self.target_numbers // 2
            paridade_balance = self.target_numbers - abs(pares - ideal_pares)
            score += max(0, paridade_balance)
            
            # Critério 3: Distribuição de soma
            soma = sum(numbers)
            # Soma ideal baseada no número de dezenas: aproximadamente target_numbers * 30
            soma_ideal = self.target_numbers * 30
            soma_tolerance = self.target_numbers * 10
            
            if abs(soma - soma_ideal) <= soma_tolerance:
                soma_balance = 5
            else:
                soma_balance = max(0, 5 - abs(soma - soma_ideal) / soma_tolerance)
            score += soma_balance
            
            scores[name] = score
        
        # Encontrar estratégia com melhor score
        best_strategy = max(scores.items(), key=lambda x: x[1])
        
        # Score máximo possível
        max_possible_score = min(6, self.target_numbers) + self.target_numbers + 5
        
        return {
            'recommended_strategy': best_strategy[0],
            'recommended_numbers': strategies[best_strategy[0]],
            'score': best_strategy[1],
            'max_score': max_possible_score,
            'all_scores': scores,
            'reasoning': f'Baseado em equilíbrio de dezenas, paridade e soma para {self.target_numbers} números'
        }
    
    def create_game_theory_plots(self):
        """Cria visualizações para teoria de jogos."""
        plots_created = []
        
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            import os
            
            # Criar diretório para plots
            plots_dir = os.path.join('data', 'plots', 'game_theory')
            os.makedirs(plots_dir, exist_ok=True)
            
            # Plot 1: Matriz de correlação
            if self.correlation_matrix is not None:
                plt.figure(figsize=(12, 10))
                mask = np.zeros_like(self.correlation_matrix, dtype=bool)
                mask[np.triu_indices_from(mask)] = True
                
                sns.heatmap(
                    self.correlation_matrix,
                    mask=mask,
                    annot=False,
                    cmap='RdBu_r',
                    center=0,
                    square=True,
                    fmt='.2f'
                )
                plt.title('Matriz de Correlação entre Números da Mega Sena')
                plt.xlabel('Número')
                plt.ylabel('Número')
                
                correlation_plot = os.path.join(plots_dir, 'correlation_matrix.png')
                plt.savefig(correlation_plot, dpi=300, bbox_inches='tight')
                plt.close()
                plots_created.append(correlation_plot)
            
            # Plot 2: Distribuição de frequências
            frequencies = np.zeros(60)
            for numbers in self.historical_data:
                if isinstance(numbers, list):
                    number_list = numbers
                elif isinstance(numbers, dict) and 'numbers' in numbers:
                    number_list = numbers['numbers']
                else:
                    continue
                    
                for num in number_list:
                    frequencies[num - 1] += 1
            
            plt.figure(figsize=(15, 6))
            bars = plt.bar(range(1, 61), frequencies, color='skyblue', alpha=0.7)
            plt.axhline(y=np.mean(frequencies), color='red', linestyle='--', 
                       label=f'Média: {np.mean(frequencies):.1f}')
            
            # Destacar números mais/menos frequentes
            max_freq_idx = np.argmax(frequencies)
            min_freq_idx = np.argmin(frequencies)
            bars[max_freq_idx].set_color('red')
            bars[min_freq_idx].set_color('blue')
            
            plt.title('Frequência dos Números na Mega Sena')
            plt.xlabel('Número')
            plt.ylabel('Frequência Absoluta')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            frequency_plot = os.path.join(plots_dir, 'number_frequencies.png')
            plt.savefig(frequency_plot, dpi=300, bbox_inches='tight')
            plt.close()
            plots_created.append(frequency_plot)
            
            return plots_created
            
        except Exception as e:
            print(f"⚠️ Erro ao criar gráficos: {e}")
            return plots_created