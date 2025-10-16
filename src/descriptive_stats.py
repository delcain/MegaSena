"""
Módulo de estatística descritiva para análise da Mega Sena.
Analisa frequências, cria histogramas e identifica padrões.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
import os


class MegaSenaStatistics:
    """Analisador de estatísticas descritivas da Mega Sena."""
    
    def __init__(self, output_dir: str = "data/plots"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Configurar estilo dos gráficos
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def frequency_analysis(self, historical_data: List[List[int]]) -> Dict:
        """Análise de frequência dos números sorteados."""
        if not historical_data:
            return {"erro": "Dados históricos necessários"}
        
        # Contar frequências
        all_numbers = [num for draw in historical_data for num in draw]
        frequency_counter = Counter(all_numbers)
        
        # Estatísticas básicas
        frequencies = list(frequency_counter.values())
        total_draws = len(historical_data)
        expected_frequency = total_draws * 6 / 60  # Frequência esperada teórica
        
        # Criar dicionário com estatísticas completas
        number_stats = {}
        for num in range(1, 61):
            freq = frequency_counter.get(num, 0)
            percentage = (freq / len(all_numbers)) * 100
            deviation = freq - expected_frequency
            
            number_stats[num] = {
                'frequencia': freq,
                'percentual': percentage,
                'desvio_esperado': deviation,
                'freq_relativa': freq / total_draws,
                'atraso_atual': self._calculate_delay(num, historical_data)
            }
        
        # Estatísticas gerais
        stats_summary = {
            'total_sorteios': total_draws,
            'media_frequencia': np.mean(frequencies),
            'mediana_frequencia': np.median(frequencies),
            'desvio_padrao': np.std(frequencies),
            'coef_variacao': np.std(frequencies) / np.mean(frequencies),
            'frequencia_esperada': expected_frequency,
            'numero_mais_frequente': frequency_counter.most_common(1)[0],
            'numero_menos_frequente': frequency_counter.most_common()[-1],
            'numeros_acima_media': sum(1 for f in frequencies if f > np.mean(frequencies)),
            'numeros_abaixo_media': sum(1 for f in frequencies if f < np.mean(frequencies))
        }
        
        return {
            'estatisticas_por_numero': number_stats,
            'resumo_geral': stats_summary,
            'top_10_mais_frequentes': frequency_counter.most_common(10),
            'top_10_menos_frequentes': frequency_counter.most_common()[-10:]
        }
    
    def _calculate_delay(self, number: int, historical_data: List[List[int]]) -> int:
        """Calcula atraso atual de um número (sorteios desde última aparição)."""
        for i, draw in enumerate(reversed(historical_data)):
            if number in draw:
                return i
        return len(historical_data)  # Nunca apareceu
    
    def delay_analysis(self, historical_data: List[List[int]]) -> Dict:
        """Análise de atrasos dos números."""
        if not historical_data:
            return {"erro": "Dados históricos necessários"}
        
        delay_stats = {}
        max_delays = {}
        delay_history = defaultdict(list)
        
        # Para cada número, calcular histórico de atrasos
        for num in range(1, 61):
            delays = []
            last_appearance = -1
            
            for i, draw in enumerate(historical_data):
                if num in draw:
                    if last_appearance >= 0:
                        delay = i - last_appearance - 1
                        delays.append(delay)
                    last_appearance = i
            
            if delays:
                delay_stats[num] = {
                    'atraso_medio': np.mean(delays),
                    'atraso_maximo': max(delays),
                    'atraso_minimo': min(delays),
                    'desvio_padrao_atraso': np.std(delays),
                    'atraso_atual': self._calculate_delay(num, historical_data),
                    'total_aparicoes': len(delays) + 1,
                    'historico_atrasos': delays
                }
                max_delays[num] = max(delays)
                delay_history[num] = delays
        
        # Estatísticas gerais de atraso
        all_delays = [delay for delays in delay_history.values() for delay in delays]
        current_delays = [self._calculate_delay(num, historical_data) for num in range(1, 61)]
        
        general_stats = {
            'atraso_medio_geral': np.mean(all_delays) if all_delays else 0,
            'atraso_maximo_historico': max(all_delays) if all_delays else 0,
            'atraso_medio_atual': np.mean(current_delays),
            'numeros_com_atraso_alto': sum(1 for delay in current_delays if delay > np.mean(all_delays)),
            'numero_maior_atraso_atual': current_delays.index(max(current_delays)) + 1,
            'maior_atraso_atual': max(current_delays)
        }
        
        return {
            'atrasos_por_numero': delay_stats,
            'estatisticas_gerais': general_stats,
            'ranking_atraso_atual': sorted(enumerate(current_delays, 1), key=lambda x: x[1], reverse=True)[:10]
        }
    
    def pattern_analysis(self, historical_data: List[List[int]]) -> Dict:
        """Análise de padrões nos sorteios."""
        if not historical_data:
            return {"erro": "Dados históricos necessários"}
        
        patterns = {
            'sequencias_consecutivas': [],
            'numeros_terminados_em': Counter(),
            'soma_sorteios': [],
            'dispersao_sorteios': [],
            'quadrantes': Counter(),
            'primeira_dezena_count': 0,
            'ultima_dezena_count': 0
        }
        
        for draw in historical_data:
            sorted_draw = sorted(draw)
            
            # Sequências consecutivas
            consecutive_count = 0
            for i in range(len(sorted_draw) - 1):
                if sorted_draw[i+1] - sorted_draw[i] == 1:
                    consecutive_count += 1
            patterns['sequencias_consecutivas'].append(consecutive_count)
            
            # Análise por terminação
            for num in draw:
                last_digit = num % 10
                patterns['numeros_terminados_em'][last_digit] += 1
            
            # Soma dos números
            patterns['soma_sorteios'].append(sum(draw))
            
            # Dispersão (diferença entre maior e menor)
            patterns['dispersao_sorteios'].append(max(draw) - min(draw))
            
            # Análise por quadrantes
            q1 = sum(1 for n in draw if 1 <= n <= 15)
            q2 = sum(1 for n in draw if 16 <= n <= 30)
            q3 = sum(1 for n in draw if 31 <= n <= 45)
            q4 = sum(1 for n in draw if 46 <= n <= 60)
            patterns['quadrantes'][f"Q1:{q1}_Q2:{q2}_Q3:{q3}_Q4:{q4}"] += 1
            
            # Primeira e última dezena
            if any(1 <= n <= 10 for n in draw):
                patterns['primeira_dezena_count'] += 1
            if any(51 <= n <= 60 for n in draw):
                patterns['ultima_dezena_count'] += 1
        
        # Estatísticas dos padrões
        total_draws = len(historical_data)
        pattern_stats = {
            'media_consecutivos': np.mean(patterns['sequencias_consecutivas']),
            'max_consecutivos': max(patterns['sequencias_consecutivas']),
            'distribuicao_consecutivos': Counter(patterns['sequencias_consecutivas']),
            'soma_media': np.mean(patterns['soma_sorteios']),
            'soma_desvio_padrao': np.std(patterns['soma_sorteios']),
            'soma_min': min(patterns['soma_sorteios']),
            'soma_max': max(patterns['soma_sorteios']),
            'dispersao_media': np.mean(patterns['dispersao_sorteios']),
            'dispersao_desvio_padrao': np.std(patterns['dispersao_sorteios']),
            'freq_primeira_dezena': patterns['primeira_dezena_count'] / total_draws * 100,
            'freq_ultima_dezena': patterns['ultima_dezena_count'] / total_draws * 100,
            'terminacoes_mais_comuns': patterns['numeros_terminados_em'].most_common(5),
            'quadrantes_mais_comuns': patterns['quadrantes'].most_common(5)
        }
        
        return {
            'padroes_brutos': patterns,
            'estatisticas_padroes': pattern_stats
        }
    
    def create_frequency_histogram(self, historical_data: List[List[int]], save_plot: bool = True) -> str:
        """Cria histograma de frequências."""
        freq_analysis = self.frequency_analysis(historical_data)
        
        if "erro" in freq_analysis:
            return "Erro: dados insuficientes"
        
        # Preparar dados
        numbers = list(range(1, 61))
        frequencies = [freq_analysis['estatisticas_por_numero'][num]['frequencia'] for num in numbers]
        expected_freq = freq_analysis['resumo_geral']['frequencia_esperada']
        
        # Criar gráfico
        plt.figure(figsize=(15, 8))
        bars = plt.bar(numbers, frequencies, alpha=0.7, color='skyblue', edgecolor='navy')
        plt.axhline(y=expected_freq, color='red', linestyle='--', linewidth=2, 
                   label=f'Frequência Esperada ({expected_freq:.1f})')
        
        # Destacar números extremos
        max_freq_num = freq_analysis['resumo_geral']['numero_mais_frequente'][0]
        min_freq_num = freq_analysis['resumo_geral']['numero_menos_frequente'][0]
        
        bars[max_freq_num-1].set_color('green')
        bars[min_freq_num-1].set_color('red')
        
        plt.xlabel('Números da Mega Sena')
        plt.ylabel('Frequência de Aparição')
        plt.title('Histograma de Frequências - Mega Sena')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(range(1, 61, 5))
        
        # Adicionar anotações
        plt.annotate(f'Mais frequente: {max_freq_num}', 
                    xy=(max_freq_num, frequencies[max_freq_num-1]), 
                    xytext=(max_freq_num+5, frequencies[max_freq_num-1]+5),
                    arrowprops=dict(arrowstyle='->', color='green'))
        
        plt.tight_layout()
        
        if save_plot:
            plot_path = os.path.join(self.output_dir, 'frequency_histogram.png')
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            return plot_path
        else:
            plt.show()
            return "Gráfico exibido"
    
    def create_delay_analysis_plot(self, historical_data: List[List[int]], save_plot: bool = True) -> str:
        """Cria gráfico de análise de atrasos."""
        delay_analysis = self.delay_analysis(historical_data)
        
        if "erro" in delay_analysis:
            return "Erro: dados insuficientes"
        
        # Preparar dados
        numbers = list(range(1, 61))
        current_delays = [delay_analysis['atrasos_por_numero'].get(num, {}).get('atraso_atual', 0) 
                         for num in numbers]
        avg_delays = [delay_analysis['atrasos_por_numero'].get(num, {}).get('atraso_medio', 0) 
                     for num in numbers]
        
        # Criar gráfico com subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # Gráfico 1: Atrasos atuais
        bars1 = ax1.bar(numbers, current_delays, alpha=0.7, color='orange', edgecolor='red')
        ax1.set_xlabel('Números da Mega Sena')
        ax1.set_ylabel('Atraso Atual (sorteios)')
        ax1.set_title('Atraso Atual dos Números')
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(range(1, 61, 5))
        
        # Destacar maior atraso
        max_delay_idx = current_delays.index(max(current_delays))
        bars1[max_delay_idx].set_color('red')
        
        # Gráfico 2: Atrasos médios históricos
        ax2.bar(numbers, avg_delays, alpha=0.7, color='lightblue', edgecolor='blue')
        ax2.set_xlabel('Números da Mega Sena')
        ax2.set_ylabel('Atraso Médio Histórico')
        ax2.set_title('Atraso Médio Histórico dos Números')
        ax2.grid(True, alpha=0.3)
        ax2.set_xticks(range(1, 61, 5))
        
        plt.tight_layout()
        
        if save_plot:
            plot_path = os.path.join(self.output_dir, 'delay_analysis.png')
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            return plot_path
        else:
            plt.show()
            return "Gráfico exibido"
    
    def create_pattern_analysis_plots(self, historical_data: List[List[int]], save_plot: bool = True) -> List[str]:
        """Cria gráficos de análise de padrões."""
        pattern_analysis = self.pattern_analysis(historical_data)
        
        if "erro" in pattern_analysis:
            return ["Erro: dados insuficientes"]
        
        plot_paths = []
        
        # Gráfico 1: Distribuição das somas
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.hist(pattern_analysis['padroes_brutos']['soma_sorteios'], bins=30, 
                alpha=0.7, color='purple', edgecolor='black')
        plt.xlabel('Soma dos 6 números')
        plt.ylabel('Frequência')
        plt.title('Distribuição das Somas dos Sorteios')
        plt.grid(True, alpha=0.3)
        
        # Gráfico 2: Números por terminação
        plt.subplot(1, 2, 2)
        terminacoes = pattern_analysis['padroes_brutos']['numeros_terminados_em']
        digits = list(range(10))
        counts = [terminacoes[d] for d in digits]
        plt.bar(digits, counts, alpha=0.7, color='green', edgecolor='darkgreen')
        plt.xlabel('Último dígito')
        plt.ylabel('Frequência')
        plt.title('Distribuição por Último Dígito')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plot:
            plot_path = os.path.join(self.output_dir, 'pattern_analysis.png')
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_paths.append(plot_path)
        else:
            plt.show()
        
        # Gráfico 3: Heatmap de correlações (números que saem juntos)
        correlation_matrix = self._calculate_number_correlations(historical_data)
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, cmap='coolwarm', center=0, 
                   square=True, cbar_kws={'label': 'Correlação'})
        plt.title('Matriz de Correlação entre Números')
        plt.xlabel('Números')
        plt.ylabel('Números')
        
        if save_plot:
            plot_path = os.path.join(self.output_dir, 'correlation_heatmap.png')
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_paths.append(plot_path)
        else:
            plt.show()
        
        return plot_paths if plot_paths else ["Gráficos exibidos"]
    
    def _calculate_number_correlations(self, historical_data: List[List[int]]) -> np.ndarray:
        """Calcula matriz de correlação entre números."""
        # Criar matriz binária (60 números x total de sorteios)
        matrix = np.zeros((60, len(historical_data)))
        
        for i, draw in enumerate(historical_data):
            for num in draw:
                matrix[num-1, i] = 1
        
        # Calcular correlação
        correlation_matrix = np.corrcoef(matrix)
        
        return correlation_matrix
    
    def generate_complete_report(self, historical_data: List[List[int]]) -> Dict:
        """Gera relatório completo de estatísticas."""
        print("Gerando análise de frequências...")
        freq_analysis = self.frequency_analysis(historical_data)
        
        print("Gerando análise de atrasos...")
        delay_analysis = self.delay_analysis(historical_data)
        
        print("Gerando análise de padrões...")
        pattern_analysis = self.pattern_analysis(historical_data)
        
        print("Criando gráficos...")
        freq_plot = self.create_frequency_histogram(historical_data)
        delay_plot = self.create_delay_analysis_plot(historical_data)
        pattern_plots = self.create_pattern_analysis_plots(historical_data)
        
        return {
            'analise_frequencia': freq_analysis,
            'analise_atraso': delay_analysis,
            'analise_padroes': pattern_analysis,
            'graficos_gerados': {
                'histograma_frequencia': freq_plot,
                'analise_atraso': delay_plot,
                'analise_padroes': pattern_plots
            }
        }


def main():
    """Função principal para teste do módulo."""
    # Dados de exemplo para teste
    sample_data = [
        [4, 5, 30, 33, 41, 52],
        [10, 11, 16, 20, 27, 58],
        [1, 5, 11, 16, 20, 56],
        [7, 12, 31, 33, 42, 51],
        [2, 8, 15, 17, 49, 57]
    ] * 100  # Simular mais dados
    
    stats = MegaSenaStatistics()
    
    print("=== ESTATÍSTICA DESCRITIVA DA MEGA SENA ===")
    
    print("\n1. Análise de frequências:")
    freq_analysis = stats.frequency_analysis(sample_data)
    if "resumo_geral" in freq_analysis:
        summary = freq_analysis['resumo_geral']
        print(f"   Total de sorteios: {summary['total_sorteios']}")
        print(f"   Média de frequência: {summary['media_frequencia']:.2f}")
        print(f"   Número mais frequente: {summary['numero_mais_frequente']}")
        print(f"   Número menos frequente: {summary['numero_menos_frequente']}")
    
    print("\n2. Análise de atrasos:")
    delay_analysis = stats.delay_analysis(sample_data)
    if "estatisticas_gerais" in delay_analysis:
        general = delay_analysis['estatisticas_gerais']
        print(f"   Atraso médio geral: {general['atraso_medio_geral']:.2f}")
        print(f"   Maior atraso atual: {general['maior_atraso_atual']}")
        print(f"   Número com maior atraso: {general['numero_maior_atraso_atual']}")
    
    print("\n3. Criando gráficos...")
    freq_plot = stats.create_frequency_histogram(sample_data)
    print(f"   Histograma de frequência: {freq_plot}")


if __name__ == "__main__":
    main()