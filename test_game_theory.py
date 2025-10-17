#!/usr/bin/env python3
"""
Teste da nova funcionalidade de Teoria de Jogos e Estratégias.

MIT License - Copyright (c) 2025 delcain
Veja LICENSE para detalhes completos.
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.game_theory_analyzer import MegaSenaGameTheoryAnalyzer
    from src.data_collector import MegaSenaDataCollector
except ImportError as e:
    print(f"Erro ao importar: {e}")
    sys.exit(1)

def test_game_theory_analysis():
    """Testa a análise de teoria de jogos."""
    print("🎲 TESTE - TEORIA DE JOGOS E ESTRATÉGIAS")
    print("=" * 50)
    
    # Carregar dados
    print("📥 Carregando dados históricos...")
    collector = MegaSenaDataCollector()
    
    try:
        historical_data = collector.get_all_numbers()
        if not historical_data:
            print("❌ Nenhum dado encontrado. Execute 'python main.py' e atualize os dados primeiro.")
            return
        
        print(f"✅ {len(historical_data)} sorteios carregados")
        
        # Criar analisador
        analyzer = MegaSenaGameTheoryAnalyzer()
        
        # Teste 1: Preparação dos dados
        print(f"\n🔧 Teste 1: Preparação dos dados estratégicos")
        df = analyzer.prepare_game_theory_data(historical_data[:200])  # Usar subset para teste
        print(f"✅ DataFrame criado com {len(df)} registros")
        print(f"📊 Colunas: {list(df.columns)}")
        
        # Teste 2: Cálculo de correlações
        print(f"\n🔗 Teste 2: Matriz de correlações")
        corr_matrix = analyzer.calculate_number_correlations()
        print(f"✅ Matriz de correlação calculada")
        print(f"   📊 Dimensões: {corr_matrix.shape}")
        print(f"   📈 Correlação máxima: {corr_matrix.max():.4f}")
        print(f"   📉 Correlação mínima: {corr_matrix.min():.4f}")
        
        # Teste 3: Seleção ótima de números
        print(f"\n🎯 Teste 3: Seleção ótima de números")
        optimal_strategies = analyzer.optimal_number_selection('min_correlation')
        print(f"✅ Estratégias otimizadas geradas")
        for name, strategy in optimal_strategies.items():
            print(f"   📊 {name}: {strategy['numbers']}")
            print(f"      📝 {strategy['description']}")
        
        # Teste 4: Equilíbrio de Nash
        print(f"\n⚖️ Teste 4: Análise de equilíbrio de Nash")
        nash_result = analyzer.nash_equilibrium_analysis()
        print(f"✅ Análise de Nash concluída")
        for player, strategy in nash_result.items():
            print(f"   🎯 {player}: {strategy['numbers']}")
            print(f"      📊 Utilidade: {strategy['utility']:.3f}")
        
        # Teste 5: Estratégia Minimax
        print(f"\n🛡️ Teste 5: Estratégia Minimax")
        minimax_result = analyzer.minimax_strategy()
        print(f"✅ Estratégia Minimax calculada")
        print(f"   📊 Números: {minimax_result['numbers']}")
        print(f"   ⚠️ Risco máximo: {minimax_result['max_risk']:.3f}")
        
        # Teste 6: Otimização de portfólio
        print(f"\n💼 Teste 6: Otimização de portfólio")
        portfolios = analyzer.portfolio_optimization(2)  # Apenas 2 para teste
        print(f"✅ {len(portfolios)} portfólios otimizados")
        for portfolio in portfolios:
            print(f"   📈 Portfólio {portfolio['combination']}: {portfolio['numbers']}")
            print(f"      📊 Sharpe Ratio: {portfolio['sharpe_ratio']:.3f}")
        
        # Teste 7: Estratégia por clusters
        print(f"\n🎯 Teste 7: Estratégia por clusters")
        cluster_strategy = analyzer.cluster_based_strategy(4)  # 4 clusters para teste
        print(f"✅ Estratégia por clusters gerada")
        print(f"   📊 Números: {cluster_strategy['numbers']}")
        print(f"   🔄 Clusters: {cluster_strategy['n_clusters']}")
        
        # Teste 8: Gráficos (se possível)
        print(f"\n📊 Teste 8: Geração de gráficos")
        try:
            plots = analyzer.create_game_theory_plots()
            print(f"✅ {len(plots)} gráficos gerados:")
            for plot in plots:
                filename = plot.split('\\')[-1] if '\\' in plot else plot.split('/')[-1]
                print(f"   📈 {filename}")
        except Exception as e:
            print(f"⚠️ Gráficos não puderam ser gerados: {e}")
        
        # Teste 9: Relatório completo
        print(f"\n📋 Teste 9: Relatório completo")
        report = analyzer.generate_game_theory_report(historical_data[:100])  # Subset para teste rápido
        print(f"✅ Relatório gerado")
        
        summary = report['summary']
        print(f"   📊 Sorteios analisados: {summary['total_sorteios_analisados']}")
        print(f"   🎯 Estratégias geradas: {summary['numero_estrategias_geradas']}")
        print(f"   📈 Melhor Sharpe: {summary['melhor_portfolio_sharpe']:.3f}")
        
        # Teste 10: Verificação da recomendação
        comparison = report['strategy_comparison']
        recommendation = comparison['recommendation']
        print(f"\n🏆 Teste 10: Sistema de recomendação")
        print(f"✅ Recomendação gerada")
        print(f"   🎯 Estratégia: {recommendation['recommended_strategy']}")
        print(f"   📊 Números: {recommendation['recommended_numbers']}")
        print(f"   ⭐ Score: {recommendation['score']:.1f}/17")
        
        print(f"\n🎉 Todos os testes de teoria de jogos concluídos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_game_theory_analysis()