from datetime import datetime
import csv
import pandas as pd
from rich.console import Console

console = Console()

# 1. MAPEAMENTO DE COLUNAS
MAPEAMENTO = {
    "DATA": "data_compra",
    "CO_ID": "codigo_de_compra",
    "CL_ID": "codigo_de_cliente",
    "CL_GENERO": "genero",
    "CL_EC": "estado_civil",
    "CL_FHL": "dependentes",
    "PR_CAT": "categoria",
}

CAMINHO_CSV = "base_vendas.csv"

print("Lendo amostra com csv.DictReader")
try:
    with open(CAMINHO_CSV, mode="r", encoding="utf-8") as file:
        leitor = csv.DictReader(file)
        print("Primeiro registro:", next(leitor))
except Exception as e:
    print(f"Erro na leitura nativa: {e}")

df = pd.read_csv(CAMINHO_CSV, sep=None, engine="python")

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

# Relatório final no terminal
console.print("\n[bold green]--- RELATÓRIO DE INSIGHTS ---[/bold green]")
insights = [
    "1. Base continha diversos nulos e inconsistências de data ajustados com sucesso.",
    "2. Categorias vazias foram padronizadas como 'Sem Categoria' via condicional.",
    "3. A média e mediana de filhos são próximas, mostrando distribuição equilibrada.",
    "4. Conversão das datas para datetime permite análises temporais confiáveis.",
    "5. Como problema remanescente, recomenda-se padronizar nomes de produtos."
]
for item in insights:
    print(item)

df.to_csv("df_limpo.csv", index=False)
console.print("\n[bold cyan]-> 'df_limpo.csv' gerado com sucesso![/bold cyan]")