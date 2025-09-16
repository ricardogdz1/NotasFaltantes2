#!/usr/bin/env python3
"""
Teste rápido do analisador de sequências.
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analisador_sequencias.settings')
django.setup()

from analisador.servicos import AnalisadorSequencia

def testar_analisador():
    print("=== Teste do Analisador de Sequências ===\n")
    
    # Teste 1: Sequência com números faltantes e duplicados
    print("Teste 1: Sequência com faltantes e duplicados")
    conteudo1 = "1, 2, 3, 5, 7, 8, 9, 12, 15, 15, 18, 20, 20, 20, 22"
    
    analisador = AnalisadorSequencia()
    resultado = analisador.processar_arquivo(conteudo1)
    
    if resultado['sucesso']:
        print(f"✓ Números encontrados: {resultado['numeros_encontrados']}")
        print(f"✓ Números faltantes: {resultado['numeros_faltantes']}")
        print(f"✓ Números duplicados: {resultado['numeros_duplicados']}")
        print(f"✓ Intervalo: {resultado['intervalo']['menor']} até {resultado['intervalo']['maior']}")
        print(f"✓ Estatísticas: {resultado['estatisticas']}")
        print(f"✓ Lista para cópia: {analisador.gerar_lista_copia_faltantes()}")
    else:
        print(f"✗ Erro: {resultado['erro']}")
    
    print("\n" + "="*50 + "\n")
    
    # Teste 2: Sequência com quebras de linha
    print("Teste 2: Sequência com quebras de linha")
    conteudo2 = """10
11
12
15
16
18
18
20"""
    
    resultado2 = analisador.processar_arquivo(conteudo2)
    
    if resultado2['sucesso']:
        print(f"✓ Números encontrados: {resultado2['numeros_encontrados']}")
        print(f"✓ Números faltantes: {resultado2['numeros_faltantes']}")
        print(f"✓ Números duplicados: {resultado2['numeros_duplicados']}")
        print(f"✓ Lista para cópia: {analisador.gerar_lista_copia_faltantes()}")
    else:
        print(f"✗ Erro: {resultado2['erro']}")
    
    print("\n" + "="*50 + "\n")
    
    # Teste 3: Sequência perfeita (sem faltantes nem duplicados)
    print("Teste 3: Sequência perfeita")
    conteudo3 = "100, 101, 102, 103, 104, 105"
    
    resultado3 = analisador.processar_arquivo(conteudo3)
    
    if resultado3['sucesso']:
        print(f"✓ Números encontrados: {resultado3['numeros_encontrados']}")
        print(f"✓ Números faltantes: {resultado3['numeros_faltantes']}")
        print(f"✓ Números duplicados: {resultado3['numeros_duplicados']}")
        print(f"✓ Lista para cópia: {analisador.gerar_lista_copia_faltantes()}")
    else:
        print(f"✗ Erro: {resultado3['erro']}")

if __name__ == "__main__":
    testar_analisador()