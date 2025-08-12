import streamlit as st
import pandas as pd
import plotly.express as px
import requests  # Importa a biblioteca para fazer requisições HTTP

# --- Função para buscar a taxa de câmbio ---
def get_exchange_rate():
    """Busca a taxa de câmbio USD-BRL de uma API pública."""
    try:
        # Usando uma API Para a taxa brl
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        response.raise_for_status()  # Lança um erro se a requisição falhar
        data = response.json()
        return data['rates']['BRL']
    except requests.exceptions.RequestException as e:
        st.warning(f"Não foi possível buscar a taxa de câmbio online. Usando taxa fixa. Erro: {e}")
        return 5.44  

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados e da taxa de câmbio ---
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")
taxa_brl = get_exchange_rate()


# --- Dicionário de Tradução de Cargos (EXPANDIDO) ---
traducoes_cargos = {
    'Data Scientist': 'Cientista de Dados',
    'Data Analyst': 'Analista de Dados',
    'Data Engineer': 'Engenheiro de Dados',
    'Machine Learning Engineer': 'Engenheiro de Machine Learning',
    'Analytics Engineer': 'Engenheiro de Analytics',
    'BI Analyst': 'Analista de BI',
    'Business Analyst': 'Analista de Negócios',
    'Data Architect': 'Arquiteto de Dados',
    'Research Scientist': 'Pesquisador Cientista',
    'Data Manager': 'Gerente de Dados',
    #top 10 cargos
    'Research Team Lead': 'Líder de Equipe de Pesquisa',
    'Analytics Engineering Manager': 'Gerente de Engenharia de Analytics',
    'Data Science Tech Lead': 'Líder Técnico de Ciência de Dados',
    'Applied AI ML Lead': 'Líder de IA Aplicada e ML',
    'Head of Applied AI': 'Chefe de IA Aplicada',
    'Head of Machine Learning': 'Chefe de Machine Learning',
    'Machine Learning Performance Engineer': 'Engenheiro de Performance de ML',
    'Director of Product Management': 'Diretor de Gestão de Produtos',
    'Engineering Manager': 'Gerente de Engenharia',
    'AWS Data Architect': 'Arquiteto de Dados AWS'
}

# --- Pré-processamento dos Dados ---
df['brl'] = df['usd'] * taxa_brl
df['cargo_br'] = df['cargo'].map(traducoes_cargos).fillna(df['cargo'])


st.markdown("""
    <style>
        /* Cor de fundo principal e cor do texto */
        .main {
            background-color: #0e1117;
            color: #fafafa;
        }
        /* Estilo para o contêiner de métricas */
        [data-testid="stMetric"] {
            background-color: #262730;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }
        /* Centraliza o valor da métrica */
        [data-testid="stMetricValue"] {
            justify-content: center;
        }
        /* Remove elementos padrão do Streamlit para um visual mais limpo */
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        /* Estilo para o rodapé */
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0e1117;
            color: #888;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Barra Lateral (Filtros Dinâmicos) ---
st.sidebar.header("🔍 Filtros")
st.sidebar.info(f"Cotação do Dólar: R$ {taxa_brl:.2f}") # Mostra a cotação na barra lateral


configuracao_filtros = [
    {"label": "Ano", "coluna": "ano"},
    {"label": "Senioridade", "coluna": "senioridade"},
    {"label": "Tipo de Contrato", "coluna": "contrato"},
    {"label": "Tamanho da Empresa", "coluna": "tamanho_empresa"},
]

selecoes = {}

for filtro in configuracao_filtros:
    label = filtro["label"]
    coluna = filtro["coluna"]
    opcoes_disponiveis = sorted(df[coluna].unique())
    selecoes[coluna] = st.sidebar.multiselect(
        label,
        opcoes_disponiveis,
        default=[],
        placeholder=f"Escolha uma ou mais opções"
    )

# --- Filtragem Dinâmica do DataFrame ---
df_filtrado = df.copy()

for coluna, valores_selecionados in selecoes.items():
    if valores_selecionados:
        df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores_selecionados)]

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados. Utilize os filtros à esquerda para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.markdown("### Métricas Gerais (Salário Anual em BRL)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['brl'].mean()
    salario_maximo = df_filtrado['brl'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo_br"].mode()[0] if not df_filtrado["cargo_br"].empty else "N/A"
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"R${salario_medio:,.0f}")
col2.metric("Salário Máximo", f"R${salario_maximo:,.0f}")
col3.metric("Total de Registros", f"{total_registros:,}")
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.markdown("### Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo_br')['brl'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos, x='brl', y='cargo_br', orientation='h',
            title="Top 10 Cargos por Salário Médio",
            labels={'brl': 'Média Salarial Anual (BRL)', 'cargo_br': ''},
            color_discrete_sequence=["#3346f6"]
        )
        grafico_cargos.update_layout(
            title_x=0.1, yaxis={'categoryorder':'total ascending'},
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color="#fafafa"
        )
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado, x='brl', nbins=30,
            title="Distribuição de Salários Anuais",
            labels={'brl': 'Faixa Salarial (BRL)', 'count': 'Quantidade'},
            color_discrete_sequence=["#3346f6"]
        )
        grafico_hist.update_layout(
            title_x=0.1, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color="#fafafa"
        )
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty and 'remoto' in df_filtrado.columns:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem, names='tipo_trabalho', values='quantidade',
            title='Proporção dos Tipos de Trabalho', hole=0.5,
            color_discrete_sequence=["#007bff", "#28a745", "#fd7e14"]
        )
        grafico_remoto.update_traces(textinfo='percent+label', pull=[0.05, 0.05, 0.05])
        grafico_remoto.update_layout(
            title_x=0.1, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color="#fafafa", legend_title_text=''
        )
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo_br'] == 'Cientista de Dados']
        media_ds_pais = df_ds.groupby('residencia_iso3')['brl'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='brl',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país (em BRL)',
            labels={'brl': 'Salário médio (BRL)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no mapa de salários por país.")

st.markdown("---")

# --- Tabela de Dados Detalhados ---
st.markdown("### Dados Detalhados (em USD)")
st.dataframe(df_filtrado.drop(columns=['brl', 'cargo_br']))


# --- Rodapé ---
st.markdown("""
    <div class="footer">
        <p>© Copyright | Desenvolvido por Henrique Gabriel </p>
    </div>
""", unsafe_allow_html=True)