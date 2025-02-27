# 📊 Data Lakehouse - Análise de Smartphones

Este projeto implementa um **Data Lakehouse** utilizando **Scrapy, Supabase, PostgreSQL e DBT** para extrair, transformar e analisar dados de smartphones disponíveis no mercado.  

A solução coleta dados da **Amazon** e estrutura as informações em um **Data lakehoue** e permite análise de preços, avaliações e configurações dos dispositivos.  

## **🚀 Arquitetura do projeto**
![Arquitetura do projeto](/images/project.png)

## **🛠️ Tecnologias Utilizadas**

### **1️⃣ Scrapy**
- **Coleta de dados da Amazon e Mercado Livre**
- **Automação do processo de Web Scraping**
- **Pipeline para armazenamento dos dados brutos no bucket do Supabase**
- **Items para estruturação dos dados coletados**

### **2️⃣ Supabase (Storage e Banco de Dados)**
- **Armazena os dados brutos na camada Raw (bucket)**
- **Armazena os dados brutos oriundos do bucket no banco de dados PostgreSQL**
- **Armazena os dados tratados na camada Silver (tabelas processadas)**
- **Armazena os dados analíticos na camada Gold (tabelas analíticas)**

### **3️⃣ DBT (Data Build Tool)**
- **Processamento e transformação dos dados**
- **Criação de modelos na camada Silver (dados tratados)**
- **Criação de tabelas analíticas na camada Gold (insights e KPIs)**

### **4️⃣ PostgreSQL**
- **Armazena as tabelas brutas, processadas e analíticas**
- **Permite consultas e análises otimizadas**



## **⚙️ Como Funciona o Pipeline?**

### **🔹 1. Extração dos Dados (ETL)**
📌 O Scrapy coleta **informações de smartphones** da **Amazon** e armazena no **Supabase Storage (Camada Raw)**.  

✅ **Pipeline do Scrapy (`pipelines.py`)**
1. Os dados brutos são **coletados e armazenados no Supabase**.  
2. Antes do upload, **os arquivos antigos são removidos automaticamente** para evitar duplicação.  
3. Os arquivos são salvos no formato **JSON** dentro do bucket organizado por **Ano/Mês**.


### **🔹 2. Carga dos Dados na Camada Bronze**
📌 Um processo de ETL carrega os dados do **bucket para o banco de dados postgres**, criando a **Camada Bronze**, onde os dados brutos são armazenados sem transformações.  

✅ **Tabela `bronze_amazon_products`**  


### **🔹 3. Transformação dos Dados na Camada Silver**
📌 O **DBT** processa os dados da **Camada Bronze** e gera a **Camada Silver**, onde os dados são limpos e estruturados.  

✅ **Remoção de caracteres especiais e espaços desnecessários**  
✅ **Extração de marca, modelo, RAM e ROM corretamente**  
✅ **Formatação do preço e das avaliações**  
✅ **Formatação de tipos de dados**
✅ **Correção da data de extração**  


### **🔹 4. Análises e Insights na Camada Gold
📌 A Camada Gold agrega os dados para insights estratégicos, respondendo perguntas como: ✅ Qual a média de preços por marca?
✅ **Comparative analysis**
✅ **Memory distribution**
✅ **price analysis**
✅ **price segmentation**
✅ **price trend**
✅ **rating analysis**
✅ **top 10 cheapest smartphones**
✅ **top 10 most expensive smartphones**


### **🔹 5. Proximos passos**
**🔹 Agendar a execução do pipeline automaticamente (via cron job ou Airflow)**
**🔹 Criar visualizações em um Dashboard (com Metabase, Superset ou Power BI)**
**🔹 Incluir mais fontes de dados (expandir além do Mercado Livre e Amazon)**
