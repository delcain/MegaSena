"""
Demonstração das funcionalidades do aplicativo Mega Sena.
Este script demonstra todas as capacidades do sistema.
"""

import sys
import os
sys.path.append('src')

from src.data_collector import MegaSenaDataCollector
from src.probability_analyzer import MegaSenaProbabilityAnalyzer
from src.descriptive_stats import MegaSenaStatistics
from src.advanced_analytics import MegaSenaAdvancedAnalytics


def demo_data_collection():
    """Demonstra coleta de dados."""
    print("🔽 DEMONSTRAÇÃO: COLETA DE DADOS")
    print("=" * 50)
    
    collector = MegaSenaDataCollector()
    
    # Simular alguns dados para demonstração
    sample_draws = {
        1: {'concurso': 1, 'data': '11/03/1996', 'numeros_ordenados': [4, 5, 30, 33, 41, 52], 'acumulado': False},
        2: {'concurso': 2, 'data': '18/03/1996', 'numeros_ordenados': [10, 11, 16, 20, 27, 58], 'acumulado': True},
        3: {'concurso': 3, 'data': '25/03/1996', 'numeros_ordenados': [1, 5, 11, 16, 20, 56], 'acumulado': False}
    }
    
    collector.save_data(sample_draws)
    
    # Mostrar estatísticas
    summary = collector.get_statistics_summary()
    if summary:
        print("📊 Resumo dos dados:")
        print(f"   Total de sorteios: {summary['total_sorteios']}")
        print(f"   Primeiro sorteio: #{summary['primeiro_sorteio']}")
        print(f"   Último sorteio: #{summary['ultimo_sorteio']}")
    
    print("✅ Demonstração de coleta concluída!\n")


def demo_probability_analysis():
    """Demonstra análise probabilística."""
    print("🎲 DEMONSTRAÇÃO: ANÁLISE PROBABILÍSTICA")
    print("=" * 50)
    
    analyzer = MegaSenaProbabilityAnalyzer()
    
    # Dados de exemplo
    sample_data = [
        [4, 5, 30, 33, 41, 52],
        [10, 11, 16, 20, 27, 58],
        [1, 5, 11, 16, 20, 56],
        [7, 12, 31, 33, 42, 51],
        [2, 8, 15, 17, 49, 57]
    ] * 20  # Multiplicar para ter mais dados
    
    print("🎯 Probabilidades básicas:")
    total_combinations = analyzer.total_combinations()
    print(f"   Total de combinações: {total_combinations:,}")
    print(f"   Probabilidade de acerto: 1 em {total_combinations:,}")
    
    print("\n🔢 Análise por número:")
    number_analysis = analyzer.probability_specific_number(sample_data)
    if 'probabilidades_por_numero' in number_analysis:
        probs = number_analysis['probabilidades_por_numero']
        sorted_by_freq = sorted(probs.items(), key=lambda x: x[1]['frequencia'], reverse=True)
        
        print("   Top 5 mais frequentes:")
        for i, (num, data) in enumerate(sorted_by_freq[:5], 1):
            print(f"      {i}. Número {num}: {data['frequencia']} vezes")
    
    print("\n⚖️ Análise par/ímpar:")
    even_odd = analyzer.probability_even_odd(sample_data)
    sorted_distributions = sorted(even_odd.items(), 
                                key=lambda x: x[1]['probabilidade_percent'], 
                                reverse=True)
    
    for i, (dist, data) in enumerate(sorted_distributions[:3], 1):
        prob_teor = data['probabilidade_percent']
        prob_emp = data.get('freq_empirica_percent', 0)
        print(f"   {i}. {dist}: {prob_teor:.2f}% (teórica) | {prob_emp:.2f}% (observada)")
    
    print("\n🎯 Comparação de estratégias:")
    strategies = analyzer.compare_strategies(sample_data)
    for strategy_name, data in list(strategies.items())[:3]:
        print(f"   {strategy_name}: {data['media_acertos']:.2f} acertos médios")
    
    print("✅ Demonstração de probabilidades concluída!\n")


def demo_descriptive_statistics():
    """Demonstra estatísticas descritivas."""
    print("📊 DEMONSTRAÇÃO: ESTATÍSTICAS DESCRITIVAS")
    print("=" * 50)
    
    stats = MegaSenaStatistics()
    
    # Dados de exemplo mais robustos
    sample_data = [
        [4, 5, 30, 33, 41, 52], [10, 11, 16, 20, 27, 58], [1, 5, 11, 16, 20, 56],
        [7, 12, 31, 33, 42, 51], [2, 8, 15, 17, 49, 57], [3, 9, 18, 25, 38, 44],
        [6, 13, 22, 29, 36, 48], [14, 19, 26, 34, 45, 59], [21, 28, 35, 40, 47, 60],
        [23, 24, 32, 37, 43, 46]
    ] * 10  # Multiplicar para mais dados
    
    print("🔍 Análise de frequências:")
    freq_analysis = stats.frequency_analysis(sample_data)
    if "resumo_geral" in freq_analysis:
        summary = freq_analysis['resumo_geral']
        print(f"   Média de frequência: {summary['media_frequencia']:.2f}")
        print(f"   Desvio padrão: {summary['desvio_padrao']:.2f}")
        print(f"   Mais frequente: {summary['numero_mais_frequente']}")
        print(f"   Menos frequente: {summary['numero_menos_frequente']}")
    
    print("\n⏰ Análise de atrasos:")
    delay_analysis = stats.delay_analysis(sample_data)
    if "estatisticas_gerais" in delay_analysis:
        delay_stats = delay_analysis['estatisticas_gerais']
        print(f"   Atraso médio geral: {delay_stats['atraso_medio_geral']:.2f}")
        print(f"   Maior atraso atual: {delay_stats['maior_atraso_atual']}")
        print(f"   Número com maior atraso: {delay_stats['numero_maior_atraso_atual']}")
    
    print("\n🔍 Análise de padrões:")
    pattern_analysis = stats.pattern_analysis(sample_data)
    if "estatisticas_padroes" in pattern_analysis:
        patterns = pattern_analysis['estatisticas_padroes']
        print(f"   Média de números consecutivos: {patterns['media_consecutivos']:.2f}")
        print(f"   Soma média dos sorteios: {patterns['soma_media']:.2f}")
        print(f"   Dispersão média: {patterns['dispersao_media']:.2f}")
    
    print("✅ Demonstração de estatísticas concluída!\n")


def demo_advanced_analytics():
    """Demonstra análise avançada."""
    print("🧬 DEMONSTRAÇÃO: ANÁLISE AVANÇADA")
    print("=" * 50)
    
    analytics = MegaSenaAdvancedAnalytics(seed=42)
    
    # Dados de exemplo
    sample_data = [
        [4, 5, 30, 33, 41, 52], [10, 11, 16, 20, 27, 58], [1, 5, 11, 16, 20, 56],
        [7, 12, 31, 33, 42, 51], [2, 8, 15, 17, 49, 57], [3, 9, 18, 25, 38, 44],
        [6, 13, 22, 29, 36, 48], [14, 19, 26, 34, 45, 59], [21, 28, 35, 40, 47, 60],
        [23, 24, 32, 37, 43, 46]
    ] * 5
    
    print("🎲 Simulação Monte Carlo:")
    monte_carlo = analytics.monte_carlo_simulation(5000, strategy="balanced")
    print(f"   Simulações executadas: {monte_carlo['simulacoes_executadas']:,}")
    print(f"   Melhor resultado: {monte_carlo['melhor_resultado']} acertos")
    print(f"   Média de acertos: {monte_carlo['estatisticas']['media_acertos']:.3f}")
    print(f"   Tempo de execução: {monte_carlo['tempo_execucao']:.2f}s")
    
    print("\n📊 Distribuição de acertos:")
    for acertos in range(4):  # Mostrar apenas os primeiros
        count = monte_carlo['resultados_por_acerto'][acertos]
        percentage = (count / 5000) * 100
        print(f"   {acertos} acertos: {count:,} vezes ({percentage:.2f}%)")
    
    print("\n🔬 Testes de aleatoriedade:")
    randomness = analytics.randomness_tests(sample_data)
    
    runs_test = randomness['teste_runs']
    print(f"   Teste de runs: {'✅ Aleatório' if runs_test['aleatorio'] else '❌ Não aleatório'}")
    
    autocorr = randomness['teste_autocorrelacao']
    print(f"   Autocorrelação: {'✅ Independente' if autocorr['independente'] else '⚠️ Possível dependência'}")
    print(f"   Máxima autocorrelação: {autocorr['max_autocorrelacao']:.4f}")
    
    print("\n🎯 Teste de uniformidade:")
    uniformity = analytics.uniform_distribution_test(sample_data)
    if "interpretacao" in uniformity:
        interpretation = uniformity['interpretacao']
        print(f"   Conclusão: {interpretation['conclusao']}")
        print(f"   Nível de uniformidade: {interpretation['nivel_uniformidade']}")
    
    print("\n🔮 Previsões geradas:")
    predictions = analytics.generate_predictions(sample_data, method="balanced", num_predictions=3)
    for i, prediction in enumerate(predictions, 1):
        numbers_str = " - ".join(f"{num:02d}" for num in prediction)
        print(f"   Previsão {i}: {numbers_str}")
    
    print("✅ Demonstração de análise avançada concluída!\n")


def main():
    """Executa todas as demonstrações."""
    print("🎰 MEGA SENA - DEMONSTRAÇÃO COMPLETA")
    print("=" * 50)
    print("Este script demonstra todas as funcionalidades do aplicativo.")
    print("Os dados utilizados são exemplos para fins de demonstração.\n")
    
    try:
        demo_data_collection()
        demo_probability_analysis()
        demo_descriptive_statistics()
        demo_advanced_analytics()
        
        print("🎉 DEMONSTRAÇÃO COMPLETA!")
        print("=" * 50)
        print("✅ Todas as funcionalidades foram demonstradas com sucesso!")
        print("🚀 Para usar o aplicativo completo, execute: python main.py")
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {e}")
        print("Certifique-se de que todas as dependências estão instaladas.")


if __name__ == "__main__":
    main()