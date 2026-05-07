# Sales PowerBI Dashboard

Um projeto de visualização e análise de dados de vendas usando **Power BI**, focado em transformação de dados e criação de dashboards interativos para insights de negócio.

## Sobre

Este projeto demonstra uma abordagem profissional para análise e visualização de dados de vendas, aplicando best practices como limpeza de dados, modelagem dimensional e criação de KPIs visualmente efetivos. É um exemplo de como um analista de dados pode estruturar pipelines de dados que transformam dados brutos em insights acionáveis e dashboards de alta qualidade.


---

##  Estrutura do Projeto

```
Sales_PowerBI_dashboard/
├── .env
├── .gitignore
├── ETL
│   ├── bronze
│   │   └── extract.py
│   ├── deliver.py
│   ├── gen_fake_sales.py
│   ├── gold
│   │   └── gold_csv.py
│   └── silver
│       ├── dummy.py
│       ├── fakestore.py
│       └── silver_functions.py
├── README.md
├── core
│   ├── config.py
│   ├── logger.py
│   └── logs
│       └── etl.log
├── main.py
└──requirements.txt
```

---

##  Fluxo de Dados

### **Etapa 1: Extração de Dados**

A primeira etapa envolve:
- Extrair dados de produtos via API
- Validar estrutura dos dados de entrada
- Documentar metadados e origem dos dados

### **Etapa 2: Limpeza e Transformação**

A transformação dos dados inclui:
- **Limpeza de dados**: remoção de espaços em branco, tratamento de valores nulos
- **Validação de tipos**: conversão correta de tipos de dados (datas, números, categorias)
- **Enriquecimento**: cálculo de métricas, normalização de valores
- **Remoção de duplicatas**: garantir unicidade dos registros

### **Etapa 3: Modelagem para BI**

A estrutura dos dados é otimizada seguindo o padrão **Star Schema**:

#### Tabelas Dimensionais:

**Dimensão: Products**
- id
- product
- category
- price
- rating


#### Tabela de Fatos:

**Sales (Fatos)**
- id
- product_id
- date_id
- quantity
- gross_profit

---

### **Etapa 4: Dashboard em BI**

<img width="976" height="538" alt="dashboard print (1)" src="https://github.com/user-attachments/assets/cfd76f9b-cfb0-4b3d-bb0c-e5a30328fa00" />

##  KPIs Principais no Dashboard

- **Lucro Total**
- **Quantidade de Unidades Vendidas**
- **Número de Vendas**
- **Lucro por Dia**
- **Lucro por Produto**
- **Quantidade de Unidades Vendidas por Produto**
- **Lucro por Categoria de produtos**

---

##  Como Executar

```bash
python3 main.py
```

E toda a pipeline é executada

---

##  Tecnologias Utilizadas

- **Python**: scripts de ETL
- **Pandas**: manipulação e transformação de dados
- **Power BI**: visualização e dashboards
- **SQL**: modelagem de dados 

---

##  Autor

**Andreas de Carvalho** - Engenheiro de Dados / Analista de Dados

