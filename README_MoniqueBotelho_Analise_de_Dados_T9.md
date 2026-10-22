ETAPA 1: PREPARANDO O COMPUTADOR

1.1 Após a instalação já realizada anteriormente do VS Code e do Python conferir se deu certo através do terminal digitando: python --version

1.2 Criar e abrir a pasta do projeto:
- Criar uma pasta chamada Mini_projeto no computador;
- No VS Code, vá em Arquivo → Abrir Pasta... e escolha a pasta Mini_projeto;
- Abra o terminal do VS Code em Terminal → Novo Terminal (ou Ctrl+').

1.3 Criar o ambiente virtual (venv):
- No terminal do VS Code, dentro da pasta do projeto, crie o ambiente digitando: python -m venv .venv ;
- Depois, ative o ambiente digitando no terminal: .\.venv\Scripts\Activate.ps1 ;
- O começo da linha do terminal deverá passar a mostrar (.venv).

1.4 Instalar as bibliotecas no terminal:
pip install pandas
pip install rich
pip install datetime

ETAPA 2 - IMPORTAÇÃO DE DADOS

2.1 Realizar a importação dos dados na plataforma Kaggle (base_varejo.csv) para o IDE do VS Code, dentro da pasta Mini_projeto.

ETAPA 3 - CRIAR ARQUIVO
3.1 Criado o arquivo codigo_fonte.py : desenvolvimento do código.

3.2 Construção do código:

from datetime import datetime: carregando a biblioteca e carregando a ferramenta;
import csv: carrega a biblioteca nativa do Python usada para ler e escrever arquivos; em formato CSV;
import pandas as pd: carregamento da bibilioteca pandas;
from rich.console import Console: traz o Console da biblioteca rich. É ele que desenha tabelas e cores no terminal;
# Mapeamento de Colunas: 
Renomear as colunas originais de uma base de dados para nomes mais claros, amigáveis ou padronizados;
# Lendo amostra com csv.DictReader: 
Tenta abrir um arquivo CSV com segurança, lê a primeira linha de dados e trata eventuais erros de leitura.
# Renomeia colunas e remove extras
df = df.rename(columns=MAPEAMENTO)
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
# Funções simples de limpeza
def limpar_texto(val):
    if pd.isna(val) or str(val).strip() in ['', 'none']:
        return "Sem Categoria"
    return str(val).strip().title()
def limpar_int(val):
    try:
        return int(float(val)) if pd.notna(val) else None
    except (ValueError, TypeError):
        return None
def limpar_data(val):
    if pd.isna(val):
        return None
    data_str = str(val).strip()
    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d']:
        try:
            return datetime.strptime(data_str, fmt)
        except ValueError:
            pass
    return None
# Aplicação da limpeza
df['categoria'] = df['categoria'].apply(limpar_texto)
df['codigo_de_cliente'] = df['codigo_de_cliente'].apply(limpar_int)
df['dependentes'] = df['dependentes'].apply(limpar_int)
df['data_compra'] = df['data_compra'].apply(limpar_data)
# Dimensão física (se existir na base)
if 'dimensao_cm' in df.columns:
    df['dimensao_cm'] = df['dimensao_cm'].fillna("0x0x0")
# Remoção de duplicatas relevantes
if 'codigo_de_compra' in df.columns and 'data_compra' in df.columns:
    df = df.drop_duplicates(subset=['codigo_de_compra', 'data_compra'], keep='first')
console.print("[bold green]✓ Limpeza e tratamento concluídos![/bold green]\n")
console.print("[bold yellow] Estatísticas de Filhos/Dependentes [/bold yellow]")
col_filhos = df['dependentes'].dropna()
estatisticas = {
    "Contagem": col_filhos.count(),
    "Média": round(col_filhos.mean(), 2),
    "Mediana": col_filhos.median(),
    "Desvio Padrão": round(col_filhos.std(), 2),
    "Moda": col_filhos.mode().iloc[0] if not col_filhos.mode().empty else "N/A",
    "Mínimo": col_filhos.min(),
    "Máximo": col_filhos.max(),
    "Q1 (25%)": col_filhos.quantile(0.25),
    "Q2 (50%)": col_filhos.quantile(0.50),
    "Q3 (75%)": col_filhos.quantile(0.75)
}
for k, v in estatisticas.items():
    print(f"{k}: {v}")
console.print("\n[bold yellow] Agrupamentos e Insights [/bold yellow]")
# Agrupamento 1: Compras por Categoria
if 'categoria' in df.columns:
    print("\n1. Volume por Categoria:")
    print(df.groupby('categoria').size().head(5))
# Agrupamento 2: Gênero vs Estado Civil
if 'genero' in df.columns and 'estado_civil' in df.columns:
    print("\n2. Cruzamento Gênero x Estado Civil:")
    print(pd.pivot_table(df, index='genero', columns='estado_civil', aggfunc='size', fill_value=0))

ETAPA 5 - INSERÇÃO DOS ARQUIVOS DO MINI PROJETO NO GITHUB
3.1 Clique no ícone de Controle de Código Fonte e em Iniciar o Repositório;
3.2 Fazer Commit e Sincronizar, adicionar uma mensagem de commit, clicar no botão de confirmação e utilizar a opção de sincronizar para enviar os dados para a plataforma Github.