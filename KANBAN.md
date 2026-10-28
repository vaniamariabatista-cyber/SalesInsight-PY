# Kanban — SalesInsight PY

Quadro em Markdown com as colunas pedidas no enunciado: Backlog, A Fazer, Em Andamento e Concluído.

## Backlog (bônus e melhorias futuras)

- [ ] B01 — Projeção simples de tendência com média móvel
- [ ] B03 — Tabela cruzada (pivot) de mês × categoria
- [ ] B04 — Gráficos adicionais (histograma, boxplot ou mapa de calor)
- [ ] Ajustar as faixas de Bronze, Prata e Ouro para uma distribuição mais equilibrada
- [ ] Aceitar um CSV externo com as mesmas colunas

## A Fazer

- [ ] Gravar o vídeo de demonstração (até 5 minutos)
- [ ] Publicar o vídeo e colocar o link no README
- [ ] Enviar os links do repositório e do vídeo no AVA

## Em Andamento

- [ ] Finalizar o README com decisões técnicas e links
- [ ] Pull requests finais e merge da `develop` na `main`

## Concluído

- [x] Criar o repositório no GitHub e o arquivo `salesinsight.py`
- [x] Gerar o dataset de vendas com dados sujos (`gerar_dataset_vendas`)
- [x] Inspecionar os dados (`inspecionar_dados`)
- [x] Limpar os dados com datetime e relatório de limpeza (`tratar_dados`)
- [x] Criar colunas derivadas com transformação condicional (`criar_colunas_derivadas`)
- [x] Calcular métricas agregadas com `groupby` (`calcular_metricas`)
- [x] Segmentar clientes em Bronze, Prata e Ouro com lambda (`segmentar_clientes`)
- [x] Criar o gráfico de linha (receita por mês)
- [x] Criar o gráfico de barras (top 5 produtos)
- [x] Criar o gráfico de dispersão (quantidade × receita)
- [x] Criar o painel com subplots 2×2 e exportar os PNGs
- [x] Implementar a função de ordem superior e os lambdas (`processar_coluna`)
- [x] Exportar resultados em CSV e JSON e reler o JSON
- [x] Criar a classe `AnalisadorDeVendas` e a função `main()`
- [x] Organizar branches por funcionalidade e commits descritivos
