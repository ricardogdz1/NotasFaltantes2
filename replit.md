# Analisador de Sequências Numéricas

## Visão Geral

Aplicação web desenvolvida em Django para análise de sequências numéricas em arquivos TXT. O sistema identifica números faltantes e duplicados, fornecendo relatórios visuais completos e funcionalidade de cópia fácil.

## Funcionalidades Principais

### ✅ Análise de Arquivos TXT
- Upload de arquivos TXT até 5MB
- Suporte a múltiplos formatos de separação:
  - Vírgulas: `1, 2, 3, 4, 6`
  - Quebras de linha: `1\n2\n3\n4\n6`
  - Formato misto: `1,\n2,\n3,\n4,\n6`

### ✅ Identificação de Números Faltantes
- Detecção automática do intervalo da sequência (menor ao maior número)
- Lista completa de todos os números faltantes
- Botão de cópia fácil para a lista de números faltantes
- Visualização em badges organizados

### ✅ Identificação de Números Duplicados
- Detecção de números que aparecem mais de uma vez
- Contagem exata de quantas vezes cada número aparece
- Visualização clara com cards individuais

### ✅ Interface Visual Completa
- Design responsivo com Bootstrap 5
- Estatísticas detalhadas da análise
- Indicadores visuais de status da sequência
- Toast notifications para confirmação de ações

### ✅ Relatórios e Estatísticas
- Total de números no arquivo
- Números únicos encontrados
- Percentual de completude da sequência
- Status geral (Perfeita, Com Duplicados, Incompleta)

## Arquitetura do Projeto

### Backend
- **Django 5.2.6**: Framework web principal
- **WhiteNoise**: Servir arquivos estáticos
- **Python 3.11**: Linguagem de programação

### Frontend
- **Bootstrap 5.3**: Framework CSS responsivo
- **Bootstrap Icons**: Ícones da interface
- **JavaScript Vanilla**: Funcionalidades interativas

### Estrutura de Arquivos
```
├── analisador/                    # Aplicação Django principal
│   ├── templates/analisador/      # Templates HTML
│   │   ├── base.html             # Template base
│   │   ├── index.html            # Página de upload
│   │   └── resultado.html        # Página de resultados
│   ├── servicos.py               # Classe AnalisadorSequencia
│   ├── views.py                  # Views do Django
│   └── urls.py                   # URLs da aplicação
├── analisador_sequencias/         # Configurações do projeto
│   ├── settings.py               # Configurações Django
│   └── urls.py                   # URLs principais
├── manage.py                     # Script de gerenciamento Django
└── replit.md                     # Este arquivo
```

## Classe Principal: AnalisadorSequencia

Localizada em `analisador/servicos.py`, esta classe é responsável por:

- **Extração de números**: Regex para identificar números em diferentes formatos
- **Identificação de duplicados**: Usando Counter para contagem
- **Cálculo de faltantes**: Comparação com sequência completa esperada
- **Geração de estatísticas**: Métricas completas da análise
- **Formatação para cópia**: String pronta para área de transferência

## Configurações Importantes

### Django Settings
- `ALLOWED_HOSTS = ['*']`: Permite acesso de qualquer host (Replit)
- `LANGUAGE_CODE = 'pt-br'`: Interface em português brasileiro
- `TIME_ZONE = 'America/Sao_Paulo'`: Fuso horário brasileiro
- WhiteNoise configurado para arquivos estáticos

### Validações de Segurança
- Validação de tipo de arquivo (.txt apenas)
- Limite de tamanho de arquivo (5MB)
- Codificação UTF-8 obrigatória
- Proteção CSRF habilitada

## Como Usar

1. **Acesse a página inicial**: Interface de upload de arquivo
2. **Selecione um arquivo TXT**: Drag & drop ou clique para selecionar
3. **Aguarde o processamento**: Análise automática da sequência
4. **Visualize os resultados**: Números faltantes, duplicados e estatísticas
5. **Copie os números faltantes**: Botão de cópia fácil disponível

## Exemplos de Uso

### Arquivo com números faltantes e duplicados:
```
1, 2, 3, 5, 7, 8, 9, 12, 15, 15, 18, 20, 20, 20, 22
```
**Resultado**: Identifica números faltantes (4, 6, 10, 11, 13, 14, 16, 17, 19, 21) e duplicados (15 aparece 2x, 20 aparece 3x)

### Arquivo com quebras de linha:
```
10
11
12
15
16
18
18
20
```
**Resultado**: Identifica números faltantes (13, 14, 17, 19) e duplicado (18 aparece 2x)

## Desenvolvimento

### Tecnologias em PT-BR
- Todos os nomes de classes, métodos e comentários em português brasileiro
- Interface de usuário completamente em português
- Mensagens de erro e sucesso em português

### Boas Práticas Implementadas
- Separação clara entre lógica de negócio (servicos.py) e apresentação (views.py)
- Validação robusta de entrada de dados
- Tratamento de exceções adequado
- Interface responsiva e acessível
- Código bem documentado e comentado

## Status do Projeto

✅ **Implementação Completa**
- Todas as funcionalidades solicitadas foram implementadas
- Testes automatizados executados com sucesso  
- Interface visual funcionando perfeitamente
- Botão de cópia implementado com fallback para navegadores antigos
- Servidor Django rodando na porta 5000

### Próximas Melhorias Possíveis
- Histórico de análises do usuário
- Download de relatórios em PDF/Excel
- Suporte para múltiplos arquivos simultaneamente
- Dashboard com estatísticas gerais
- Validação avançada de formatos de arquivo

## Data de Criação
Setembro 16, 2025

## Tecnologias Utilizadas
- Python 3.11
- Django 5.2.6  
- Bootstrap 5.3
- JavaScript ES6+
- HTML5 & CSS3