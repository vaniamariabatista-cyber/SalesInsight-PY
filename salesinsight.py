import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


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


def main():
    df = gerar_dataset_vendas()
    df.to_csv("vendas.csv", index=False)
    print(f"Dataset gerado com {len(df)} registros.")

    df_bruto = pd.read_csv("vendas.csv")
    inspecionar_dados(df_bruto)

    df_limpo, relatorio = tratar_dados(df_bruto)
    print(df_limpo.dtypes)


if __name__ == "__main__":
    main()