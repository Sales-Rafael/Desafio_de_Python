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
# Adiciona a logo do Projeto Desenvolve no canto do dashboard
st.logo('./Projeto_Desenvolve.png')

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
df_credit_card_agrupado = df_credit_card.groupby(['Tipo de Cartão', 'Tipo de Despesa'])[['Quantia']].sum().reset_index()

df_brasil = pd.read_csv('./archive/precos_combustiveis.csv')
df_brasil['DATA INICIAL'], df_brasil['DATA FINAL'] = pd.to_datetime(df_brasil['DATA INICIAL']),pd.to_datetime(df_brasil['DATA FINAL'])

itens_indesejados = ['GLP', 'GNV','ETANOL HIDRATADO']

# Filtrar o DataFrame para remover linhas com os itens indesejados
df_brasil_filtrado = df_brasil[~df_brasil['PRODUTO'].isin(itens_indesejados)]
df_brasil_filtrado['PREÇO MÉDIO REVENDA'] = df_brasil_filtrado['PREÇO MÉDIO REVENDA'].round(2)

Tabela_carros = df_fuel_consum.iloc[:, [2,8,9,7,12,1,4,5,6,]]
Tabela_carros_agrupado = Tabela_carros.groupby(['Fabricante'])[['Emissão de CO2(g/km)']].mean().reset_index()

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


with st.sidebar:
    # Verfifica qual opção de tema escolhido pelo usuário e muda o css e as cores dos gráficos de acordo com a escolhida
    options = ['Vermelho', 'Verde', 'Azul', 'Laranja', 
    'Roxo', 'Turquesa']
    Cor = st.selectbox("Escolha a cor tema", options, index=0)
    if Cor == "Vermelho":
        rainbow = px.colors.sequential.Reds[::-1]
        with open('./temas/Vermelho.css', 'r') as fp:
            st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)
    elif Cor == "Verde":
        rainbow = px.colors.sequential.Greens[::-1]
        with open('./temas/Verde.css', 'r') as fp:
            st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)
    elif Cor == "Azul":
        rainbow = px.colors.sequential.Blues[::-1]
        with open('./temas/Azul.css', 'r') as fp:
            st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)
    elif Cor == "Laranja":
        rainbow = px.colors.sequential.Oranges[::-1]
        with open('./temas/Laranja.css', 'r') as fp:
            st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)
    elif Cor == "Roxo":
        rainbow = px.colors.sequential.Purples[::-1]
        with open('./temas/Roxo.css', 'r') as fp:
            st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)
    elif Cor == "Turquesa":
        rainbow = px.colors.sequential.Teal
        with open('./temas/Turquesa.css', 'r') as fp:
            st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)

    # Verfica a região escolhida pelo usuario e muda o gráfico de acordo com a opção
    selected_region = st.selectbox("Região", df_avg_price_per_year_region["REGIÃO"].unique(),index=3)
    df_filtered = df_avg_price_per_year_region[df_avg_price_per_year_region["REGIÃO"] == selected_region]
    unique_states = df_filtered["ESTADO"].unique()

    # Verfifica quais os estados escolhidos de acordo com a região esciolhida
    selected_states = st.multiselect('Estado', unique_states, default=unique_states[:2])
    df_filtered = df_filtered[df_filtered["ESTADO"].isin(selected_states)]

    # Verifica qual tipo de cartão de credito o usuário pretende que o gráfico mostre
    selected_card = st.selectbox("Tipo de Cartão", df_credit_card_agrupado["Tipo de Cartão"].unique(),index=0)
    df_card_filtered = df_credit_card_agrupado[df_credit_card_agrupado["Tipo de Cartão"] == selected_card]

    # Sobre mim
    st.write('Email: rafael.sales@pditabira.com')
    st.write('Rafael Lucas do Nascimento Sales')
    st.write('PDita157')
    col1,col2,col3 = st.columns((3), gap='small')
    col1.link_button('Instagram', 'https://www.instagram.com/rafaellnascimento._/')
    col2.link_button('LinkedIn', 'https://www.linkedin.com/in/rafael-lucas-a0548b24a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app')
    col3.link_button('GitHub', 'https://github.com/Faellinho')

#######################
# Apresentando plots no painel 
# principal do dashboard 

# criando colunas e suas larguras
col_1 = st.columns((5,5), gap='medium')
col_2 = st.columns((4.5, 3), gap='medium')
col_3 = st.columns((1,1), gap='medium')

# preencha as colunas incorporando seus
# dados e plots como elementos Streamlit
with col_1[0]:
    fig = px.line(df_brasil_filtrado, x="DATA INICIAL", y="PREÇO MÉDIO REVENDA", color="PRODUTO", title='Historico do preço do Combustivel no Brasil',color_discrete_sequence=rainbow[1::])
    st.plotly_chart(fig) 
with col_1[1]:
        # Criar o gráfico de linha
        fig = px.line(df_filtered, x="Ano", y="Média do Preço", color="ESTADO", title='Histórico do preço do Etanol Hidratado no Brasil',color_discrete_sequence=rainbow)
        # Mostrar o gráfico no Streamlit
        st.plotly_chart(fig)

with col_2[0]:
    # cria uma nova coluna que converte a quantidade de galão para litros, depois de dolares para reais e depois arredonda.
    df_fuel_price['Preço do galão de gasolina em reais'] = (df_fuel_price['R2']* 5.16).round(2)
    # converte a data de "dtype: object" para "datetime64[ns]"
    df_fuel_price['Data'] = pd.to_datetime(df_fuel_price['Date'])
    fig = px.line(df_fuel_price, x="Data", y="Preço do galão de gasolina em reais", title='Histórico de Preço da Gasolina nos EUA',color_discrete_sequence=rainbow[3::])
    st.plotly_chart(fig) 

with col_2[1]:
    # Extrair o ano da coluna 'Data'
    df_fuel_price['Ano'] = df_fuel_price['Data'].dt.year

    # Calcular a média dos preços por ano e arredondar para 2 casas decimais
    df_avg_price_per_year = df_fuel_price.groupby('Ano')['Preço do galão de gasolina em reais'].mean().round(2).reset_index()

    # Renomear a coluna para algo mais amigável
    df_avg_price_per_year = df_avg_price_per_year.rename(columns={'Preço do galão de gasolina em reais': 'Média do Preço'})

    # Ordenar os resultados pelo preço médio do maior para o menor
    df_avg_price_per_year = df_avg_price_per_year.sort_values(by='Média do Preço', ascending=False)

    # Criar o gráfico de barras horizontal
    fig1 = px.bar(df_avg_price_per_year, x='Ano', y='Média do Preço', orientation='v', title='Média do Preço do Galão de Gasolina no EUA por Ano',color='Média do Preço',color_continuous_scale=rainbow[::-1])

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig1)

with col_3[0]:
    fig_pie = px.pie(df_card_filtered, values='Quantia', names='Tipo de Despesa', title ="Gasto por tipo de cartão de credito",color_discrete_sequence=rainbow)
    fig_pie.update_traces(
        pull=[0.2 if exp_type == 'Combustível' else 0 for exp_type in df_credit_card_agrupado['Tipo de Despesa']]
    )
    fig_pie.update_traces(textposition='inside')
    st.plotly_chart(fig_pie) 
# with col_3[1]:
#     fig = px.pie(df_credit_card_agrupado, values='Amount', names='Exp Type', title ="Gasto com cartão de credito(Todos)",color_discrete_sequence=rainbow[::-1])
#     fig.update_traces(
#         pull=[0.2 if exp_type == 'Fuel' else 0 for exp_type in df_credit_card_agrupado['Exp Type']]
#     )
#     st.plotly_chart(fig) 
with col_3[1]:
    fig_pie_2 = px.pie(Tabela_carros_agrupado, values='Emissão de CO2(g/km)', names='Fabricante', title ="Emissão de CO2 por fabricante de carro",color_discrete_sequence=rainbow)
    fig_pie_2.update_traces(textposition='inside', textinfo='percent')
    st.plotly_chart(fig_pie_2) 

