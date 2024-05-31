import streamlit as st
import pandas as pd
import plotly.express as px

#######################
# Configurações gerais da página
st.set_page_config(
    page_title="Meu dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

#######################
# Estilização CSS 
# Crie o seu arquivo .css
with open('style.css', 'r') as fp:
    st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)

#######################
# Carregamento de dados com Pandas

df_fuel_price = pd.read_csv('./archive/PET_PRI_GND_DCUS_NUS_W.csv')
df_fuel_consum = pd.read_csv('./archive/Fuel_Consumption_Ratings.csv')
df_credit_card = pd.read_csv('./archive/Credit_card_transactions.csv')
df_brasil = pd.read_csv('./archive/precos_combustiveis.csv')
df_brasil['DATA INICIAL'], df_brasil['DATA FINAL'] = pd.to_datetime(df_brasil['DATA INICIAL']),pd.to_datetime(df_brasil['DATA FINAL'])
Tabela_carros = df_fuel_consum.iloc[:, [2,8,9,7,12,1,4,5,6,]]
# Carregar o arquivo CSV
df_brazilbug = pd.read_csv('./archive/brazil_fuel.csv')

# Converter a coluna 'DATA INICIAL' para datetime
df_brazilbug['DATA INICIAL'] = pd.to_datetime(df_brazilbug['DATA INICIAL'])

# Extrair o ano da coluna 'DATA INICIAL'
df_brazilbug['Ano'] = df_brazilbug['DATA INICIAL'].dt.year

# Calcular a média dos preços por ano, por região e por estado, e arredondar para 2 casas decimais
df_avg_price_per_year_region = df_brazilbug.groupby(['Ano', 'REGIÃO', 'ESTADO'])['PREÇO MÉDIO REVENDA'].mean().round(2).reset_index()

# Renomear a coluna para algo mais amigável
df_avg_price_per_year_region = df_avg_price_per_year_region.rename(columns={'PREÇO MÉDIO REVENDA': 'Média do Preço'})


#######################
# Sidebar (barra lateral)
# inclua elementos de interatividade
# fornecidos pelo Streamlit e/ou
# informações sobre os dados
with st.sidebar:
    options = ["blue","green","seaborn"]
    Cor = st.selectbox("Escolha a cor tema", options, index=0)
    selected_region = st.selectbox("Região", df_avg_price_per_year_region["REGIÃO"].unique(),index=3)
    df_filtered = df_avg_price_per_year_region[df_avg_price_per_year_region["REGIÃO"] == selected_region]
    unique_states = df_filtered["ESTADO"].unique()
    selected_states = st.multiselect('Estado', unique_states, default=unique_states[:2])
    df_filtered = df_filtered[df_filtered["ESTADO"].isin(selected_states)]
    st.divider()
    st.title('📊 Sobre Mim')
    st.write('Email: rafael.sales@pditabira.com')
    st.write('Rafael Lucas do Nascimento Sales')
    st.write('PDita157')
    coll1,coll2,coll3 = st.columns((3), gap='small')
    coll1.link_button('Instagram', 'https://www.instagram.com/rafaellnascimento._/')
    coll2.link_button('LinkedIn', 'https://www.linkedin.com/in/rafael-lucas-a0548b24a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app')
    coll3.link_button('GitHub', 'https://github.com/Faellinho')
    
#######################
# Criando Plots
# crie uma função para cada gráfico
# a função deve retornar o objeto do gráfico.
# Use e abuse do Plotly!

# def plot1(input1, input2, input3):
#     return 

# def plot2(input1, input2, input3):
#     return 

# def plot3(input1, input2, input3):
#     return


#######################
# Apresentando plots no painel 
# principal do dashboard 

# criando colunas e suas larguras
col0 = st.columns((5,5), gap='medium')
col1 = st.columns((4.5, 3), gap='medium')

# preencha as colunas incorporando seus
# dados e plots como elementos Streamlit
with col0[0]:
    fig = px.line(df_brasil, x="DATA INICIAL", y="PREÇO MÉDIO REVENDA", color="PRODUTO", title='Historico do preço do Combustivel no Brasil')
    st.plotly_chart(fig) 
with col0[1]:
        # Criar o gráfico de linha
        fig = px.line(df_filtered, x="Ano", y="Média do Preço", color="ESTADO", title='Histórico do preço do Etanol Hidratado no Brasil')
        # Mostrar o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)

with col1[0]:
    # cria uma nova coluna que converte a quantidade de galão para litros, depois de dolares para reais e depois arredonda.
    df_fuel_price['Preço do galão de gasolina em reais'] = (df_fuel_price['R2']* 5.16).round(2)
    # converte a data de "dtype: object" para "datetime64[ns]"
    df_fuel_price['Data'] = pd.to_datetime(df_fuel_price['Date'])
    fig = px.line(df_fuel_price, x="Data", y="Preço do galão de gasolina em reais", title='Histórico de Preço da Gasolina nos EUA')
    st.plotly_chart(fig) 

with col1[1]:
    # Extrair o ano da coluna 'Data'
    df_fuel_price['Ano'] = df_fuel_price['Data'].dt.year

    # Calcular a média dos preços por ano e arredondar para 2 casas decimais
    df_avg_price_per_year = df_fuel_price.groupby('Ano')['Preço do galão de gasolina em reais'].mean().round(2).reset_index()

    # Renomear a coluna para algo mais amigável
    df_avg_price_per_year = df_avg_price_per_year.rename(columns={'Preço do galão de gasolina em reais': 'Média do Preço'})

    # Ordenar os resultados pelo preço médio do maior para o menor
    df_avg_price_per_year = df_avg_price_per_year.sort_values(by='Média do Preço', ascending=False)

    # Criar o gráfico de barras horizontal
    fig1 = px.bar(df_avg_price_per_year, x='Média do Preço', y='Ano', orientation='h', title='Média do Preço do Galão de Gasolina por Ano')

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig1)


st.dataframe(Tabela_carros)
