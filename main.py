"""
Aplicativo principal de análise da Mega Sena.
Interface que integra todos os módulos de análise.

MIT License - Copyright (c) 2025 delcain
Veja LICENSE para detalhes completos.
"""

import sys
import os
from datetime import datetime
from typing import Dict, List
from collections import Counter

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.data_collector import MegaSenaDataCollector
    from src.probability_analyzer import MegaSenaProbabilityAnalyzer
    from src.descriptive_stats import MegaSenaStatistics
    from src.advanced_analytics import MegaSenaAdvancedAnalytics
    from src.time_series_analyzer import MegaSenaTimeSeriesAnalyzer
    from src.game_theory_analyzer import MegaSenaGameTheoryAnalyzer
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de que todas as dependências estão instaladas:")
    print("pip install -r requirements.txt")
    sys.exit(1)

try:
    from colorama import init, Fore, Style
    init()  # Inicializar colorama para cores no terminal
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


class MegaSenaApp:
    """Aplicativo principal de análise da Mega Sena."""
    
    def __init__(self):
        self.collector = MegaSenaDataCollector()
        self.probability_analyzer = MegaSenaProbabilityAnalyzer()
        self.stats = MegaSenaStatistics()
        self.advanced_analytics = MegaSenaAdvancedAnalytics()
        self.time_series_analyzer = MegaSenaTimeSeriesAnalyzer()
        self.game_theory_analyzer = MegaSenaGameTheoryAnalyzer()
        self.historical_data = []
        self.data_loaded = False
    
    def print_colored(self, text: str, color: str = "white"):
        """Imprime texto colorido se colorama estiver disponível."""
        if not COLORS_AVAILABLE:
            print(text)
            return
        
        color_map = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE
        }
        
        color_code = color_map.get(color, Fore.WHITE)
        print(f"{color_code}{text}{Style.RESET_ALL}")
    
    def print_header(self, title: str):
        """Imprime cabeçalho formatado."""
        separator = "=" * len(title)
        self.print_colored(f"\n{separator}", "cyan")
        self.print_colored(title, "cyan")
        self.print_colored(separator, "cyan")
    
    def print_menu(self):
        """Exibe o menu principal."""
        self.print_header("MEGA SENA - ANÁLISE PROBABILÍSTICA")
        print("📊 MENU PRINCIPAL:")
        print("1. 📥 Atualizar dados históricos")
        print("2. 📈 Análise de probabilidades")
        print("3. 📊 Estatísticas descritivas")
        print("4. 🎯 Análise probabilística avançada")
        print("5. 🔮 Gerar previsões")
        print("6. 🕒 Análise de séries temporais")
        print("7. 🎲 Teoria de jogos e estratégias ⭐ NOVO!")
        print("8. � Relatório completo")
        print("9. ℹ️  Informações dos dados")
        print("10. 💰 Configurar valor do jogo")
        print("0. 🚪 Sair")
        print()
    
    def load_data(self):
        """Carrega dados históricos."""
        if not self.data_loaded:
            self.print_colored("Carregando dados históricos...", "yellow")
            try:
                self.historical_data = self.collector.get_all_numbers()
                if self.historical_data:
                    self.data_loaded = True
                    self.print_colored(f"✅ {len(self.historical_data)} sorteios carregados!", "green")
                else:
                    self.print_colored("⚠️ Nenhum dado encontrado. Execute a opção 1 primeiro.", "yellow")
                    return False
            except Exception as e:
                self.print_colored(f"❌ Erro ao carregar dados: {e}", "red")
                return False
        return True
    
    def update_data(self):
        """Atualiza dados históricos."""
        self.print_header("ATUALIZAÇÃO DE DADOS")
        
        try:
            self.print_colored("Conectando à fonte oficial da Caixa...", "yellow")
            updated = self.collector.update_historical_data()
            
            if updated:
                self.print_colored("✅ Dados atualizados com sucesso!", "green")
                self.data_loaded = False  # Forçar recarregamento
                self.load_data()
            else:
                self.print_colored("ℹ️ Dados já estão atualizados.", "blue")
                if not self.data_loaded:
                    self.load_data()
            
            # Mostrar resumo
            summary = self.collector.get_statistics_summary()
            if summary:
                print("\n📋 RESUMO DOS DADOS:")
                print(f"   📊 Total de sorteios: {summary['total_sorteios']}")
                print(f"   🎯 Primeiro sorteio: #{summary['primeiro_sorteio']} ({summary['data_primeiro']})")
                print(f"   🆕 Último sorteio: #{summary['ultimo_sorteio']} ({summary['data_ultimo']})")
                print(f"   🔢 Total de números sorteados: {summary['total_numeros_sorteados']:,}")
        
        except Exception as e:
            self.print_colored(f"❌ Erro na atualização: {e}", "red")
    
    def probability_analysis(self):
        """Executa análise de probabilidades."""
        self.print_header("ANÁLISE DE PROBABILIDADES")
        
        if not self.load_data():
            return
        
        print("\n🎲 PROBABILIDADES BÁSICAS:")
        total_combinations = self.probability_analyzer.total_combinations()
        specific_prob = self.probability_analyzer.probability_specific_combination()
        
        print(f"   🎯 Total de combinações possíveis: {total_combinations:,}")
        print(f"   🎪 Probabilidade de acertar: 1 em {total_combinations:,}")
        print(f"   📊 Probabilidade percentual: {specific_prob * 100:.10f}%")
        
        print("\n🔢 ANÁLISE POR NÚMERO:")
        number_analysis = self.probability_analyzer.probability_specific_number(self.historical_data)
        if 'probabilidades_por_numero' in number_analysis:
            # Mostrar os 5 mais e menos frequentes
            probs = number_analysis['probabilidades_por_numero']
            sorted_by_freq = sorted(probs.items(), key=lambda x: x[1]['frequencia'], reverse=True)
            
            print("   🔥 5 números mais frequentes:")
            for i, (num, data) in enumerate(sorted_by_freq[:5], 1):
                freq = data['frequencia']
                prob = data['probabilidade_empirica_percent']
                print(f"      {i}. Número {num:2d}: {freq:3d} vezes ({prob:.2f}%)")
            
            print("   ❄️ 5 números menos frequentes:")
            for i, (num, data) in enumerate(sorted_by_freq[-5:], 1):
                freq = data['frequencia']
                prob = data['probabilidade_empirica_percent']
                print(f"      {i}. Número {num:2d}: {freq:3d} vezes ({prob:.2f}%)")
        
        print("\n⚖️ ANÁLISE PAR/ÍMPAR:")
        even_odd = self.probability_analyzer.probability_even_odd(self.historical_data)
        print("   📊 Distribuições mais prováveis:")
        
        # Ordenar por probabilidade
        sorted_distributions = sorted(even_odd.items(), 
                                    key=lambda x: x[1]['probabilidade_percent'], 
                                    reverse=True)
        
        for i, (dist, data) in enumerate(sorted_distributions[:5], 1):
            prob_teor = data['probabilidade_percent']
            prob_emp = data.get('freq_empirica_percent', 0)
            print(f"      {i}. {dist}: {prob_teor:.2f}% (teórica) | {prob_emp:.2f}% (observada)")
        
        print("\n💰 ANÁLISE DE INVESTIMENTO:")
        current_cost = self.probability_analyzer.get_cost_per_game()
        print(f"   💸 Valor atual do jogo: R$ {current_cost:.2f}")
        investment = self.probability_analyzer.calculate_investment_analysis(100)
        print(f"   💸 Para 100 jogos (R$ {investment['investimento_total']:.2f}):")
        print(f"   🎯 Retorno esperado: R$ {investment['retorno_esperado']['total']:.2f}")
        print(f"   📈 ROI esperado: {investment['analise_roi']['roi_percent']:.2f}%")
        print(f"   🎰 Jogos necessários para sena esperada: {investment['analise_roi']['jogos_para_sena_esperada']:,.0f}")
    
    def game_theory_analysis(self):
        """Executa análise de teoria de jogos e estratégias."""
        self.print_header("TEORIA DE JOGOS E ESTRATÉGIAS")
        
        if not self.load_data():
            return
        
        try:
            # Perguntar quantas dezenas o jogador quer jogar
            print("🎲 Configuração da Estratégia")
            print("=" * 40)
            print("A Mega Sena permite jogar de 6 a 15 números.")
            print("Mais números = mais chances, mas custa mais caro.")
            print()
            
            while True:
                try:
                    dezenas_str = input("🎯 Quantas dezenas você gostaria de jogar? (6-15): ").strip()
                    dezenas = int(dezenas_str)
                    
                    if 6 <= dezenas <= 15:
                        break
                    else:
                        self.print_colored("❌ Número inválido! Digite um valor entre 6 e 15.", "red")
                        
                except ValueError:
                    self.print_colored("❌ Por favor, digite um número válido!", "red")
            
            print(f"\n✅ Configurado para jogar com {dezenas} números")
            
            # Calcular custo do jogo
            cost_info = self.probability_analyzer.calculate_game_cost(dezenas)
            if cost_info:
                print(f"💰 Custo total: R$ {cost_info['total_cost']:.2f}")
                print(f"📊 Número de jogos: {cost_info['combinations']:,}")
                if cost_info['combinations'] > 1:
                    print(f"💡 Suas chances melhoram {cost_info['combinations']}x comparado ao jogo simples!")
                print()
            
            print("🎲 Executando análise de teoria de jogos...")
            print("📊 Esta análise pode levar alguns minutos...")
            print()
            
            # Configurar o analisador com o número de dezenas escolhido
            self.game_theory_analyzer.target_numbers = dezenas
            
            # Gerar relatório completo
            report = self.game_theory_analyzer.generate_game_theory_report(self.historical_data)
            
            # Exibir resumo executivo
            summary = report['summary']
            self.print_colored("📋 RESUMO EXECUTIVO:", "cyan")
            print(f"   📊 Sorteios analisados: {summary['total_sorteios_analisados']:,}")
            print(f"   🎯 Estratégias geradas: {summary['numero_estrategias_geradas']}")
            print(f"   📈 Melhor Sharpe Ratio: {summary['melhor_portfolio_sharpe']:.3f}")
            print(f"   🏆 Recomendação: {summary['estrategia_recomendada']}")
            print()
            
            # Estratégias otimizadas
            self.print_colored("🎯 ESTRATÉGIAS OTIMIZADAS:", "cyan")
            for name, strategy in report['optimal_strategies'].items():
                print(f"   📊 {name.replace('_', ' ').title()}: {strategy['numbers']}")
                print(f"      📝 {strategy['description']}")
                if 'correlation_score' in strategy:
                    print(f"      📈 Score correlação: {strategy['correlation_score']:.3f}")
                print()
            
            # Equilíbrio de Nash
            self.print_colored("⚖️ EQUILÍBRIO DE NASH:", "cyan")
            for player, strategy in report['nash_equilibrium'].items():
                print(f"   🎯 Jogador {player}: {strategy['numbers']}")
                print(f"      📊 Utilidade: {strategy['utility']:.3f}")
                weights = strategy['strategy_weights']
                print(f"      ⚖️ Pesos: Freq={weights['freq_weight']}, Corr={weights['corr_weight']}")
                print()
            
            # Estratégia Minimax
            minimax = report['minimax_strategy']
            self.print_colored("🛡️ ESTRATÉGIA MINIMAX (Menor Risco):", "cyan")
            print(f"   📊 Números: {minimax['numbers']}")
            print(f"   ⚠️ Risco máximo: {minimax['max_risk']:.3f}")
            print(f"   📝 {minimax['description']}")
            print()
            
            # Portfolio otimizado
            if report['portfolio_optimization']:
                self.print_colored("💼 PORTFÓLIOS OTIMIZADOS:", "cyan")
                for i, portfolio in enumerate(report['portfolio_optimization'][:3]):
                    print(f"   📈 Portfólio #{portfolio['combination']}: {portfolio['numbers']}")
                    print(f"      📊 Retorno esperado: {portfolio['expected_return']:.3f}")
                    print(f"      ⚠️ Risco: {portfolio['risk']:.3f}")
                    print(f"      📈 Sharpe Ratio: {portfolio['sharpe_ratio']:.3f}")
                    print()
            
            # Estratégia por clusters
            cluster = report['cluster_strategy']
            self.print_colored("🎯 ESTRATÉGIA POR CLUSTERS:", "cyan")
            print(f"   📊 Números: {cluster['numbers']}")
            print(f"   🔄 Clusters utilizados: {cluster['n_clusters']}")
            print(f"   📝 {cluster['description']}")
            print()
            
            # Análise de correlações
            correlations = report['correlation_insights']
            if correlations:
                self.print_colored("🔗 INSIGHTS DE CORRELAÇÃO:", "cyan")
                print(f"   📊 Correlação média: {correlations['average_correlation']:.4f}")
                print(f"   📏 Desvio padrão: {correlations['correlation_std']:.4f}")
                
                print("   🔴 Pares mais correlacionados:")
                for pair_data in correlations['most_positively_correlated'][-3:]:
                    pair, corr = pair_data['pair'], pair_data['correlation']
                    print(f"      📊 {pair[0]}-{pair[1]}: {corr:.4f}")
                
                print("   🔵 Pares menos correlacionados:")
                for pair_data in correlations['most_negatively_correlated'][:3]:
                    pair, corr = pair_data['pair'], pair_data['correlation']
                    print(f"      📊 {pair[0]}-{pair[1]}: {corr:.4f}")
                print()
            
            # Comparação de estratégias
            comparison = report['strategy_comparison']
            self.print_colored("🏆 RECOMENDAÇÃO FINAL:", "cyan")
            recommendation = comparison['recommendation']
            print(f"   🎯 Estratégia recomendada: {recommendation['recommended_strategy']}")
            print(f"   📊 Números: {recommendation['recommended_numbers']}")
            max_score = recommendation.get('max_score', 17)
            print(f"   ⭐ Score: {recommendation['score']:.1f}/{max_score}")
            print(f"   📝 Critério: {recommendation['reasoning']}")
            print()
            
            # Diversidade entre estratégias
            total_unique = comparison['total_unique_numbers']
            print(f"   🌟 Total de números únicos nas estratégias: {total_unique}")
            print()
            
            # Informações do jogo escolhido
            if dezenas > 6:
                self.print_colored("💡 DICA PARA SEU JOGO:", "yellow")
                recommended_numbers = recommendation['recommended_numbers']
                if len(recommended_numbers) >= dezenas:
                    suggested = recommended_numbers[:dezenas]
                else:
                    # Completar com números adicionais das outras estratégias
                    all_strategy_numbers = set()
                    for strategy_numbers in comparison['strategies'].values():
                        all_strategy_numbers.update(strategy_numbers)
                    remaining = list(all_strategy_numbers - set(recommended_numbers))
                    suggested = recommended_numbers + remaining[:dezenas - len(recommended_numbers)]
                
                print(f"   🎲 Para {dezenas} números, sugerimos: {sorted(suggested[:dezenas])}")
                print(f"   💰 Custo: R$ {cost_info['total_cost']:.2f}")
                print(f"   🎯 {cost_info['combinations']:,} combinações diferentes")
                print()
            
            # Gerar gráficos
            self.print_colored("📊 GRÁFICOS GERADOS:", "cyan")
            try:
                plots = self.game_theory_analyzer.create_game_theory_plots()
                if plots:
                    for plot in plots:
                        filename = plot.split('\\')[-1] if '\\' in plot else plot.split('/')[-1]
                        print(f"   📈 {filename}")
                    print(f"✅ {len(plots)} gráficos salvos em data/plots/game_theory/")
                else:
                    print("   ⚠️ Nenhum gráfico foi gerado")
            except Exception as e:
                print(f"   ⚠️ Erro ao gerar gráficos: {e}")
            
        except Exception as e:
            self.print_colored(f"❌ Erro na análise de teoria de jogos: {e}", "red")
            import traceback
            traceback.print_exc()

    def time_series_analysis(self):
        """Executa análise de séries temporais."""
        self.print_header("ANÁLISE DE SÉRIES TEMPORAIS")
        
        if not self.load_data():
            return
        
        print("🕒 Executando análise temporal avançada...")
        print("📊 Esta análise pode levar alguns minutos...")
        
        try:
            # Gerar relatório completo de séries temporais
            report = self.time_series_analyzer.generate_time_series_report(self.historical_data)
            
            # Mostrar resumo executivo
            summary = report['summary']
            print(f"\n📋 RESUMO EXECUTIVO:")
            print(f"   📊 Sorteios analisados: {summary['total_sorteios_analisados']:,}")
            print(f"   📅 Período: {summary['periodo_analise']['inicio']} a {summary['periodo_analise']['fim']}")
            print(f"   📈 Tendência geral: {summary['tendencia_geral']}")
            print(f"   🔄 Sazonalidade detectada: {'✅ Sim' if summary['sazonalidade_detectada'] else '❌ Não'}")
            print(f"   ⚠️ Outliers detectados: {summary['outliers_detectados']}")
            print(f"   📊 Qualidade da decomposição: {summary['qualidade_decomposicao']}")
            
            # Análise de decomposição
            decomp = report['decomposition']
            print(f"\n🧬 DECOMPOSIÇÃO TEMPORAL:")
            print(f"   📈 Inclinação da tendência: {decomp['trend_slope']:.4f}")
            print(f"   🔄 Força sazonal: {decomp['seasonal_strength']:.3f}")
            print(f"   📊 Nível de ruído: {decomp['noise_level']:.2f}")
            
            # Análise de tendências
            trends = report['trend_analysis']
            print(f"\n📈 ANÁLISE DE TENDÊNCIAS:")
            for metric, data in trends.items():
                if 'trend_direction' in data:
                    direction = data['trend_direction']
                    strength = data.get('trend_strength', 0)
                    significant = data.get('significant_trend', False)
                    sig_icon = "✅" if significant else "❌"
                    
                    metric_names = {
                        'sum_numbers': 'Soma dos números',
                        'max_number': 'Número máximo',
                        'even_count': 'Contagem de pares',
                        'range_numbers': 'Amplitude'
                    }
                    
                    print(f"   📊 {metric_names.get(metric, metric)}: {direction} (força: {strength:.3f}) {sig_icon}")
            
            # Análise sazonal
            seasonal = report['seasonal_analysis']
            if 'summary' in seasonal:
                season_summary = seasonal['summary']
                print(f"\n🗓️ PADRÕES SAZONAIS:")
                print(f"   📈 Mês com maior soma média: {season_summary['highest_sum_month']}")
                print(f"   📉 Mês com menor soma média: {season_summary['lowest_sum_month']}")
                print(f"   📊 Mês mais variável: {season_summary['most_variable_month']}")
                print(f"   📏 Mês menos variável: {season_summary['least_variable_month']}")
            
            # Detecção de ciclos
            cycles = report['cycles_and_patterns']
            print(f"\n🔄 DETECÇÃO DE CICLOS:")
            cycle_found = False
            for metric, data in cycles.items():
                if data['dominant_periods']:
                    periods = data['dominant_periods'][:3]  # Top 3
                    print(f"   📊 {metric}: períodos dominantes {[f'{p:.1f}' for p in periods]} semanas")
                    cycle_found = True
            
            if not cycle_found:
                print("   📊 Nenhum ciclo dominante detectado nos dados")
            
            # Anomalias
            anomalies = report['anomaly_detection']
            print(f"\n⚠️ DETECÇÃO DE ANOMALIAS:")
            total_outliers = sum(data['outlier_count'] for data in anomalies.values())
            total_extremes = sum(data['extreme_count'] for data in anomalies.values())
            
            print(f"   📊 Total de outliers: {total_outliers}")
            print(f"   🔴 Anomalias extremas: {total_extremes}")
            
            if total_outliers > 0:
                print(f"   📈 Percentual de outliers: {(total_outliers / len(self.historical_data)) * 100:.2f}%")
            
            # Gráficos gerados
            plots = report['generated_plots']
            if plots:
                print(f"\n📊 GRÁFICOS GERADOS:")
                for plot in plots:
                    filename = plot.split('\\')[-1] if '\\' in plot else plot.split('/')[-1]
                    print(f"   📈 {filename}")
                self.print_colored(f"✅ {len(plots)} gráficos salvos em data/plots/time_series/", "green")
            else:
                print(f"\n📊 Gráficos não puderam ser gerados (verifique dependências)")
            
            # Qualidade dos dados
            data_quality = report['data_quality']
            print(f"\n📋 QUALIDADE DOS DADOS:")
            print(f"   ✅ Completude: {data_quality['completeness'] * 100:.1f}%")
            print(f"   📊 Consistência: {data_quality['consistency']}")
            print(f"   📅 Cobertura temporal: {data_quality['temporal_coverage']}")
            
        except Exception as e:
            self.print_colored(f"❌ Erro na análise temporal: {e}", "red")
            print("💡 Dica: Verifique se pandas e matplotlib estão instalados")
    
    def configure_game_cost(self):
        """Configura o valor atual do jogo da Mega Sena."""
        self.print_header("CONFIGURAÇÃO DO VALOR DO JOGO")
        
        current_cost = self.probability_analyzer.get_cost_per_game()
        print(f"💰 Valor atual do jogo: R$ {current_cost:.2f}")
        print()
        
        try:
            new_cost_input = input("💸 Digite o novo valor do jogo (ou ENTER para manter atual): R$ ").strip()
            
            if new_cost_input == "":
                self.print_colored(f"✅ Mantendo valor atual: R$ {current_cost:.2f}", "blue")
                return
            
            # Tentar converter para float
            new_cost = float(new_cost_input.replace(',', '.'))
            
            if new_cost <= 0:
                self.print_colored("❌ O valor deve ser maior que zero!", "red")
                return
            
            # Configurar o novo valor
            self.probability_analyzer.set_cost_per_game(new_cost)
            self.print_colored(f"✅ Valor do jogo atualizado para: R$ {new_cost:.2f}", "green")
            
            # Mostrar impacto da mudança
            print(f"\n📊 IMPACTO DA MUDANÇA:")
            print(f"   💰 Valor anterior: R$ {current_cost:.2f}")
            print(f"   💰 Valor atual: R$ {new_cost:.2f}")
            
            if new_cost > current_cost:
                diff_percent = ((new_cost - current_cost) / current_cost) * 100
                print(f"   📈 Aumento: {diff_percent:.1f}%")
            elif new_cost < current_cost:
                diff_percent = ((current_cost - new_cost) / current_cost) * 100
                print(f"   📉 Redução: {diff_percent:.1f}%")
            
            # Mostrar exemplo de investimento com novo valor
            print(f"\n💡 EXEMPLO (100 jogos):")
            investment_example = self.probability_analyzer.calculate_investment_analysis(100)
            print(f"   💸 Investimento total: R$ {investment_example['investimento_total']:.2f}")
            print(f"   🎯 Retorno esperado: R$ {investment_example['retorno_esperado']['total']:.2f}")
            print(f"   📊 ROI esperado: {investment_example['analise_roi']['roi_percent']:.2f}%")
            
        except ValueError:
            self.print_colored("❌ Valor inválido! Digite um número válido (ex: 6.00)", "red")
        except Exception as e:
            self.print_colored(f"❌ Erro ao configurar valor: {e}", "red")
    
    def descriptive_statistics(self):
        """Executa análise de estatísticas descritivas."""
        self.print_header("ESTATÍSTICAS DESCRITIVAS")
        
        if not self.load_data():
            return
        
        print("🔍 Executando análise de frequências...")
        freq_analysis = self.statistics.frequency_analysis(self.historical_data)
        
        if "resumo_geral" in freq_analysis:
            summary = freq_analysis['resumo_geral']
            print("\n📊 RESUMO ESTATÍSTICO:")
            print(f"   📈 Média de frequência: {summary['media_frequencia']:.2f}")
            print(f"   📊 Mediana de frequência: {summary['mediana_frequencia']:.2f}")
            print(f"   📏 Desvio padrão: {summary['desvio_padrao']:.2f}")
            print(f"   🎯 Frequência esperada: {summary['frequencia_esperada']:.2f}")
            
            most_freq = summary['numero_mais_frequente']
            least_freq = summary['numero_menos_frequente']
            print(f"   🔥 Mais frequente: {most_freq[0]} ({most_freq[1]} vezes)")
            print(f"   ❄️ Menos frequente: {least_freq[0]} ({least_freq[1]} vezes)")
        
        print("\n⏰ ANÁLISE DE ATRASOS:")
        delay_analysis = self.statistics.delay_analysis(self.historical_data)
        
        if "estatisticas_gerais" in delay_analysis:
            delay_stats = delay_analysis['estatisticas_gerais']
            print(f"   📊 Atraso médio geral: {delay_stats['atraso_medio_geral']:.2f} sorteios")
            print(f"   📈 Maior atraso histórico: {delay_stats['atraso_maximo_historico']} sorteios")
            print(f"   🎯 Atraso médio atual: {delay_stats['atraso_medio_atual']:.2f} sorteios")
            print(f"   🔥 Número com maior atraso atual: {delay_stats['numero_maior_atraso_atual']} ({delay_stats['maior_atraso_atual']} sorteios)")
        
        print("\n🔍 ANÁLISE DE PADRÕES:")
        pattern_analysis = self.statistics.pattern_analysis(self.historical_data)
        
        if "estatisticas_padroes" in pattern_analysis:
            patterns = pattern_analysis['estatisticas_padroes']
            print(f"   🔗 Média de números consecutivos: {patterns['media_consecutivos']:.2f}")
            print(f"   📊 Soma média dos sorteios: {patterns['soma_media']:.2f}")
            print(f"   📏 Dispersão média: {patterns['dispersao_media']:.2f}")
            print(f"   🎯 Frequência primeira dezena: {patterns['freq_primeira_dezena']:.1f}%")
            print(f"   🎯 Frequência última dezena: {patterns['freq_ultima_dezena']:.1f}%")
        
        # Gerar gráficos
        print("\n📊 Gerando gráficos...")
        try:
            freq_plot = self.statistics.create_frequency_histogram(self.historical_data)
            delay_plot = self.statistics.create_delay_analysis_plot(self.historical_data)
            pattern_plots = self.statistics.create_pattern_analysis_plots(self.historical_data)
            
            self.print_colored("✅ Gráficos salvos na pasta data/plots/", "green")
            print(f"   📊 Histograma de frequência: {freq_plot}")
            print(f"   ⏰ Análise de atrasos: {delay_plot}")
            print(f"   🔍 Análise de padrões: {', '.join(pattern_plots)}")
        except Exception as e:
            self.print_colored(f"⚠️ Erro ao gerar gráficos: {e}", "yellow")
    
    def advanced_analysis(self):
        """Executa análise probabilística avançada."""
        self.print_header("ANÁLISE PROBABILÍSTICA AVANÇADA")
        
        if not self.load_data():
            return
        
        print("🎲 SIMULAÇÃO MONTE CARLO:")
        print("Escolha o número de simulações:")
        print("1. 10,000 (rápido)")
        print("2. 100,000 (moderado)")
        print("3. 1,000,000 (lento, mais preciso)")
        
        try:
            choice = input("Opção (1-3): ").strip()
            sim_counts = {"1": 10000, "2": 100000, "3": 1000000}
            num_sims = sim_counts.get(choice, 10000)
            
            print("Estratégias disponíveis:")
            print("1. Aleatória")
            print("2. Números mais frequentes")
            print("3. Números menos frequentes")
            print("4. Balanceada")
            
            strategy_choice = input("Estratégia (1-4): ").strip()
            strategies = {"1": "random", "2": "most_frequent", "3": "least_frequent", "4": "balanced"}
            strategy = strategies.get(strategy_choice, "random")
            
            monte_carlo = self.advanced_analytics.monte_carlo_simulation(num_sims, strategy)
            
            print(f"\n🎯 RESULTADOS DA SIMULAÇÃO ({strategy}):")
            print(f"   🎲 Simulações executadas: {monte_carlo['simulacoes_executadas']:,}")
            print(f"   🏆 Melhor resultado: {monte_carlo['melhor_resultado']} acertos")
            print(f"   📊 Média de acertos: {monte_carlo['estatisticas']['media_acertos']:.3f}")
            print(f"   ⏱️ Tempo de execução: {monte_carlo['tempo_execucao']:.2f}s")
            
            print("\n📊 DISTRIBUIÇÃO DE ACERTOS:")
            for acertos in range(7):
                count = monte_carlo['resultados_por_acerto'][acertos]
                percentage = (count / num_sims) * 100
                prob_teorica = monte_carlo['estatisticas']['probabilidades_teoricas'][acertos] * 100
                print(f"   {acertos} acertos: {count:,} vezes ({percentage:.3f}% obs. vs {prob_teorica:.3f}% teórica)")
        
        except KeyboardInterrupt:
            self.print_colored("❌ Simulação cancelada pelo usuário.", "yellow")
        except Exception as e:
            self.print_colored(f"❌ Erro na simulação: {e}", "red")
        
        print("\n🔬 TESTES DE ALEATORIEDADE:")
        randomness = self.advanced_analytics.randomness_tests(self.historical_data)
        
        runs_test = randomness['teste_runs']
        print(f"   🏃 Teste de runs: {'✅ Aleatório' if runs_test['aleatorio'] else '❌ Não aleatório'}")
        
        autocorr = randomness['teste_autocorrelacao']
        print(f"   🔗 Autocorrelação: {'✅ Independente' if autocorr['independente'] else '⚠️ Possível dependência'}")
        print(f"      📊 Máxima autocorrelação: {autocorr['max_autocorrelacao']:.4f}")
        
        print("\n🎯 TESTE DE UNIFORMIDADE:")
        uniformity = self.advanced_analytics.uniform_distribution_test(self.historical_data)
        if "interpretacao" in uniformity:
            interpretation = uniformity['interpretacao']
            print(f"   📊 Conclusão: {interpretation['conclusao']}")
            print(f"   📈 Nível de uniformidade: {interpretation['nivel_uniformidade']}")
    
    def analyze_prediction_history(self, predictions: List[List[int]]) -> Dict:
        """
        Analisa se as combinações e números das previsões já foram sorteados.
        
        Args:
            predictions: Lista de previsões (cada previsão é uma lista de 6 números)
            
        Returns:
            Dict com análise detalhada das previsões
        """
        analysis = {
            'total_predictions': len(predictions),
            'combinations_analysis': [],
            'numbers_analysis': {},
            'summary': {
                'combinations_already_drawn': 0,
                'combinations_never_drawn': 0,
                'most_drawn_numbers': [],
                'never_drawn_numbers': []
            }
        }
        
        # Converter dados históricos para formato de conjuntos para comparação rápida
        historical_combinations = []
        all_drawn_numbers = set()
        
        for sorteio in self.historical_data:
            # Verificar se é dicionário ou lista
            if isinstance(sorteio, dict) and 'numeros' in sorteio:
                numeros = sorteio['numeros']
            elif isinstance(sorteio, list):
                numeros = sorteio
            else:
                continue  # Pular se formato não reconhecido
                
            combination = set(numeros)
            historical_combinations.append(combination)
            all_drawn_numbers.update(combination)
        
        # Contar frequência de cada número nos dados históricos
        number_frequency = {}
        for sorteio in self.historical_data:
            # Verificar se é dicionário ou lista
            if isinstance(sorteio, dict) and 'numeros' in sorteio:
                numeros = sorteio['numeros']
            elif isinstance(sorteio, list):
                numeros = sorteio
            else:
                continue  # Pular se formato não reconhecido
                
            for num in numeros:
                number_frequency[num] = number_frequency.get(num, 0) + 1
        
        # Analisar cada previsão
        for i, prediction in enumerate(predictions, 1):
            pred_set = set(prediction)
            
            # Verificar se a combinação exata já foi sorteada
            combination_drawn = pred_set in historical_combinations
            
            # Contar quantos números da previsão já foram sorteados
            drawn_numbers = pred_set.intersection(all_drawn_numbers)
            never_drawn = pred_set - all_drawn_numbers
            
            # Análise de frequência dos números da previsão
            prediction_frequencies = {}
            for num in prediction:
                prediction_frequencies[num] = number_frequency.get(num, 0)
            
            combination_analysis = {
                'prediction_number': i,
                'numbers': sorted(prediction),
                'combination_already_drawn': combination_drawn,
                'drawn_numbers_count': len(drawn_numbers),
                'drawn_numbers': sorted(list(drawn_numbers)),
                'never_drawn_count': len(never_drawn),
                'never_drawn_numbers': sorted(list(never_drawn)),
                'frequencies': prediction_frequencies,
                'total_frequency': sum(prediction_frequencies.values()),
                'average_frequency': sum(prediction_frequencies.values()) / 6
            }
            
            analysis['combinations_analysis'].append(combination_analysis)
            
            # Atualizar sumário
            if combination_drawn:
                analysis['summary']['combinations_already_drawn'] += 1
            else:
                analysis['summary']['combinations_never_drawn'] += 1
        
        # Análise geral dos números
        from collections import Counter
        all_predicted_numbers = [num for pred in predictions for num in pred]
        predicted_counter = Counter(all_predicted_numbers)
        
        for num, count in predicted_counter.items():
            historical_freq = number_frequency.get(num, 0)
            analysis['numbers_analysis'][num] = {
                'predicted_times': count,
                'historical_frequency': historical_freq,
                'ever_drawn': num in all_drawn_numbers
            }
        
        # Números mais e menos frequentes nas previsões
        most_predicted = predicted_counter.most_common(10)
        analysis['summary']['most_predicted_numbers'] = most_predicted
        
        # Números que nunca foram sorteados
        never_drawn_in_predictions = []
        for num in range(1, 61):
            if num not in all_drawn_numbers and num in predicted_counter:
                never_drawn_in_predictions.append(num)
        
        analysis['summary']['never_drawn_numbers'] = never_drawn_in_predictions
        
        return analysis

    def generate_predictions(self):
        """Gera previsões para próximos sorteios."""
        self.print_header("GERADOR DE PREVISÕES")
        
        if not self.load_data():
            return
        
        # Perguntar quantas dezenas o usuário quer jogar
        print("🔮 Configuração das Previsões")
        print("=" * 40)
        print("A Mega Sena permite jogar de 6 a 15 números.")
        print("Mais números = mais chances, mas custa mais caro.")
        print()
        
        while True:
            try:
                dezenas_str = input("🎯 Quantas dezenas por jogo? (6-15): ").strip()
                dezenas = int(dezenas_str)
                
                if 6 <= dezenas <= 15:
                    break
                else:
                    self.print_colored("❌ Número inválido! Digite um valor entre 6 e 15.", "red")
                    
            except ValueError:
                self.print_colored("❌ Por favor, digite um número válido!", "red")
        
        print(f"\n✅ Configurado para gerar jogos com {dezenas} números")
        
        # Calcular custo do jogo
        cost_info = self.probability_analyzer.calculate_game_cost(dezenas)
        if cost_info:
            print(f"💰 Custo por jogo: R$ {cost_info['total_cost']:.2f}")
            print(f"📊 Combinações por jogo: {cost_info['combinations']:,}")
            if cost_info['combinations'] > 1:
                print(f"💡 Cada jogo tem {cost_info['combinations']}x mais chances que o jogo simples!")
            print()
        
        print("🔮 MÉTODOS DE PREVISÃO:")
        print("1. 🎲 Aleatório ponderado (baseado em frequências)")
        print("2. 🔥 Números quentes (mais frequentes recentemente)")
        print("3. ❄️ Números frios (maior atraso)")
        print("4. ⚖️ Balanceado (combinação de estratégias)")
        
        try:
            method_choice = input("Método (1-4): ").strip()
            methods = {"1": "weighted_random", "2": "hot_numbers", "3": "cold_numbers", "4": "balanced"}
            method = methods.get(method_choice, "balanced")
            
            num_predictions = int(input("Quantas previsões gerar (1-10)? ") or "5")
            num_predictions = max(1, min(10, num_predictions))
            
            # Configurar o número de dezenas no analisador avançado
            if hasattr(self.advanced_analytics, 'set_target_numbers'):
                self.advanced_analytics.set_target_numbers(dezenas)
            
            predictions = self.advanced_analytics.generate_predictions(
                self.historical_data, method, num_predictions, target_numbers=dezenas
            )
            
            method_names = {
                "weighted_random": "Aleatório Ponderado",
                "hot_numbers": "Números Quentes",
                "cold_numbers": "Números Frios",
                "balanced": "Balanceado"
            }
            
            print(f"\n🎯 PREVISÕES - MÉTODO: {method_names[method]}")
            print(f"🎲 Jogos com {dezenas} números cada")
            print("=" * 50)
            
            for i, prediction in enumerate(predictions, 1):
                numbers_str = " - ".join(f"{num:02d}" for num in prediction)
                print(f"   🎫 Jogo {i}: {numbers_str}")
            
            # Mostrar custo total
            if cost_info:
                total_cost = cost_info['total_cost'] * num_predictions
                total_combinations = cost_info['combinations'] * num_predictions
                print(f"\n💰 RESUMO FINANCEIRO:")
                print(f"   💸 Custo por jogo: R$ {cost_info['total_cost']:.2f}")
                print(f"   💳 Custo total ({num_predictions} jogos): R$ {total_cost:.2f}")
                print(f"   🎯 Total de combinações: {total_combinations:,}")
                print(f"   📈 Fator de melhoria: {cost_info['combinations']}x por jogo")
            
            # Executar análise histórica das previsões
            print(f"\n📊 ANÁLISE HISTÓRICA DAS PREVISÕES:")
            history_analysis = self.analyze_prediction_history(predictions)
            
            # Mostrar se alguma combinação já foi sorteada
            combinations_drawn = history_analysis['summary']['combinations_already_drawn']
            combinations_never = history_analysis['summary']['combinations_never_drawn']
            
            print(f"   🎯 Combinações já sorteadas: {combinations_drawn}/{num_predictions}")
            print(f"   🆕 Combinações inéditas: {combinations_never}/{num_predictions}")
            
            if combinations_drawn > 0:
                self.print_colored("   ⚠️  ATENÇÃO: Algumas combinações já foram sorteadas!", "yellow")
                        
            
            print(f"\n📊 RESUMO GERAL:")
            all_predicted = [num for pred in predictions for num in pred]
            most_common = Counter(all_predicted).most_common(5)
            
            print("   🔢 Números mais sugeridos:")
            for num, count in most_common:
                historical_freq = history_analysis['numbers_analysis'][num]['historical_frequency']
                ever_drawn = history_analysis['numbers_analysis'][num]['ever_drawn']
                status = "✅" if ever_drawn else "🆕"
                print(f"      {status} {num:02d}: {count} vez(es) nas previsões, {historical_freq} vezes na história")
            
            # Análise par/ímpar das previsões
            print(f"\n🎲 COMPOSIÇÃO DAS PREVISÕES:")
            for i, prediction in enumerate(predictions, 1):
                pares = sum(1 for n in prediction if n % 2 == 0)
                impares = 6 - pares
                soma = sum(prediction)
                print(f"   🎲 Jogo {i}: {pares}P/{impares}I, Soma: {soma}")
            
            # Mostrar números inéditos se houver
            never_drawn_in_pred = history_analysis['summary']['never_drawn_numbers']
            if never_drawn_in_pred:
                never_drawn_str = " - ".join(f"{n:02d}" for n in sorted(never_drawn_in_pred))
                self.print_colored(f"\n🆕 NÚMEROS INÉDITOS nas previsões: {never_drawn_str}", "cyan")
                self.print_colored("   💡 Estes números nunca foram sorteados na história da Mega Sena!", "cyan")
        
        except ValueError:
            self.print_colored("❌ Entrada inválida.", "red")
        except Exception as e:
            self.print_colored(f"❌ Erro ao gerar previsões: {e}", "red")
    
    def complete_report(self):
        """Gera relatório completo."""
        self.print_header("RELATÓRIO COMPLETO")
        
        if not self.load_data():
            return
        
        print("📝 Gerando relatório completo... Isso pode levar alguns minutos.")
        
        try:
            # Executar todas as análises
            print("\n🔍 1/4 - Análise de probabilidades...")
            prob_analysis = self.probability_analyzer.probability_specific_number(self.historical_data)
            
            print("📊 2/4 - Estatísticas descritivas...")
            complete_stats = self.statistics.generate_complete_report(self.historical_data)
            
            print("🎲 3/4 - Simulação Monte Carlo...")
            monte_carlo = self.advanced_analytics.monte_carlo_simulation(50000, "balanced")
            
            print("🔬 4/4 - Testes avançados...")
            uniformity = self.advanced_analytics.uniform_distribution_test(self.historical_data)
            randomness = self.advanced_analytics.randomness_tests(self.historical_data)
            
            # Salvar relatório
            report_path = os.path.join("data", f"relatorio_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("RELATÓRIO COMPLETO - ANÁLISE MEGA SENA\n")
                f.write("=" * 50 + "\n")
                f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total de sorteios analisados: {len(self.historical_data)}\n\n")
                
                # Adicionar todas as análises ao relatório
                f.write("ANÁLISE DE PROBABILIDADES\n")
                f.write("-" * 30 + "\n")
                if 'resumo_geral' in prob_analysis:
                    for key, value in prob_analysis['resumo_geral'].items():
                        f.write(f"{key}: {value}\n")
                
                f.write("\nESTATÍSTICAS DESCRITIVAS\n")
                f.write("-" * 30 + "\n")
                # Adicionar estatísticas detalhadas...
                
                f.write("\nSIMULAÇÃO MONTE CARLO\n")
                f.write("-" * 30 + "\n")
                f.write(f"Simulações: {monte_carlo['simulacoes_executadas']:,}\n")
                f.write(f"Melhor resultado: {monte_carlo['melhor_resultado']} acertos\n")
                f.write(f"Média de acertos: {monte_carlo['estatisticas']['media_acertos']:.3f}\n")
            
            self.print_colored(f"✅ Relatório salvo em: {report_path}", "green")
            
        except Exception as e:
            self.print_colored(f"❌ Erro ao gerar relatório: {e}", "red")
    
    def show_data_info(self):
        """Mostra informações sobre os dados carregados."""
        self.print_header("INFORMAÇÕES DOS DADOS")
        
        summary = self.collector.get_statistics_summary()
        if summary:
            print("📋 DADOS HISTÓRICOS:")
            print(f"   📊 Total de sorteios: {summary['total_sorteios']}")
            print(f"   🎯 Primeiro sorteio: #{summary['primeiro_sorteio']} em {summary['data_primeiro']}")
            print(f"   🆕 Último sorteio: #{summary['ultimo_sorteio']} em {summary['data_ultimo']}")
            print(f"   🔢 Total de números sorteados: {summary['total_numeros_sorteados']:,}")
            print(f"   🎲 Números únicos utilizados: {summary['numeros_unicos']}")
        
        # Verificar se há dados carregados na memória
        if self.data_loaded:
            print(f"\n💾 DADOS EM MEMÓRIA:")
            print(f"   ✅ {len(self.historical_data)} sorteios carregados")
            print(f"   📂 Arquivos disponíveis:")
            
            data_files = []
            if os.path.exists("data/megasena_historical.json"):
                data_files.append("✅ megasena_historical.json")
            if os.path.exists("data/megasena_historical.csv"):
                data_files.append("✅ megasena_historical.csv")
            
            if data_files:
                for file in data_files:
                    print(f"      {file}")
            else:
                print("      ❌ Nenhum arquivo de dados encontrado")
        else:
            print(f"\n💾 DADOS EM MEMÓRIA:")
            print(f"   ❌ Nenhum dado carregado")
    
    def run(self):
        """Executa o aplicativo principal."""
        while True:
            try:
                self.print_menu()
                choice = input("🎯 Escolha uma opção: ").strip()
                
                if choice == "0":
                    self.print_colored("\n👋 Obrigado por usar o Mega Sena Analyzer!", "green")
                    break
                elif choice == "1":
                    self.update_data()
                elif choice == "2":
                    self.probability_analysis()
                elif choice == "3":
                    self.descriptive_statistics()
                elif choice == "4":
                    self.advanced_analysis()
                elif choice == "5":
                    self.generate_predictions()
                elif choice == "6":
                    self.time_series_analysis()
                elif choice == "7":
                    self.game_theory_analysis()
                elif choice == "8":
                    self.complete_report()
                elif choice == "9":
                    self.show_data_info()
                elif choice == "10":
                    self.configure_game_cost()
                else:
                    self.print_colored("❌ Opção inválida! Tente novamente.", "red")
                
                input("\n⏸️ Pressione ENTER para continuar...")
                
            except KeyboardInterrupt:
                self.print_colored("\n\n👋 Programa encerrado pelo usuário.", "yellow")
                break
            except Exception as e:
                self.print_colored(f"❌ Erro inesperado: {e}", "red")
                input("\n⏸️ Pressione ENTER para continuar...")


def main():
    """Função principal."""
    app = MegaSenaApp()
    app.run()


if __name__ == "__main__":
    main()