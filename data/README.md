##  Pipeline de Streaming de Dados - Desafio Serasa

Este projeto implementa um pipeline de engenharia de dados completo, focado em alta performance, escalabilidade e organização de um Data Lake moderno.

##  Tecnologias Utilizadas
- **Producer (Flask-SSE):** Geração de eventos de streaming baseados no dataset de táxis de NYC.
- **Consumer (DuckDB):** Consumo dos eventos com motor SQL OLAP para filtragem em tempo real.
- **Armazenamento (Parquet):** Persistência dos dados consolidados em formato colunar de alta compressão.
- **Orquestração (Docker Compose):** Ambiente totalmente containerizado para garantir a reprodutibilidade.

##  Arquitetura e Filtros
A aplicação realiza a ingestão dos dados e aplica regras de negócio diretamente no stream:
1. **Qualidade de Dados:** Filtra registros onde `passenger_count > 0` utilizando o **DuckDB**.
2. **Transformação:** Converte timestamps para colunas de tempo (ano, mês, dia).
3. **Data Lake:** Salva os arquivos no diretório `data/analytics/` utilizando o padrão de **Particionamento Hive** (`ano=YYYY/mes=MM/dia=DD`), o que otimiza drasticamente as consultas analíticas.

##  Como Executar

1. **Subir o ambiente:**
   ```bash
   docker-compose up --build