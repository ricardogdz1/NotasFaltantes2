import re
from typing import List, Tuple, Set
from collections import Counter


class AnalisadorSequencia:
    """
    Classe responsável por analisar sequências numéricas de arquivos TXT
    e identificar números faltantes e duplicados.
    """
    
    def __init__(self):
        self.numeros_encontrados = []
        self.numeros_faltantes = []
        self.numeros_duplicados = []
        self.menor_numero = None
        self.maior_numero = None
    
    def processar_arquivo(self, conteudo_arquivo: str) -> dict:
        """
        Processa o conteúdo do arquivo e identifica números faltantes e duplicados.
        
        Args:
            conteudo_arquivo (str): Conteúdo do arquivo TXT
            
        Returns:
            dict: Resultado da análise com números encontrados, faltantes e duplicados
        """
        try:
            # Limpar dados anteriores
            self._limpar_dados()
            
            # Extrair números do conteúdo
            self.numeros_encontrados = self._extrair_numeros(conteudo_arquivo)
            
            if not self.numeros_encontrados:
                return {
                    'sucesso': False,
                    'erro': 'Nenhum número foi encontrado no arquivo.',
                    'numeros_encontrados': [],
                    'numeros_faltantes': [],
                    'numeros_duplicados': [],
                    'estatisticas': {}
                }
            
            # Identificar duplicados
            self.numeros_duplicados = self._identificar_duplicados()
            
            # Determinar intervalo da sequência
            self.menor_numero = min(self.numeros_encontrados)
            self.maior_numero = max(self.numeros_encontrados)
            
            # Identificar números faltantes
            self.numeros_faltantes = self._identificar_faltantes()
            
            # Preparar estatísticas
            estatisticas = self._gerar_estatisticas()
            
            return {
                'sucesso': True,
                'numeros_encontrados': sorted(list(set(self.numeros_encontrados))),
                'numeros_faltantes': self.numeros_faltantes,
                'numeros_duplicados': self.numeros_duplicados,
                'estatisticas': estatisticas,
                'intervalo': {
                    'menor': self.menor_numero,
                    'maior': self.maior_numero
                }
            }
            
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro ao processar arquivo: {str(e)}',
                'numeros_encontrados': [],
                'numeros_faltantes': [],
                'numeros_duplicados': [],
                'estatisticas': {}
            }
    
    def _limpar_dados(self):
        """Limpa os dados de análises anteriores."""
        self.numeros_encontrados = []
        self.numeros_faltantes = []
        self.numeros_duplicados = []
        self.menor_numero = None
        self.maior_numero = None
    
    def _extrair_numeros(self, conteudo: str) -> List[int]:
        """
        Extrai números do conteúdo do arquivo, suportando diferentes formatos:
        - Separados por vírgula: 1, 2, 3, 4
        - Separados por quebra de linha: 1\n2\n3\n4
        - Separados por vírgula e quebra de linha: 1,\n2,\n3,\n4
        
        Args:
            conteudo (str): Conteúdo do arquivo
            
        Returns:
            List[int]: Lista de números encontrados
        """
        # Remove espaços extras e quebras de linha desnecessárias
        conteudo_limpo = conteudo.strip()
        
        # Padrão regex para encontrar números (incluindo negativos)
        padrao_numeros = r'-?\d+'
        
        # Encontra todos os números no texto
        numeros_texto = re.findall(padrao_numeros, conteudo_limpo)
        
        # Converte para inteiros
        numeros = []
        for num_str in numeros_texto:
            try:
                numero = int(num_str)
                numeros.append(numero)
            except ValueError:
                # Ignora valores que não podem ser convertidos para int
                continue
        
        return numeros
    
    def _identificar_duplicados(self) -> List[dict]:
        """
        Identifica números duplicados na sequência.
        
        Returns:
            List[dict]: Lista com números duplicados e suas quantidades
        """
        contador = Counter(self.numeros_encontrados)
        duplicados = []
        
        for numero, quantidade in contador.items():
            if quantidade > 1:
                duplicados.append({
                    'numero': numero,
                    'quantidade': quantidade
                })
        
        # Ordena por número
        duplicados.sort(key=lambda x: x['numero'])
        return duplicados
    
    def _identificar_faltantes(self) -> List[int]:
        """
        Identifica números faltantes na sequência.
        
        Returns:
            List[int]: Lista de números faltantes na sequência
        """
        if not self.numeros_encontrados:
            return []
        
        # Cria set dos números únicos encontrados
        numeros_unicos = set(self.numeros_encontrados)
        
        # Cria sequência completa do menor ao maior número
        if self.menor_numero is not None and self.maior_numero is not None:
            sequencia_completa = set(range(self.menor_numero, self.maior_numero + 1))
        else:
            return []
        
        # Identifica números faltantes
        faltantes = sorted(list(sequencia_completa - numeros_unicos))
        
        return faltantes
    
    def _gerar_estatisticas(self) -> dict:
        """
        Gera estatísticas da análise.
        
        Returns:
            dict: Estatísticas da análise
        """
        total_numeros_encontrados = len(self.numeros_encontrados)
        numeros_unicos = len(set(self.numeros_encontrados))
        total_duplicados = len(self.numeros_duplicados)
        total_faltantes = len(self.numeros_faltantes)
        
        # Calcula tamanho esperado da sequência
        tamanho_esperado = 0
        if self.menor_numero is not None and self.maior_numero is not None:
            tamanho_esperado = self.maior_numero - self.menor_numero + 1
        
        return {
            'total_numeros_arquivo': total_numeros_encontrados,
            'numeros_unicos': numeros_unicos,
            'total_duplicados': total_duplicados,
            'total_faltantes': total_faltantes,
            'tamanho_sequencia_esperada': tamanho_esperado,
            'percentual_completo': round((numeros_unicos / tamanho_esperado * 100), 2) if tamanho_esperado > 0 else 0
        }
    
    def gerar_lista_copia_faltantes(self) -> str:
        """
        Gera uma string formatada dos números faltantes para cópia.
        
        Returns:
            str: String com números faltantes separados por vírgula
        """
        if not self.numeros_faltantes:
            return "Nenhum número faltante"
        
        return ", ".join(map(str, self.numeros_faltantes))