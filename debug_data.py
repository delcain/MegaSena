#!/usr/bin/env python3
"""
Debug da estrutura dos dados históricos.
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.data_collector import MegaSenaDataCollector
except ImportError as e:
    print(f"Erro ao importar: {e}")
    sys.exit(1)

def debug_data_structure():
    """Debug da estrutura dos dados."""
    print("🔍 DEBUG - ESTRUTURA DOS DADOS")
    print("=" * 40)
    
    collector = MegaSenaDataCollector()
    historical_data = collector.get_all_numbers()
    
    if historical_data:
        print(f"📊 Total de registros: {len(historical_data)}")
        print(f"📋 Tipo dos dados: {type(historical_data)}")
        print(f"📋 Tipo do primeiro elemento: {type(historical_data[0])}")
        print(f"📋 Estrutura do primeiro elemento:")
        
        first_element = historical_data[0]
        if isinstance(first_element, dict):
            for key, value in first_element.items():
                print(f"   {key}: {value} (tipo: {type(value)})")
        elif isinstance(first_element, list):
            print(f"   Lista com {len(first_element)} elementos: {first_element}")
        else:
            print(f"   Conteúdo: {first_element}")
        
        print(f"\n📋 Amostra dos primeiros 3 elementos:")
        for i, element in enumerate(historical_data[:3]):
            print(f"   Elemento {i}: {element}")
    else:
        print("❌ Nenhum dado encontrado")

if __name__ == "__main__":
    debug_data_structure()