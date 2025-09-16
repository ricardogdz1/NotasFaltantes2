from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import tempfile

from .servicos import AnalisadorSequencia


@csrf_protect
def pagina_inicial(request):
    """
    View da página inicial com formulário de upload.
    """
    # Garante que o token CSRF está disponível
    csrf_token = get_token(request)
    return render(request, 'analisador/index.html', {'csrf_token': csrf_token})


@csrf_protect
@require_http_methods(["POST"])
def processar_arquivo(request):
    """
    View para processar o arquivo enviado e exibir resultados.
    """
    # Verificar se um arquivo foi enviado
    if 'arquivo' not in request.FILES:
        messages.error(request, 'Nenhum arquivo foi enviado.')
        return redirect('analisador:index')
    
    arquivo = request.FILES['arquivo']
    
    # Validar se arquivo não está vazio
    if not arquivo:
        messages.error(request, 'Arquivo vazio ou inválido.')
        return redirect('analisador:index')
    
    # Validar tipo de arquivo
    if not arquivo.name.endswith('.txt'):
        messages.error(request, 'Por favor, envie apenas arquivos com extensão .txt')
        return redirect('analisador:index')
    
    # Validar tamanho do arquivo (máximo 5MB)
    if arquivo.size > 5 * 1024 * 1024:  # 5MB em bytes
        messages.error(request, 'Arquivo muito grande. Tamanho máximo permitido: 5MB')
        return redirect('analisador:index')
    
    try:
        # Ler conteúdo do arquivo
        conteudo = arquivo.read().decode('utf-8')
        
        # Verificar se o arquivo não está vazio
        if not conteudo.strip():
            messages.error(request, 'O arquivo está vazio. Por favor, envie um arquivo com números.')
            return redirect('analisador:index')
        
        # Processar arquivo usando o serviço analisador
        analisador = AnalisadorSequencia()
        resultado = analisador.processar_arquivo(conteudo)
        
        if not resultado['sucesso']:
            messages.error(request, resultado['erro'])
            return redirect('analisador:index')
        
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
        return redirect('analisador:index')
    
    except Exception as e:
        messages.error(request, f'Erro inesperado ao processar arquivo: {str(e)}')
        return redirect('analisador:index')
