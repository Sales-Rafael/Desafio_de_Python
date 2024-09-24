import streamlit as st
import pandas as pd
import plotly.express as px

#######################
# Configurações gerais da página
st.set_page_config(
    page_title="Gasolina",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded")

#######################
# Estilização CSS 
with open('style.css', 'r') as fp:
    st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)

#######################
# Carregamento de dados com Pandas

# Lê o arquivo CSV com os preços do combustível e armazena os dados no DataFrame df_fuel_price
# CSV do primeiro e segundo gráfico da segunda linha
df_fuel_price = pd.read_csv('./archive/PET_PRI_GND_DCUS_NUS_W.csv')

# Lê o arquivo CSV de consumo de combustível e armazena os dados no DataFrame df_fuel_consum
# CSV do Segundo grafico da Terceira linha
df_fuel_consum = pd.read_csv('./archive/Fuel_Consumption_Ratings.csv')
# Seleciona colunas específicas do CSV original, agrupa por 'Fabricante' e calcula a média de 'Emissão de CO2(g/km)', retornando um novo DataFrame.
Tabela_carros = df_fuel_consum.iloc[:, [2,8,9,7,12,1,4,5,6,]]
Tabela_carros_agrupado = Tabela_carros.groupby(['Fabricante'])[['Emissão de CO2(g/km)']].mean().reset_index()

# Lê o arquivo CSV de transações de cartão de crédito, agrupa os dados por 'Tipo de Cartão' e 'Tipo de Despesa', soma as quantias de cada grupo e redefine o índice.
# CSV do Primeiro grafico da Terceira Linha
df_credit_card = pd.read_csv('./archive/Credit_card_transactions.csv')
df_credit_card_agrupado = df_credit_card.groupby(['Tipo de Cartão', 'Tipo de Despesa'])[['Quantia']].sum().reset_index()

# Lê os dados, converte colunas de datas, filtra produtos indesejados, e arredonda os preços médios de revenda para duas casas decimais.
# CSV do primeiro grafico da primeira linha
df_brasil = pd.read_csv('./archive/precos_combustiveis.csv')
df_brasil['DATA INICIAL'], df_brasil['DATA FINAL'] = pd.to_datetime(df_brasil['DATA INICIAL']),pd.to_datetime(df_brasil['DATA FINAL'])
itens_indesejados = ['GLP', 'GNV','ETANOL HIDRATADO']
df_brasil_filtrado = df_brasil[~df_brasil['PRODUTO'].isin(itens_indesejados)]
df_brasil_filtrado['PREÇO MÉDIO REVENDA'] = df_brasil_filtrado['PREÇO MÉDIO REVENDA'].round(2)

# Carrega o CSV de combustíveis do Brasil, converte a coluna 'DATA INICIAL' para datetime, extrai o ano, calcula a média anual do preço de revenda por região e estado (arredondada para duas casas decimais), e renomeia a coluna resultante para 'Média do Preço'.
# CSV do Segundo grafico da Primeira linha
df_brazilbug = pd.read_csv('./archive/brazil_fuel.csv')
df_brazilbug['DATA INICIAL'] = pd.to_datetime(df_brazilbug['DATA INICIAL'])
df_brazilbug['Ano'] = df_brazilbug['DATA INICIAL'].dt.year
df_avg_price_per_year_region = df_brazilbug.groupby(['Ano', 'REGIÃO', 'ESTADO'])['PREÇO MÉDIO REVENDA'].mean().round(2).reset_index()
df_avg_price_per_year_region = df_avg_price_per_year_region.rename(columns={'PREÇO MÉDIO REVENDA': 'Média do Preço'})

#######################
# Sidebar (barra lateral)


with st.sidebar:
    # Verfifica qual opção de tema escolhido pelo usuário e muda o css e as cores dos gráficos de acordo com a escolhida
    options = ['Vermelho', 'Verde', 'Azul', 'Laranja', 
    'Roxo', 'Turquesa']
    Cor = st.selectbox("Escolha o Tema", options, index=0)
    # Muda as cores dos graficos e de uma parte da fonte de acordo com a cor escolhida no selectbox
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
    selected_card = st.selectbox("Tipo de Cartão de Crédito", df_credit_card_agrupado["Tipo de Cartão"].unique(),index=0)
    df_card_filtered = df_credit_card_agrupado[df_credit_card_agrupado["Tipo de Cartão"] == selected_card]

    # Sobre mim
    # Cria a variavel html e adiciona nela um codigo html com ids para poder ser feita uma estilização em css
    # Tentei fazer com as classes prontas mas houve um problema que as classes mudavam de um computador para outro. Usei essa solução alternativa por isso.
    html = """
    <div class="centered">
        <p>Email: <a href='https://mail.google.com/mail/u/0/?fs=1&tf=cm&source=mailto&to=rafael.sales@pditabira.com' id='link'>rafael.sales@pditabira.com</a></p>
        <p>Rafael Lucas do Nascimento Sales</p>
        <p>PDita157</p>
    </div>"""
    st.write(html, unsafe_allow_html=True)

    # coloca os botões de redes sociais em colunas
    col_1_side,col_2_side,col_3_side = st.columns((3), gap='small')
    col_1_side.link_button('Instagram', 'https://www.instagram.com/rafaellnascimento._/')
    col_2_side.link_button('LinkedIn', 'https://www.linkedin.com/in/rafael-lucas-a0548b24a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app')
    col_3_side.link_button('GitHub', 'https://github.com/Sales-Rafael')

#######################
# Apresentando plots no painel principal do dashboard 

# criando colunas e suas larguras
col_1 = st.columns((5,5), gap='medium')
col_2 = st.columns((4.5, 3), gap='medium')
col_3 = st.columns((1,1), gap='medium')

with col_1[0]:
    # Cria um gráfico de linha do histórico de preços de revenda de combustíveis no Brasil e exibe usando Streamlit
    fig_line_hist_comb = px.line(df_brasil_filtrado, x="DATA INICIAL", y="PREÇO MÉDIO REVENDA", color="PRODUTO", title='Historico do preço do Combustivel no Brasil',color_discrete_sequence=rainbow[1::])
    st.plotly_chart(fig_line_hist_comb) 


with col_1[1]:
    # Cria um gráfico de linha do histórico de preços do etanol hidratado no Brasil por estado e o exibe
    fig_line_hist_etanol = px.line(df_filtered, x="Ano", y="Média do Preço", color="ESTADO", title='Histórico do preço do Etanol Hidratado no Brasil',color_discrete_sequence=rainbow)
    st.plotly_chart(fig_line_hist_etanol)

with col_2[0]:
    # cria uma nova coluna que converte a quantidade de galão para litros, depois de dolares para reais e depois arredonda.
    df_fuel_price['Preço do galão de gasolina em reais'] = (df_fuel_price['R2']* 5.16).round(2)
    # converte a data de "dtype: object" para "datetime64[ns]"
    df_fuel_price['Data'] = pd.to_datetime(df_fuel_price['Date'])
    fig_line_EUA = px.line(df_fuel_price, x="Data", y="Preço do galão de gasolina em reais", title='Histórico de Preço da Gasolina nos EUA',color_discrete_sequence=rainbow[3::])
    st.plotly_chart(fig_line_EUA) 

with col_2[1]:
    # Primeiro, é extraído o ano da coluna de dados para, em seguida, calcular a média e arredondar para duas casas decimais.
    # A coluna é renomeada e os valores são ordenados para, depois, ser feito o gráfico, que é exibido após isso.
    df_fuel_price['Ano'] = df_fuel_price['Data'].dt.year
    df_avg_price_per_year = df_fuel_price.groupby('Ano')['Preço do galão de gasolina em reais'].mean().round(2).reset_index()
    df_avg_price_per_year = df_avg_price_per_year.rename(columns={'Preço do galão de gasolina em reais': 'Média do Preço'})
    df_avg_price_per_year = df_avg_price_per_year.sort_values(by='Média do Preço', ascending=False)
    fig_bar_EUA = px.bar(df_avg_price_per_year, x='Ano', y='Média do Preço', orientation='v', title='Média do Preço do Galão de Gasolina no EUA por Ano',color='Média do Preço',color_continuous_scale=rainbow[::-1])
    st.plotly_chart(fig_bar_EUA)

with col_3[0]:
    # Cria e exibe um gráfico de pizza interativo dos gastos por tipo de cartão de crédito, destacando a categoria "Combustível".
    fig_pie_credit_card= px.pie(df_card_filtered, values='Quantia', names='Tipo de Despesa', title ="Gasto por tipo de cartão de credito",color_discrete_sequence=rainbow)
    fig_pie_credit_card.update_traces(
        pull=[0.2 if exp_type == 'Combustível' else 0 for exp_type in df_credit_card_agrupado['Tipo de Despesa']]
    )
    fig_pie_credit_card.update_traces(textposition='inside')
    st.plotly_chart(fig_pie_credit_card) 

with col_3[1]:
    # Cria um gráfico de pizza da emissão de CO2 por fabricante de carro, com porcentagens exibidas dentro das fatias, e o plota usando Streamlit
    fig_pie_CO2 = px.pie(Tabela_carros_agrupado, values='Emissão de CO2(g/km)', names='Fabricante', title ="Emissão de CO2 por fabricante de carro",color_discrete_sequence=rainbow)
    fig_pie_CO2.update_traces(textposition='inside', textinfo='percent')
    st.plotly_chart(fig_pie_CO2) 

