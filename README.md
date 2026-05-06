# Sales PowerBI Dashboard

Um projeto de visualização e análise de dados de vendas usando **Power BI**, focado em transformação de dados e criação de dashboards interativos para insights de negócio.

## Sobre

Este projeto demonstra uma abordagem profissional para análise e visualização de dados de vendas, aplicando best practices como limpeza de dados, modelagem dimensional e criação de KPIs visualmente efetivos. É um exemplo de como um analista de dados pode estruturar pipelines de dados que transformam dados brutos em insights acionáveis e dashboards de alta qualidade.

---

### Por que Power BI?

- **Visualizações interativas**: criar dashboards dinâmicos e responsivos
- **Integração com múltiplas fontes**: conectar dados de diferentes sistemas
- **Análise em tempo real**: monitorar métricas de vendas constantemente
- **Escalabilidade**: fácil adicionar novos relatórios e KPIs sem retrabalho

---

## 📊 Estrutura do Projeto

```
Sales_PowerBI_dashboard/
├── data/                      # Dados brutos de origem
│   ├── sales_data.csv        # Dados de transações de vendas
│   ├── customers.csv         # Informações de clientes
│   └── products.csv          # Informações de produtos
├── scripts/                   # Scripts de processamento
│   ├── data_cleaning.py      # Limpeza e validação de dados
│   ├── data_transformation.py # Transformações e enriquecimento
│   └── etl_pipeline.py       # Orquestrador do pipeline
├── dashboards/               # Arquivos Power BI
│   └── Sales_Dashboard.pbix  # Dashboard principal de vendas
└── README.md                 # Este arquivo
```

---

## 🔄 Fluxo de Dados

### **Etapa 1: Extração de Dados**

A primeira etapa envolve:
- **Ler arquivos** de sistemas de origem (CSVs)
- **Validar estrutura** dos dados de entrada
- **Documentar** metadados e origem dos dados

### **Etapa 2: Limpeza e Transformação**

A transformação dos dados inclui:
- **Limpeza de dados**: remoção de espaços em branco, tratamento de valores nulos
- **Validação de tipos**: conversão correta de tipos de dados (datas, números, categorias)
- **Enriquecimento**: cálculo de métricas, normalização de valores
- **Remoção de duplicatas**: garantir unicidade dos registros

### **Etapa 3: Modelagem para BI**

A estrutura dos dados é otimizada seguindo o padrão **Star Schema**:

#### Tabelas Dimensionais:

**Dimensão: Customers**
- customer_id
- customer_name
- city
- region
- customer_segment

**Dimensão: Products**
- product_id
- product_name
- category
- subcategory
- unit_price

**Dimensão: Date** (Calendário)
- date_key
- date
- month
- quarter
- year

#### Tabela de Fatos:

**Sales (Fatos)**
- order_id
- customer_id
- product_id
- date_id
- quantity
- unit_price
- total_amount
- discount
- net_sales

---

## 📈 KPIs Principais no Dashboard

- **Total de Vendas**: receita total no período
- **Número de Transações**: volume de pedidos
- **Ticket Médio**: valor médio por transação
- **Top 10 Produtos**: produtos mais vendidos
- **Vendas por Região**: distribuição geográfica
- **Crescimento MoM**: variação mês a mês
- **Taxa de Desconto**: impacto de promoções

---

## 🚀 Como Executar

### Pré-requisitos:
- Python 3.8+
- pandas, numpy
- Power BI Desktop (ou acesso ao Power BI Service)
- Arquivos de dados de origem em `/data`

### Passos:

1. **Preparar dados brutos**
   ```bash
   python scripts/data_cleaning.py
   ```

2. **Executar transformações**
   ```bash
   python scripts/data_transformation.py
   ```

3. **Rodar pipeline completo**
   ```bash
   python scripts/etl_pipeline.py
   ```

4. **Abrir dashboard no Power BI**
   - Abrir `dashboards/Sales_Dashboard.pbix`
   - Atualizar conexão com dados transformados
   - Interagir com visualizações

---

## 📋 Tecnologias Utilizadas

- **Python**: scripts de ETL
- **Pandas**: manipulação e transformação de dados
- **Power BI**: visualização e dashboards
- **SQL**: modelagem de dados (se aplicável)

---

## 👤 Autor

**Andreas de Carvalho** - Engenheiro de Dados / Analista de Dados

---

## 📝 Notas

Este projeto é um exemplo educacional de pipeline de dados para BI, demonstrando boas práticas em limpeza, transformação e visualização de dados de vendas.
