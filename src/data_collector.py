"""
Módulo para coleta de dados históricos da Mega Sena.
Obtém dados da fonte oficial da Caixa Econômica Federal.

MIT License - Copyright (c) 2025 delcain
Veja LICENSE para detalhes completos.
"""

import requests
import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import time
import concurrent.futures
import threading

class MegaSenaDataCollector:
    """Coletor de dados históricos da Mega Sena."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.base_url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena"
        self.bulk_url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/"
        self.data_file = os.path.join(data_dir, "megasena_historical.json")
        self.csv_file = os.path.join(data_dir, "megasena_historical.csv")
        
        # Criar diretório se não existir
        os.makedirs(data_dir, exist_ok=True)
    
    def get_latest_draw_number(self) -> int:
        """Obtém o número do último sorteio disponível."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('numero', 0)
        except Exception as e:
            print(f"Erro ao obter último sorteio: {e}")
            return 0
    
    def get_draw_data(self, draw_number: int) -> Optional[Dict]:
        """Obtém dados de um sorteio específico."""
        try:
            response = requests.get(f"{self.base_url}/{draw_number}", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extrair informações relevantes
            if data and 'numero' in data:
                return {
                    'concurso': data['numero'],
                    'data': data.get('dataApuracao', ''),
                    'numeros': data.get('dezenasSorteadasOrdemSorteio', []),
                    'numeros_ordenados': sorted(data.get('dezenasSorteadasOrdemSorteio', [])),
                    'acumulado': data.get('acumulado', False),
                    'valor_acumulado': data.get('valorAcumuladoProximoConcurso', 0),
                    'ganhadores_sena': data.get('listaRateioPremio', [{}])[0].get('numeroDeGanhadores', 0) if data.get('listaRateioPremio') else 0,
                    'valor_premio_sena': data.get('listaRateioPremio', [{}])[0].get('valorPremio', 0) if data.get('listaRateioPremio') else 0,
                    'local_sorteio': data.get('localSorteio', ''),
                    'observacao': data.get('observacao', '')
                }
            return None
        except Exception as e:
            print(f"Erro ao obter dados do concurso {draw_number}: {e}")
            return None
    
    def bulk_download_historical_data(self) -> Dict[int, Dict]:
        """Faz download em massa de dados históricos usando múltiplas estratégias."""
        print("Iniciando download em massa dos dados históricos...")
        
        # Tentar diferentes URLs da API da Caixa
        bulk_urls = [
            "https://servicebus2.caixa.gov.br/portaldeloterias/api/home/ultimos-resultados",
            "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/",
        ]
        
        historical_data = {}
        
        # Primeira tentativa: buscar arquivo consolidado (se existir)
        for url in bulk_urls:
            try:
                print(f"Tentando URL: {url}")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Verificar se retornou dados da megasena
                    if isinstance(data, list):
                        for item in data:
                            if item.get('modalidade') == 'megasena' or 'megasena' in str(item).lower():
                                # Processar dados encontrados
                                pass
                    elif isinstance(data, dict) and 'megasena' in data:
                        # Dados específicos da megasena
                        pass
                        
            except Exception as e:
                print(f"Erro na URL {url}: {e}")
                continue
        
        # Se não conseguiu dados em massa, usar método de lotes
        if not historical_data:
            print("Download em massa não disponível. Usando método de lotes otimizado...")
            historical_data = self.batch_download_data()
        
        return historical_data
    
    def batch_download_data(self, batch_size: int = 50) -> Dict[int, Dict]:
        """Download otimizado em lotes."""
        latest_draw = self.get_latest_draw_number()
        if latest_draw == 0:
            return {}
        
        historical_data = {}
        total_batches = (latest_draw // batch_size) + 1
        
        print(f"Baixando {latest_draw} sorteios em lotes de {batch_size}...")
        
        for batch_num in range(total_batches):
            start_draw = (batch_num * batch_size) + 1
            end_draw = min((batch_num + 1) * batch_size, latest_draw)
            
            print(f"Lote {batch_num + 1}/{total_batches}: Concursos {start_draw}-{end_draw}")
            
            # Download paralelo do lote
            batch_data = self.download_batch_parallel(start_draw, end_draw)
            historical_data.update(batch_data)
            
            # Salvar periodicamente para não perder progresso
            if batch_num % 10 == 0:  # A cada 10 lotes (500 sorteios)
                print(f"Salvando progresso... {len(historical_data)} sorteios baixados")
                self.save_data(historical_data)
            
            # Pausa menor entre lotes
            time.sleep(0.1)
        
        return historical_data
    
    def download_batch_parallel(self, start_draw: int, end_draw: int) -> Dict[int, Dict]:
        """Download paralelo de um lote de sorteios."""        
        batch_data = {}
        lock = threading.Lock()
        
        def download_single_draw(draw_num):
            draw_data = self.get_draw_data(draw_num)
            if draw_data:
                with lock:
                    batch_data[draw_num] = draw_data
                    if draw_num % 10 == 0:
                        print(f"  ✓ Concurso {draw_num}")
        
        # Usar ThreadPoolExecutor para downloads paralelos
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(download_single_draw, draw_num) 
                      for draw_num in range(start_draw, end_draw + 1)]
            
            # Aguardar conclusão
            concurrent.futures.wait(futures)
        
        return batch_data
    
    def needs_initial_download(self, threshold: int = 100) -> bool:
        """Verifica se precisa fazer download inicial completo."""
        existing_data = self.load_existing_data()
        latest_draw = self.get_latest_draw_number()
        
        if not existing_data:
            return True
        
        missing_count = latest_draw - len(existing_data)
        return missing_count > threshold
    
    def load_existing_data(self) -> Dict[int, Dict]:
        """Carrega dados existentes do arquivo."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {int(k): v for k, v in data.items()}
            except UnicodeDecodeError:
                # Tentar com encoding diferente
                try:
                    with open(self.data_file, 'r', encoding='latin-1') as f:
                        data = json.load(f)
                        return {int(k): v for k, v in data.items()}
                except Exception as e:
                    print(f"Erro ao carregar dados com encoding alternativo: {e}")
            except Exception as e:
                print(f"Erro ao carregar dados existentes: {e}")
        return {}
    
    def save_data(self, data: Dict[int, Dict]):
        """Salva dados no arquivo JSON."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Dados salvos em {self.data_file}")
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def save_to_csv(self, data: Dict[int, Dict]):
        """Salva dados em formato CSV."""
        try:
            records = []
            for concurso, info in data.items():
                record = {
                    'concurso': concurso,
                    'data': info['data'],
                    'num1': info['numeros_ordenados'][0] if len(info['numeros_ordenados']) > 0 else None,
                    'num2': info['numeros_ordenados'][1] if len(info['numeros_ordenados']) > 1 else None,
                    'num3': info['numeros_ordenados'][2] if len(info['numeros_ordenados']) > 2 else None,
                    'num4': info['numeros_ordenados'][3] if len(info['numeros_ordenados']) > 3 else None,
                    'num5': info['numeros_ordenados'][4] if len(info['numeros_ordenados']) > 4 else None,
                    'num6': info['numeros_ordenados'][5] if len(info['numeros_ordenados']) > 5 else None,
                    'acumulado': info['acumulado'],
                    'valor_acumulado': info['valor_acumulado'],
                    'ganhadores_sena': info['ganhadores_sena'],
                    'valor_premio_sena': info['valor_premio_sena']
                }
                records.append(record)
            
            df = pd.DataFrame(records)
            df = df.sort_values('concurso')
            df.to_csv(self.csv_file, index=False, encoding='utf-8')
            print(f"Dados salvos em CSV: {self.csv_file}")
        except Exception as e:
            print(f"Erro ao salvar CSV: {e}")
    
    def update_historical_data(self) -> bool:
        """Atualiza dados históricos com estratégia otimizada."""
        print("🔄 Iniciando atualização inteligente dos dados históricos...")
        
        # Obter último sorteio disponível
        latest_draw = self.get_latest_draw_number()
        if latest_draw == 0:
            print("❌ Não foi possível obter o número do último sorteio.")
            return False
        
        print(f"📊 Último sorteio disponível online: #{latest_draw}")
        
        # Verificar se precisa de download inicial em massa
        if self.needs_initial_download():
            print("🚀 Detectada necessidade de download inicial completo...")
            print("⚡ Usando método otimizado de download em massa...")
            
            # Download em massa otimizado
            all_data = self.bulk_download_historical_data()
            
            if all_data:
                print(f"✅ Download completo: {len(all_data)} sorteios obtidos!")
                self.save_data(all_data)
                self.save_to_csv(all_data)
                return True
            else:
                print("❌ Falha no download em massa. Tentando método tradicional...")
                return self.incremental_update()
        else:
            print("🔄 Fazendo atualização incremental...")
            return self.incremental_update()
    
    def incremental_update(self) -> bool:
        """Atualização incremental otimizada para poucos registros."""
        # Carregar dados existentes
        existing_data = self.load_existing_data()
        
        # Obter último sorteio disponível
        latest_draw = self.get_latest_draw_number()
        if latest_draw == 0:
            return False
        
        # Determinar quais sorteios precisam ser baixados
        if existing_data:
            last_downloaded = max(existing_data.keys())
            start_draw = last_downloaded + 1
            print(f"📈 Último sorteio local: #{last_downloaded}")
        else:
            start_draw = 1
            print("📥 Iniciando download completo (método incremental)...")
        
        missing_count = latest_draw - (last_downloaded if existing_data else 0)
        
        if missing_count == 0:
            print("✅ Dados já estão atualizados!")
            return False
        
        print(f"📦 Baixando {missing_count} novos sorteios...")
        
        # Para poucos registros, usar método sequencial otimizado
        if missing_count <= 10:
            # Download sequencial rápido
            new_data_count = 0
            for draw_num in range(start_draw, latest_draw + 1):
                print(f"⬇️  Concurso #{draw_num}")
                draw_data = self.get_draw_data(draw_num)
                
                if draw_data:
                    existing_data[draw_num] = draw_data
                    new_data_count += 1
                
                # Pausa mínima para poucos registros
                time.sleep(0.1)
        else:
            # Para muitos registros, usar lotes
            batch_data = self.download_batch_parallel(start_draw, latest_draw)
            existing_data.update(batch_data)
            new_data_count = len(batch_data)
        
        if new_data_count > 0:
            print(f"✅ {new_data_count} novos sorteios baixados e salvos!")
            self.save_data(existing_data)
            self.save_to_csv(existing_data)
            return True
        else:
            print("⚠️  Nenhum novo sorteio encontrado.")
            return False
    
    def get_dataframe(self) -> pd.DataFrame:
        """Retorna dados como DataFrame do pandas."""
        data = self.load_existing_data()
        if not data:
            print("Nenhum dado encontrado. Execute update_historical_data() primeiro.")
            return pd.DataFrame()
        
        records = []
        for concurso, info in data.items():
            record = {
                'concurso': concurso,
                'data': pd.to_datetime(info['data']),
                'numeros': info['numeros_ordenados'],
                'acumulado': info['acumulado'],
                'valor_acumulado': info['valor_acumulado'],
                'ganhadores_sena': info['ganhadores_sena'],
                'valor_premio_sena': info['valor_premio_sena']
            }
            # Adicionar cada número como coluna separada
            for i, num in enumerate(info['numeros_ordenados'], 1):
                record[f'num{i}'] = num
            
            records.append(record)
        
        df = pd.DataFrame(records)
        return df.sort_values('concurso')
    
    def get_all_numbers(self) -> List[List[int]]:
        """Retorna todos os números sorteados como lista de listas."""
        data = self.load_existing_data()
        result = []
        for info in data.values():
            numeros = info.get('numeros_ordenados', [])
            # Converter strings para inteiros se necessário
            if numeros and isinstance(numeros[0], str):
                numeros = [int(num) for num in numeros]
            result.append(numeros)
        return result
    
    def get_statistics_summary(self) -> Dict:
        """Retorna resumo estatístico dos dados."""
        data = self.load_existing_data()
        if not data:
            return {}
        
        total_draws = len(data)
        all_numbers = []
        for info in data.values():
            all_numbers.extend(info['numeros_ordenados'])
        
        return {
            'total_sorteios': total_draws,
            'primeiro_sorteio': min(data.keys()),
            'ultimo_sorteio': max(data.keys()),
            'total_numeros_sorteados': len(all_numbers),
            'numeros_unicos': len(set(all_numbers)),
            'data_primeiro': next(iter(data.values()))['data'],
            'data_ultimo': data[max(data.keys())]['data']
        }


def main():
    """Função principal para teste do módulo."""
    collector = MegaSenaDataCollector()
    
    print("=== COLETOR DE DADOS DA MEGA SENA ===")
    print("1. Atualizando dados históricos...")
    collector.update_historical_data()
    
    print("\n2. Resumo dos dados:")
    summary = collector.get_statistics_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    print("\n3. Primeiros 5 registros:")
    df = collector.get_dataframe()
    if not df.empty:
        print(df.head())


if __name__ == "__main__":
    main()