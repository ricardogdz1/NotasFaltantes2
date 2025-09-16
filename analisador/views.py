from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import tempfile

from .servicos import AnalisadorSequencia


def pagina_inicial(request):
    """
    View da página inicial com formulário de upload.
    """
    return render(request, 'analisador/index.html')


def processar_arquivo(request):
    """
    View para processar o arquivo enviado e exibir resultados.
    """
    if request.method == 'POST':
        # Verificar se um arquivo foi enviado
        if 'arquivo' not in request.FILES:
            messages.error(request, 'Nenhum arquivo foi enviado.')
            return render(request, 'analisador/index.html')
        
        arquivo = request.FILES['arquivo']
        
        # Validar tipo de arquivo
        if not arquivo.name.endswith('.txt'):
            messages.error(request, 'Por favor, envie apenas arquivos com extensão .txt')
            return render(request, 'analisador/index.html')
        
        # Validar tamanho do arquivo (máximo 5MB)
        if arquivo.size > 5 * 1024 * 1024:  # 5MB em bytes
            messages.error(request, 'Arquivo muito grande. Tamanho máximo permitido: 5MB')
            return render(request, 'analisador/index.html')
        
        try:
            # Ler conteúdo do arquivo
            conteudo = arquivo.read().decode('utf-8')
            
            # Processar arquivo usando o serviço analisador
            analisador = AnalisadorSequencia()
            resultado = analisador.processar_arquivo(conteudo)
            
            if not resultado['sucesso']:
                messages.error(request, resultado['erro'])
                return render(request, 'analisador/index.html')
            
            # Preparar contexto para o template
            contexto = {
                'resultado': resultado,
                'nome_arquivo': arquivo.name,
                'lista_faltantes_copia': analisador.gerar_lista_copia_faltantes(),
                'tem_faltantes': len(resultado['numeros_faltantes']) > 0,
                'tem_duplicados': len(resultado['numeros_duplicados']) > 0,
            }
            
            return render(request, 'analisador/resultado.html', contexto)
            
        except UnicodeDecodeError:
            messages.error(request, 'Erro ao ler o arquivo. Certifique-se de que é um arquivo de texto válido (UTF-8).')
            return render(request, 'analisador/index.html')
        
        except Exception as e:
            messages.error(request, f'Erro inesperado ao processar arquivo: {str(e)}')
            return render(request, 'analisador/index.html')
    
    # Se não for POST, redireciona para página inicial
    return render(request, 'analisador/index.html')


@csrf_exempt
def copiar_numeros_faltantes(request):
    """
    View AJAX para retornar lista de números faltantes formatada para cópia.
    """
    if request.method == 'POST':
        try:
            # Recuperar dados da sessão ou do POST
            arquivo_conteudo = request.POST.get('conteudo_arquivo', '')
            
            if not arquivo_conteudo:
                return JsonResponse({
                    'sucesso': False,
                    'erro': 'Nenhum conteúdo para processar'
                })
            
            # Processar novamente para obter números faltantes
            analisador = AnalisadorSequencia()
            resultado = analisador.processar_arquivo(arquivo_conteudo)
            
            if not resultado['sucesso']:
                return JsonResponse({
                    'sucesso': False,
                    'erro': resultado['erro']
                })
            
            lista_faltantes = analisador.gerar_lista_copia_faltantes()
            
            return JsonResponse({
                'sucesso': True,
                'lista_faltantes': lista_faltantes,
                'total_faltantes': len(resultado['numeros_faltantes'])
            })
            
        except Exception as e:
            return JsonResponse({
                'sucesso': False,
                'erro': f'Erro ao gerar lista para cópia: {str(e)}'
            })
    
    return JsonResponse({
        'sucesso': False,
        'erro': 'Método não permitido'
    })