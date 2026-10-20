import pandas as pd
import random
from datetime import datetime, timedelta

def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um conjunto fictício de vendas."""

    random.seed(seed)

    produtos = {
        "Notebook": ("Computadores", 3500.00),
        "Smartphone": ("Celulares", 1800.00),
        "Tablet": ("Tablets", 1200.00),
        "Monitor": ("Periféricos", 900.00),
        "Teclado": ("Periféricos", 250.00),
        "Mouse": ("Periféricos", 120.00),
        "Headset": ("Periféricos", 350.00),
    }

    clientes = [
        "Ana", "Bruno", "Carla", "Daniel",
        "Elisa", "Felipe", "Gabriela", "Henrique",
        "Isabela", "João"
    ]

    regioes = ["Sul", "Sudeste", "Centro-Oeste", "Nordeste", "Norte"]

    data_inicial = datetime(2025, 1, 1)
    dados = []

    for i in range(n_registros):
        produto = random.choice(list(produtos.keys()))
        categoria, preco_base = produtos[produto]

        quantidade = random.randint(1, 10)
        preco_unitario = round(
            preco_base * random.uniform(0.85, 1.15), 2
        )

        data_venda = data_inicial + timedelta(
            days=random.randint(0, 364)
        )

        dados.append({
            "id_venda": i + 1,
            "data_venda": data_venda,
            "cliente": random.choice(clientes),
            "produto": produto,
            "categoria": categoria,
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
        })

    return pd.DataFrame(dados)

def main():
    """Executa a geração inicial dos dados."""

    df = gerar_dataset_vendas()

    df.to_csv("vendas.csv", index=False)

    print("Dataset gerado com sucesso!")
    print(f"Quantidade de registros: {len(df)}")
    print("\nPrimeiras cinco vendas:")
    print(df.head())

if __name__ == "__main__":
    main()