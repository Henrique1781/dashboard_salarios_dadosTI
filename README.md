# 📊 Dashboard de Análise de Salários na Área de Dados

Este é um dashboard interativo criado com Streamlit para explorar e analisar dados de salários na área de tecnologia e dados. O projeto permite que os usuários visualizem informações salariais de forma dinâmica, aplicando filtros e explorando diferentes aspectos dos dados através de gráficos interativos.

**Acesse a aplicação online:** [Dashboard de Salários](https://salarios-na-area-de-dadosti.streamlit.app/)

## ✨ Funcionalidades Principais

* **Conversão de Moeda em Tempo Real:** O dashboard busca a cotação mais recente do dólar americano (USD) para o real brasileiro (BRL) via API para apresentar os valores salariais atualizados.
* **Filtros Dinâmicos:** Permite a filtragem dos dados por:
    * Ano
    * Nível de senioridade
    * Tipo de contrato
    * Tamanho da empresa
* **Métricas Gerais (KPIs):** Apresenta cartões com as principais métricas calculadas a partir dos filtros selecionados, como Salário Médio, Salário Máximo, Total de Registros e o Cargo Mais Frequente.
* **Visualizações Interativas:** Utiliza a biblioteca Plotly para gerar gráficos detalhados e interativos:
    * **Top 10 Cargos por Salário Médio:** Gráfico de barras horizontais com os cargos de maior remuneração.
    * **Distribuição Salarial:** Histograma que mostra a frequência das diferentes faixas salariais.
    * **Proporção de Tipos de Trabalho:** Gráfico de pizza que ilustra a distribuição entre trabalho remoto, híbrido e presencial.
    * **Mapa de Salários por País:** Um mapa coroplético que exibe a média salarial para Cientistas de Dados por país.
* **Tabela de Dados Detalhada:** Exibe os dados brutos (em USD) que correspondem aos filtros aplicados, permitindo uma análise mais granular.
* **Interface Customizada:** O dashboard possui um tema escuro e um layout limpo para uma melhor experiência de usuário.

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Streamlit:** Framework para a criação do dashboard web interativo.
* **Pandas:** Para manipulação e análise dos dados.
* **Plotly:** Para a criação dos gráficos interativos.
* **Requests:** Para realizar chamadas à API de cotação de moedas.

## 🚀 Como Executar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run app.py
    ```

A aplicação será aberta no seu navegador padrão.

## 📄 Dados

Os dados utilizados neste projeto foram obtidos do seguinte repositório e são carregados diretamente no dashboard: [vqrca/dashboard\_salarios\_dados](https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv).
