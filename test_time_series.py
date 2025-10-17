#!/usr/bin/env python3
"""
Teste da nova funcionalidade de análise de séries temporais.

MIT License - Copyright (c) 2025 delcain
Veja LICENSE para detalhes completos.
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.time_series_analyzer import MegaSenaTimeSeriesAnalyzer
    from src.data_collector import MegaSenaDataCollector
except ImportError as e:
    print(f"Erro ao importar: {e}")
    sys.exit(1)

def test_time_series_analysis():
    """Testa a análise de séries temporais."""
    print("🧪 TESTE - ANÁLISE DE SÉRIES TEMPORAIS")
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
        analyzer = MegaSenaTimeSeriesAnalyzer()
        
        # Teste 1: Preparação dos dados
        print(f"\n🔧 Teste 1: Preparação dos dados temporais")
        df = analyzer.prepare_time_series_data(historical_data[:100])  # Usar apenas 100 para teste
        print(f"✅ DataFrame criado com {len(df)} registros")
        print(f"📊 Colunas: {list(df.columns)}")
        
        # Teste 2: Decomposição temporal
        print(f"\n📈 Teste 2: Decomposição temporal")
        decomp = analyzer.decompose_time_series('sum_numbers')
        print(f"✅ Decomposição concluída")
        print(f"   📊 Qualidade: {decomp['decomposition_quality']:.3f}")
        print(f"   📈 Inclinação da tendência: {decomp['trend_slope']:.4f}")
        print(f"   🔄 Força sazonal: {decomp['seasonal_strength']:.3f}")
        
        # Teste 3: Análise sazonal
        print(f"\n🗓️ Teste 3: Análise sazonal")
        seasonal = analyzer.seasonal_analysis()
        print(f"✅ Análise sazonal concluída")
        if 'summary' in seasonal:
            summary = seasonal['summary']
            print(f"   📈 Mês com maior soma: {summary['highest_sum_month']}")
            print(f"   📉 Mês com menor soma: {summary['lowest_sum_month']}")
        
        # Teste 4: Análise de tendências
        print(f"\n📊 Teste 4: Análise de tendências")
        trends = analyzer.trend_analysis()
        print(f"✅ Análise de tendências concluída")
        for metric, data in trends.items():
            if 'trend_direction' in data:
                direction = data['trend_direction']
                strength = data.get('trend_strength', 0)
                print(f"   📊 {metric}: {direction} (força: {strength:.3f})")
        
        # Teste 5: Detecção de anomalias
        print(f"\n⚠️ Teste 5: Detecção de anomalias")
        anomalies = analyzer.anomaly_detection()
        print(f"✅ Detecção de anomalias concluída")
        total_outliers = sum(data['outlier_count'] for data in anomalies.values())
        print(f"   📊 Total de outliers: {total_outliers}")
        
        # Teste 6: Detecção de ciclos
        print(f"\n🔄 Teste 6: Detecção de ciclos")
        cycles = analyzer.detect_cycles_and_patterns()
        print(f"✅ Detecção de ciclos concluída")
        cycle_found = False
        for metric, data in cycles.items():
            if data['dominant_periods']:
                periods = data['dominant_periods'][:2]
                print(f"   📊 {metric}: períodos {[f'{p:.1f}' for p in periods]} semanas")
                cycle_found = True
        
        if not cycle_found:
            print("   📊 Nenhum ciclo dominante detectado")
        
        # Teste 7: Gráficos (se possível)
        print(f"\n📊 Teste 7: Geração de gráficos")
        try:
            plots = analyzer.create_time_series_plots()
            print(f"✅ {len(plots)} gráficos gerados:")
            for plot in plots:
                filename = plot.split('\\')[-1] if '\\' in plot else plot.split('/')[-1]
                print(f"   📈 {filename}")
        except Exception as e:
            print(f"⚠️ Gráficos não puderam ser gerados: {e}")
        
        # Teste 8: Relatório completo
        print(f"\n📋 Teste 8: Relatório completo")
        report = analyzer.generate_time_series_report(historical_data[:50])  # Subset para teste rápido
        print(f"✅ Relatório gerado")
        
        summary = report['summary']
        print(f"   📊 Sorteios analisados: {summary['total_sorteios_analisados']}")
        print(f"   📅 Período: {summary['periodo_analise']['inicio']} a {summary['periodo_analise']['fim']}")
        print(f"   📈 Tendência: {summary['tendencia_geral']}")
        print(f"   🔄 Sazonalidade: {'Sim' if summary['sazonalidade_detectada'] else 'Não'}")
        
        print(f"\n🎉 Todos os testes concluídos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_time_series_analysis()