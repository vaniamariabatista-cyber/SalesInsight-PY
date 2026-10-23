import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

import os

import matplotlib.pyplot as plt
import seaborn as sns

PASTA_GRAFICOS = "outputs/graficos"
COR_PRINCIPAL = "#1f4e79"

def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintetico de vendas com dados sujos."""
    random.seed(seed)
    np.random.seed(seed)

    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor",
                "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares",
                  "Tablet": "Celulares", "Monitor": "Computadores",
                  "Teclado": "Perifericos", "Mouse": "Perifericos",
                  "Headset": "Perifericos"}
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
              "Monitor": 1200, "Teclado": 250, "Mouse": 120,
              "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    data_inicio = datetime(2025, 1, 1)
    dados = []

    for i in range(n_registros):
        produto = random.choice(produtos)
        categoria = categorias[produto]
        quantidade = random.randint(1, 10)
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))
        data_txt = data.strftime("%Y-%m-%d")
        cliente = f"Cliente_{random.randint(1, 50):03d}"

        # sujeira proposital para a etapa de limpeza
        if random.random() < 0.03:
            data_txt = "DATA INVALIDA"

        dados.append({
            "id_venda": i + 1,
            "data_venda": data_txt,
            "cliente": cliente,
            "produto": produto,
            "categoria": categoria,
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco,
        })

    return pd.DataFrame(dados)


def inspecionar_dados(df):
    """Exibe as informacoes estruturais do DataFrame."""
    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Shape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")
    return df

def tratar_dados(df):
    """
    Trata o DataFrame de vendas.
    Retorna: (df_limpo, relatorio), onde relatorio e um dicionario
    com as contagens de registros iniciais, convertidos e finais.
    """
    df = df.copy()
    registros_iniciais = len(df)

    # 1. remover espacos extras nas colunas de texto
    for coluna in ["cliente", "produto", "categoria", "regiao"]:
        df[coluna] = df[coluna].str.strip()

    # 2. converter data_venda; o que nao for data vira NaT
    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    datas_invalidas = int(df["data_venda"].isna().sum())
    df = df.dropna(subset=["data_venda"]).reset_index(drop=True)

    # 3. garantir os tipos numericos
    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)

    # 4. relatorio de limpeza
    relatorio = {
        "registros_iniciais": registros_iniciais,
        "datas_convertidas": registros_iniciais - datas_invalidas,
        "datas_invalidas_removidas": datas_invalidas,
        "registros_finais": len(df),
    }

    print("\n=== RELATORIO DE LIMPEZA ===")
    for chave, valor in relatorio.items():
        print(f"{chave}: {valor}")

    return df, relatorio

def criar_colunas_derivadas(df):
    """Cria receita, mes, trimestre, ano e faixa de valor da venda."""
    df = df.copy()

    # receita da linha: quantidade x preco (a coluna toda de uma vez)
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]

    # partes da data
    meses = {1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril",
             5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
             9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
    df["mes"] = df["data_venda"].dt.month
    df["mes_nome"] = df["mes"].map(meses)
    df["trimestre"] = "Q" + df["data_venda"].dt.quarter.astype(str)
    df["ano"] = df["data_venda"].dt.year

    # faixa de valor, por condicoes
    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000,
    ]
    faixas = ["Baixo Valor", "Medio Valor", "Alto Valor"]

    df["faixa_receita_item"] = "Nao Classificado"
    for condicao, faixa in zip(condicoes, faixas):
        df.loc[condicao, "faixa_receita_item"] = faixa

    return df


def calcular_metricas(df):
    """
    Calcula as metricas agregadas do dataset.
    Retorna um dicionario no formato {nome_da_metrica: DataFrame}.
    """
    metricas = {}

    # receita, quantidade e numero de vendas por mes
    metricas["por_mes"] = (
        df.groupby("mes")
        .agg(receita_total=("receita_total", "sum"),
             quantidade=("quantidade", "sum"),
             n_vendas=("id_venda", "count"))
        .reset_index()
    )

    # top 5 produtos por receita
    metricas["top_produtos"] = (
        df.groupby("produto")["receita_total"].sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    # receita por categoria
    metricas["por_categoria"] = (
        df.groupby("categoria")["receita_total"].sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # receita e ticket medio por regiao
    metricas["por_regiao"] = (
        df.groupby("regiao")
        .agg(receita_total=("receita_total", "sum"),
             ticket_medio=("receita_total", "mean"))
        .sort_values("receita_total", ascending=False)
        .reset_index()
    )

    # exibicao legivel no console
    for nome, tabela in metricas.items():
        print(f"\n=== {nome.upper().replace('_', ' ')} ===")
        print(tabela.round(2).to_string(index=False))

    return metricas

def segmentar_clientes(df):
    """
    Agrupa por cliente, soma a receita e classifica em
    Bronze / Prata / Ouro.
    Retorna um DataFrame com: cliente, total_gasto, segmento.
    """
    clientes = (
        df.groupby("cliente")["receita_total"].sum()
        .reset_index()
        .rename(columns={"receita_total": "total_gasto"})
        .sort_values("total_gasto", ascending=False)
        .reset_index(drop=True)
    )

    # lambda: recebe o total de um cliente e devolve o segmento
    clientes["segmento"] = clientes["total_gasto"].apply(
        lambda total: "Bronze" if total < 5000
        else ("Prata" if total <= 15000 else "Ouro")
    )

    print("\n=== TOP 10 CLIENTES ===")
    print(clientes.head(10).round(2).to_string(index=False))

    print("\n=== CLIENTES POR SEGMENTO ===")
    print(clientes["segmento"].value_counts())

    return clientes

def _salvar(fig, nome):
    """Ajusta o layout e salva a figura como PNG."""
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    fig.tight_layout()
    fig.savefig(f"{PASTA_GRAFICOS}/{nome}", dpi=150)
    plt.close(fig)


def _plot_linha(ax, por_mes):
    """Desenha a receita total por mes em um eixo."""
    ax.plot(por_mes["mes"], por_mes["receita_total"],
            marker="o", linewidth=2, color=COR_PRINCIPAL)
    ax.set_title("Receita Total por Mes")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Receita Total (R$)")
    ax.set_xticks(por_mes["mes"])
    ax.grid(True, alpha=0.3)


def gerar_graficos(df, metricas):
    """Gera e exporta as figuras do projeto."""
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(10, 6))
    _plot_linha(ax, metricas["por_mes"])
    _salvar(fig, "receita_por_mes.png")

    print(f"\nGraficos salvos em {PASTA_GRAFICOS}")

def main():
    df = gerar_dataset_vendas()
    df.to_csv("vendas.csv", index=False)
    print(f"Dataset gerado com {len(df)} registros.")

    df_bruto = pd.read_csv("vendas.csv")
    inspecionar_dados(df_bruto)

    df_limpo, relatorio = tratar_dados(df_bruto)
    print(df_limpo.dtypes)

    df_final = criar_colunas_derivadas(df_limpo)
    print(df_final.head())

    metricas = calcular_metricas(df_final)

    clientes = segmentar_clientes(df_final)

    gerar_graficos(df_final, metricas)
    
if __name__ == "__main__":
    main()