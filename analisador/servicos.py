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
        self.limite_gap = 1000  # Limite para gaps muito grandes
        self.limite_total_numeros = 50000  # Limite total de números a processar
    
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
            
            # Verificar se o gap é muito grande
            tamanho_sequencia = self.maior_numero - self.menor_numero + 1
            
            if tamanho_sequencia > self.limite_total_numeros:
                return {
                    'sucesso': False,
                    'erro': f'O intervalo da sequência é muito grande ({tamanho_sequencia:,} números). '
                           f'Para análises de sequências com mais de {self.limite_total_numeros:,} números, '
                           f'considere dividir o arquivo em partes menores.',
                    'numeros_encontrados': [],
                    'numeros_faltantes': [],
                    'numeros_duplicados': [],
                    'estatisticas': {},
                    'gap_muito_grande': True
                }
            
            # Identificar números faltantes (agora com otimização)
            self.numeros_faltantes = self._identificar_faltantes_otimizado()
            
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
                },
                'gap_detectado': self._detectar_gaps_grandes()
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
    
    def _detectar_gaps_grandes(self) -> List[dict]:
        """
        Detecta gaps grandes na sequência que podem indicar diferentes blocos.
        
        Returns:
            List[dict]: Lista com informações sobre gaps grandes
        """
        if not self.numeros_encontrados:
            return []
        
        numeros_unicos = sorted(set(self.numeros_encontrados))
        gaps_grandes = []
        
        for i in range(len(numeros_unicos) - 1):
            gap = numeros_unicos[i + 1] - numeros_unicos[i] - 1
            if gap > self.limite_gap:
                gaps_grandes.append({
                    'inicio': numeros_unicos[i],
                    'fim': numeros_unicos[i + 1],
                    'tamanho_gap': gap
                })
        
        return gaps_grandes
    
    def _identificar_faltantes_otimizado(self) -> List[int]:
        """
        Versão otimizada para identificar números faltantes na sequência.
        Evita problemas de memória com gaps muito grandes.
        
        Returns:
            List[int]: Lista de números faltantes na sequência
        """
        if not self.numeros_encontrados:
            return []
        
        # Cria set dos números únicos encontrados
        numeros_unicos_set = set(self.numeros_encontrados)
        numeros_unicos_lista = sorted(numeros_unicos_set)
        
        # Verifica se há gaps muito grandes
        gaps_grandes = self._detectar_gaps_grandes()
        
        faltantes = []
        
        # Se não há gaps grandes, usa método tradicional
        if not gaps_grandes:
            if self.menor_numero is not None and self.maior_numero is not None:
                for numero in range(self.menor_numero, self.maior_numero + 1):
                    if numero not in numeros_unicos_set:
                        faltantes.append(numero)
        else:
            # Com gaps grandes, analisa apenas blocos consecutivos
            faltantes = self._identificar_faltantes_por_blocos(numeros_unicos_lista)
        
        return faltantes
    
    def _identificar_faltantes_por_blocos(self, numeros_ordenados: List[int]) -> List[int]:
        """
        Identifica números faltantes analisando apenas blocos consecutivos.
        Evita análise de gaps muito grandes.
        
        Args:
            numeros_ordenados: Lista de números únicos ordenados
            
        Returns:
            List[int]: Lista de números faltantes em blocos consecutivos
        """
        if len(numeros_ordenados) <= 1:
            return []
        
        faltantes = []
        numeros_set = set(numeros_ordenados)
        
        for i in range(len(numeros_ordenados) - 1):
            atual = numeros_ordenados[i]
            proximo = numeros_ordenados[i + 1]
            gap = proximo - atual - 1
            
            # Só analisa gaps pequenos
            if 0 < gap <= self.limite_gap:
                for num in range(atual + 1, proximo):
                    faltantes.append(num)
        
        return faltantes
    
    def _identificar_faltantes(self) -> List[int]:
        """
        MÉTODO LEGACY - Mantido para compatibilidade.
        Use _identificar_faltantes_otimizado() para melhor performance.
        """
        return self._identificar_faltantes_otimizado()
    
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
        
        # Detecta se há gaps grandes
        gaps_grandes = self._detectar_gaps_grandes()
        tem_gaps_grandes = len(gaps_grandes) > 0
        
        estatisticas = {
            'total_numeros_arquivo': total_numeros_encontrados,
            'numeros_unicos': numeros_unicos,
            'total_duplicados': total_duplicados,
            'total_faltantes': total_faltantes,
            'tamanho_sequencia_esperada': tamanho_esperado,
            'percentual_completo': round((numeros_unicos / tamanho_esperado * 100), 2) if tamanho_esperado > 0 else 0,
            'tem_gaps_grandes': tem_gaps_grandes,
            'total_gaps_grandes': len(gaps_grandes)
        }
        
        return estatisticas
    
    def gerar_lista_copia_faltantes(self) -> str:
        """
        Gera uma string formatada dos números faltantes para cópia.
        
        Returns:
            str: String com números faltantes separados por vírgula
        """
        if not self.numeros_faltantes:
            return "Nenhum número faltante"
        
        # Se há muitos números faltantes, sugere análise por blocos
        if len(self.numeros_faltantes) > 1000:
            return f"Muitos números faltantes ({len(self.numeros_faltantes)}). Considere analisar por blocos menores."
        
        return ", ".join(map(str, self.numeros_faltantes))
    
    def gerar_relatorio_gaps(self) -> str:
        """
        Gera relatório sobre gaps grandes detectados.
        
        Returns:
            str: Relatório formatado sobre gaps grandes
        """
        gaps = self._detectar_gaps_grandes()
        
        if not gaps:
            return "Nenhum gap grande detectado na sequência."
        
        relatorio = f"Detectados {len(gaps)} gaps grandes:\n"
        for i, gap in enumerate(gaps, 1):
            relatorio += f"{i}. Entre {gap['inicio']} e {gap['fim']}: {gap['tamanho_gap']} números faltantes\n"
        
        return relatorio
