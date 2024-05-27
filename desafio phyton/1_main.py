import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import webbrowser
import json

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
    
# df_pib_pc = pd.read_csv('./archive/gdp_per_capita.csv')
df_co2 = pd.read_csv('./archive/co2_emissions_kt_by_country.csv')
df_fertility = pd.read_csv('./archive/total_fertility_rate_time_series.csv')
df_population = pd.read_csv('./archive/World-population-by-countries-dataset.csv')

#######################
# Sidebar (barra lateral)
# inclua elementos de interatividade
# fornecidos pelo Streamlit e/ou
# informações sobre os dados
with st.sidebar:
    st.divider()
    st.title('📊 Meu dashboard')
    st.write('Rafael Lucas do Nascimento Sales')
    st.write('PDita157')
    btn = st.button('LinkedIn')
    if btn:
        webbrowser.open_new_tab('https://www.linkedin.com/in/rafael-lucas-a0548b24a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app')
    btn1 = st.button('Instagram')
    if btn:
        webbrowser.open_new_tab('https://www.instagram.com/rafaellnascimento._/')
    btn2 = st.button('GitHub')
    if btn:
        webbrowser.open_new_tab('https://github.com/Faellinho')


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
col = st.columns((3, 4.5), gap='medium')

# preencha as colunas incorporando seus
# dados e plots como elementos Streamlit

# plot 1
counties = json.load("./custom.geo.json")
df = pd.read_csv("./archive/gdp_per_capita.csv",
                   dtype={"Country Name"})
fig = px.choropleth(df, geojson=counties, locations='Country Name', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
