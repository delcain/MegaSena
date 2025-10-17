"""
Módulo de análise de séries temporais para Mega Sena.
Implementa decomposição temporal, detecção de ciclos e análise sazonal.

MIT License - Copyright (c) 2025 delcain
Veja LICENSE para detalhes completos.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

try:
    from scipy import stats
    from scipy.signal import find_peaks
    from scipy.fft import fft, fftfreq
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class MegaSenaTimeSeriesAnalyzer:
    """Análise de séries temporais para dados da Mega Sena."""
    
    def __init__(self):
        self.historical_data = []
        self.time_series_data = None
        self.frequency_data = None
        
    def prepare_time_series_data(self, historical_data: List) -> pd.DataFrame:
        """
        Prepara dados históricos para análise de séries temporais.
        
        Args:
            historical_data: Lista com dados históricos dos sorteios
            
        Returns:
            DataFrame com dados organizados por tempo
        """
        if not historical_data:
            raise ValueError("Dados históricos não fornecidos")
        
        # Criar DataFrame temporal
        time_data = []
        
        for i, sorteio in enumerate(historical_data):
            # Se sorteio é lista de números
            if isinstance(sorteio, list):
                numbers = sorteio
                # Simular datas (semanais, começando em 1996)
                base_date = datetime(1996, 3, 11)  # Primeiro sorteio da Mega Sena
                date = base_date + timedelta(weeks=i)
            else:
                # Se tem estrutura de dicionário
                numbers = sorteio.get('numeros', sorteio)
                date = datetime(1996, 3, 11) + timedelta(weeks=i)
            
            # Métricas por sorteio
            time_data.append({
                'date': date,
                'sorteio_id': i + 1,
                'numbers': numbers,
                'sum_numbers': sum(numbers),
                'max_number': max(numbers),
                'min_number': min(numbers),
                'range_numbers': max(numbers) - min(numbers),
                'even_count': sum(1 for n in numbers if n % 2 == 0),
                'odd_count': sum(1 for n in numbers if n % 2 == 1),
                'decade_1': sum(1 for n in numbers if 1 <= n <= 10),
                'decade_2': sum(1 for n in numbers if 11 <= n <= 20),
                'decade_3': sum(1 for n in numbers if 21 <= n <= 30),
                'decade_4': sum(1 for n in numbers if 31 <= n <= 40),
                'decade_5': sum(1 for n in numbers if 41 <= n <= 50),
                'decade_6': sum(1 for n in numbers if 51 <= n <= 60),
                'year': date.year,
                'month': date.month,
                'quarter': (date.month - 1) // 3 + 1,
                'day_of_year': date.timetuple().tm_yday
            })
        
        df = pd.DataFrame(time_data)
        df.set_index('date', inplace=True)
        
        self.time_series_data = df
        return df
    
    def decompose_time_series(self, column: str = 'sum_numbers') -> Dict:
        """
        Decomposição de série temporal em tendência, sazonalidade e ruído.
        
        Args:
            column: Coluna para análise (default: soma dos números)
            
        Returns:
            Dict com componentes da decomposição
        """
        if self.time_series_data is None:
            raise ValueError("Dados de série temporal não preparados")
        
        data = self.time_series_data[column].values
        n = len(data)
        
        # Decomposição simples usando média móvel
        # Tendência (média móvel de 52 semanas = 1 ano)
        window = min(52, n // 4)
        if window < 3:
            window = 3
            
        trend = pd.Series(data).rolling(window=window, center=True).mean().values
        
        # Remover tendência
        detrended = data - np.nanmean(trend) if np.isnan(trend).all() else data - np.nan_to_num(trend)
        
        # Sazonalidade (padrão anual)
        seasonal_period = min(52, n // 2)  # 52 semanas por ano
        if seasonal_period < 4:
            seasonal_period = 4
            
        seasonal = np.zeros_like(data)
        for i in range(seasonal_period):
            indices = np.arange(i, n, seasonal_period)
            if len(indices) > 0:
                seasonal[indices] = np.mean(detrended[indices])
        
        # Resíduo (ruído)
        residual = data - np.nan_to_num(trend) - seasonal
        
        # Análise estatística
        trend_slope = 0
        if not np.isnan(trend).all():
            valid_trend = trend[~np.isnan(trend)]
            if len(valid_trend) > 1:
                x = np.arange(len(valid_trend))
                trend_slope = np.polyfit(x, valid_trend, 1)[0]
        
        seasonal_strength = np.var(seasonal) / np.var(data) if np.var(data) > 0 else 0
        noise_level = np.std(residual)
        
        return {
            'original': data,
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual,
            'trend_slope': trend_slope,
            'seasonal_strength': seasonal_strength,
            'noise_level': noise_level,
            'decomposition_quality': 1 - (np.var(residual) / np.var(data)) if np.var(data) > 0 else 0
        }
    
    def detect_cycles_and_patterns(self) -> Dict:
        """
        Detecta ciclos e padrões temporais nos dados.
        
        Returns:
            Dict com informações sobre ciclos detectados
        """
        if self.time_series_data is None:
            raise ValueError("Dados de série temporal não preparados")
        
        results = {}
        
        # Análise por diferentes métricas
        metrics = ['sum_numbers', 'max_number', 'even_count', 'range_numbers']
        
        for metric in metrics:
            if metric not in self.time_series_data.columns:
                continue
                
            data = self.time_series_data[metric].values
            
            # Análise de Fourier (se scipy disponível)
            if SCIPY_AVAILABLE and len(data) > 10:
                # FFT para detectar periodicidades
                fft_vals = fft(data - np.mean(data))
                freqs = fftfreq(len(data))
                
                # Encontrar frequências dominantes
                power = np.abs(fft_vals) ** 2
                dominant_freqs = freqs[np.argsort(power)[-5:]]  # Top 5 frequências
                
                # Converter para períodos (em semanas)
                periods = []
                for freq in dominant_freqs:
                    if freq != 0:
                        period = 1 / abs(freq)
                        if 2 <= period <= len(data) // 2:  # Períodos válidos
                            periods.append(period)
                
                results[metric] = {
                    'dominant_periods': sorted(periods, reverse=True)[:3],
                    'spectral_analysis': {
                        'frequencies': dominant_freqs.tolist(),
                        'power_spectrum': power[np.argsort(power)[-5:]].tolist()
                    }
                }
            else:
                results[metric] = {
                    'dominant_periods': [],
                    'spectral_analysis': None
                }
        
        return results
    
    def seasonal_analysis(self) -> Dict:
        """
        Análise sazonal detalhada (mensal, trimestral, anual).
        
        Returns:
            Dict com análises sazonais
        """
        if self.time_series_data is None:
            raise ValueError("Dados de série temporal não preparados")
        
        df = self.time_series_data
        
        # Análise mensal
        monthly_stats = df.groupby('month').agg({
            'sum_numbers': ['mean', 'std', 'min', 'max'],
            'even_count': ['mean', 'std'],
            'max_number': ['mean', 'std']
        }).round(2)
        
        # Análise trimestral
        quarterly_stats = df.groupby('quarter').agg({
            'sum_numbers': ['mean', 'std', 'min', 'max'],
            'even_count': ['mean', 'std'],
            'max_number': ['mean', 'std']
        }).round(2)
        
        # Análise anual (se há dados suficientes)
        yearly_stats = df.groupby('year').agg({
            'sum_numbers': ['mean', 'std', 'min', 'max'],
            'even_count': ['mean', 'std'],
            'max_number': ['mean', 'std']
        }).round(2)
        
        # Teste de sazonalidade (se scipy disponível)
        seasonality_tests = {}
        if SCIPY_AVAILABLE:
            for metric in ['sum_numbers', 'even_count', 'max_number']:
                # Teste ANOVA para diferenças entre meses
                monthly_groups = [group[metric].values for name, group in df.groupby('month')]
                if len(monthly_groups) > 1 and all(len(group) > 0 for group in monthly_groups):
                    f_stat, p_value = stats.f_oneway(*monthly_groups)
                    seasonality_tests[metric] = {
                        'f_statistic': f_stat,
                        'p_value': p_value,
                        'is_seasonal': p_value < 0.05
                    }
        
        return {
            'monthly_statistics': monthly_stats.to_dict(),
            'quarterly_statistics': quarterly_stats.to_dict(),
            'yearly_statistics': yearly_stats.to_dict(),
            'seasonality_tests': seasonality_tests,
            'summary': {
                'most_variable_month': monthly_stats[('sum_numbers', 'std')].idxmax(),
                'least_variable_month': monthly_stats[('sum_numbers', 'std')].idxmin(),
                'highest_sum_month': monthly_stats[('sum_numbers', 'mean')].idxmax(),
                'lowest_sum_month': monthly_stats[('sum_numbers', 'mean')].idxmin()
            }
        }
    
    def trend_analysis(self) -> Dict:
        """
        Análise de tendências ao longo do tempo.
        
        Returns:
            Dict com análise de tendências
        """
        if self.time_series_data is None:
            raise ValueError("Dados de série temporal não preparados")
        
        df = self.time_series_data.reset_index()
        results = {}
        
        # Análise de tendência para diferentes métricas
        metrics = ['sum_numbers', 'max_number', 'even_count', 'range_numbers']
        
        for metric in metrics:
            if metric not in df.columns:
                continue
                
            # Regressão linear simples
            x = np.arange(len(df))
            y = df[metric].values
            
            if SCIPY_AVAILABLE:
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                
                results[metric] = {
                    'slope': slope,
                    'intercept': intercept,
                    'correlation': r_value,
                    'p_value': p_value,
                    'standard_error': std_err,
                    'trend_direction': 'crescente' if slope > 0 else 'decrescente' if slope < 0 else 'estável',
                    'trend_strength': abs(r_value),
                    'significant_trend': p_value < 0.05
                }
            else:
                # Cálculo manual se scipy não disponível
                slope = np.polyfit(x, y, 1)[0]
                correlation = np.corrcoef(x, y)[0, 1]
                
                results[metric] = {
                    'slope': slope,
                    'correlation': correlation,
                    'trend_direction': 'crescente' if slope > 0 else 'decrescente' if slope < 0 else 'estável',
                    'trend_strength': abs(correlation)
                }
        
        return results
    
    def anomaly_detection(self) -> Dict:
        """
        Detecta anomalias e outliers temporais.
        
        Returns:
            Dict com anomalias detectadas
        """
        if self.time_series_data is None:
            raise ValueError("Dados de série temporal não preparados")
        
        df = self.time_series_data.reset_index()
        anomalies = {}
        
        metrics = ['sum_numbers', 'max_number', 'range_numbers']
        
        for metric in metrics:
            if metric not in df.columns:
                continue
                
            data = df[metric].values
            
            # Método IQR para detecção de outliers
            Q1 = np.percentile(data, 25)
            Q3 = np.percentile(data, 75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_indices = np.where((data < lower_bound) | (data > upper_bound))[0]
            
            # Z-score para anomalias extremas
            z_scores = np.abs(stats.zscore(data)) if SCIPY_AVAILABLE else np.abs((data - np.mean(data)) / np.std(data))
            extreme_indices = np.where(z_scores > 3)[0]
            
            anomalies[metric] = {
                'outlier_indices': outlier_indices.tolist(),
                'extreme_indices': extreme_indices.tolist(),
                'outlier_count': len(outlier_indices),
                'extreme_count': len(extreme_indices),
                'outlier_percentage': len(outlier_indices) / len(data) * 100,
                'bounds': {
                    'lower': lower_bound,
                    'upper': upper_bound,
                    'iqr': IQR
                }
            }
        
        return anomalies
    
    def create_time_series_plots(self, save_path: str = "data/plots/time_series") -> List[str]:
        """
        Cria gráficos de análise temporal.
        
        Args:
            save_path: Caminho para salvar os gráficos
            
        Returns:
            Lista com caminhos dos arquivos salvos
        """
        import os
        os.makedirs(save_path, exist_ok=True)
        
        if self.time_series_data is None:
            raise ValueError("Dados de série temporal não preparados")
        
        saved_files = []
        
        # 1. Gráfico de decomposição temporal
        plt.style.use('default')
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        
        decomp = self.decompose_time_series('sum_numbers')
        
        # Série original
        axes[0].plot(self.time_series_data.index, decomp['original'], 'b-', alpha=0.8)
        axes[0].set_title('Série Temporal Original - Soma dos Números', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Soma')
        axes[0].grid(True, alpha=0.3)
        
        # Tendência
        axes[1].plot(self.time_series_data.index, decomp['trend'], 'r-', linewidth=2)
        axes[1].set_title('Tendência', fontsize=12)
        axes[1].set_ylabel('Tendência')
        axes[1].grid(True, alpha=0.3)
        
        # Sazonalidade
        axes[2].plot(self.time_series_data.index, decomp['seasonal'], 'g-', linewidth=1.5)
        axes[2].set_title('Componente Sazonal', fontsize=12)
        axes[2].set_ylabel('Sazonalidade')
        axes[2].grid(True, alpha=0.3)
        
        # Resíduo
        axes[3].plot(self.time_series_data.index, decomp['residual'], 'orange', alpha=0.7)
        axes[3].set_title('Resíduo (Ruído)', fontsize=12)
        axes[3].set_ylabel('Resíduo')
        axes[3].set_xlabel('Data')
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        decomp_file = os.path.join(save_path, 'decomposicao_temporal.png')
        plt.savefig(decomp_file, dpi=300, bbox_inches='tight')
        plt.close()
        saved_files.append(decomp_file)
        
        # 2. Análise sazonal
        seasonal_data = self.seasonal_analysis()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Análise mensal
        monthly_means = [seasonal_data['monthly_statistics'][('sum_numbers', 'mean')][i] 
                        for i in range(1, 13)]
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        axes[0,0].bar(months, monthly_means, color='skyblue', alpha=0.8)
        axes[0,0].set_title('Soma Média por Mês', fontweight='bold')
        axes[0,0].set_ylabel('Soma Média')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Análise trimestral
        quarterly_means = [seasonal_data['quarterly_statistics'][('sum_numbers', 'mean')][i] 
                          for i in range(1, 5)]
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        
        axes[0,1].bar(quarters, quarterly_means, color='lightcoral', alpha=0.8)
        axes[0,1].set_title('Soma Média por Trimestre', fontweight='bold')
        axes[0,1].set_ylabel('Soma Média')
        
        # Evolução anual
        df_reset = self.time_series_data.reset_index()
        yearly_evolution = df_reset.groupby('year')['sum_numbers'].mean()
        
        axes[1,0].plot(yearly_evolution.index, yearly_evolution.values, 'ro-', linewidth=2, markersize=6)
        axes[1,0].set_title('Evolução Anual da Soma Média', fontweight='bold')
        axes[1,0].set_xlabel('Ano')
        axes[1,0].set_ylabel('Soma Média')
        axes[1,0].grid(True, alpha=0.3)
        
        # Distribuição de números pares/ímpares
        axes[1,1].hist([self.time_series_data['even_count'], self.time_series_data['odd_count']], 
                      bins=7, alpha=0.7, label=['Pares', 'Ímpares'], color=['blue', 'red'])
        axes[1,1].set_title('Distribuição Pares/Ímpares', fontweight='bold')
        axes[1,1].set_xlabel('Quantidade')
        axes[1,1].set_ylabel('Frequência')
        axes[1,1].legend()
        
        plt.tight_layout()
        seasonal_file = os.path.join(save_path, 'analise_sazonal.png')
        plt.savefig(seasonal_file, dpi=300, bbox_inches='tight')
        plt.close()
        saved_files.append(seasonal_file)
        
        return saved_files
    
    def generate_time_series_report(self, historical_data: List) -> Dict:
        """
        Gera relatório completo de análise temporal.
        
        Args:
            historical_data: Dados históricos dos sorteios
            
        Returns:
            Dict com relatório completo
        """
        # Preparar dados
        self.prepare_time_series_data(historical_data)
        
        # Executar todas as análises
        decomposition = self.decompose_time_series()
        cycles = self.detect_cycles_and_patterns()
        seasonal = self.seasonal_analysis()
        trends = self.trend_analysis()
        anomalies = self.anomaly_detection()
        
        # Criar gráficos
        try:
            plot_files = self.create_time_series_plots()
        except Exception as e:
            plot_files = []
            print(f"Erro ao criar gráficos: {e}")
        
        # Resumo executivo
        summary = {
            'total_sorteios_analisados': len(historical_data),
            'periodo_analise': {
                'inicio': self.time_series_data.index.min().strftime('%d/%m/%Y'),
                'fim': self.time_series_data.index.max().strftime('%d/%m/%Y')
            },
            'qualidade_decomposicao': f"{decomposition['decomposition_quality']:.3f}",
            'tendencia_geral': trends.get('sum_numbers', {}).get('trend_direction', 'N/A'),
            'sazonalidade_detectada': any(seasonal['seasonality_tests'].get(metric, {}).get('is_seasonal', False) 
                                        for metric in seasonal['seasonality_tests']),
            'outliers_detectados': sum(anomalies[metric]['outlier_count'] for metric in anomalies),
            'graficos_gerados': len(plot_files)
        }
        
        return {
            'summary': summary,
            'decomposition': decomposition,
            'cycles_and_patterns': cycles,
            'seasonal_analysis': seasonal,
            'trend_analysis': trends,
            'anomaly_detection': anomalies,
            'generated_plots': plot_files,
            'data_quality': {
                'completeness': 1.0,  # Assumindo dados completos
                'consistency': 'Alta',
                'temporal_coverage': f"{len(historical_data)} sorteios"
            }
        }