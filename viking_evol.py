#######################
# Importando libraries
import streamlit as st
import altair as alt
import json
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards


#######################
# Configuração da página
st.set_page_config(
    page_title="Evolua como um Viking",
    page_icon=":muscle:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

alt.themes.enable("dark")

#######################
# Projeto utilizando streamlit_extras.metric_cards
# pip install streamlit-extras
# streamlit-extras==0.3.5
# https://arnaudmiribel.github.io/streamlit-extras/extras/metric_cards/


#######################
# Carregando dataset


df_inbody_full = pd.read_excel(
    "https://raw.githubusercontent.com/gabrielmprata/viking_evol/main/dataset/evol_python.xlsx", sheet_name='inbody_full')

df_inbody_full['data'] = pd.to_datetime(df_inbody_full['data'])
df_inbody_full['ano_mes'] = df_inbody_full['data'].dt.strftime('%Y-%m')

df_adp = pd.read_excel(
    "https://raw.githubusercontent.com/gabrielmprata/viking_evol/main/dataset/evol_python.xlsx", sheet_name='adp')
df_adp['data'] = pd.to_datetime(df_adp['data'])
df_adp['ano_mes'] = df_adp['data'].dt.strftime('%Y-%m')

df_bio_medidas = pd.read_excel(
    "https://raw.githubusercontent.com/gabrielmprata/viking_evol/main/dataset/evol_python.xlsx", sheet_name='medidas')
df_bio_medidas['data'] = pd.to_datetime(df_bio_medidas['data'])
df_bio_medidas['ano_mes'] = df_bio_medidas['data'].dt.strftime('%Y-%m')

# Param
maxi = '2025-01'
mes_ant = '2024-12'

maxia = '2025-02'
maxia_ant = '2025-01'

mes_adp = '2025-02'
mes_adp_ant = '2025-01'

# Construção dos Datasets
# 1. Avaliação InBody ATUAL
# Peso

peso = (df_inbody_full[['Valor']]
        [(df_inbody_full['ano_mes'] == maxi) & (df_inbody_full['kpi'] == 5)]
        ).reset_index()

peso_ant = (df_inbody_full[['Valor']]
            [(df_inbody_full['ano_mes'] == mes_ant) & (df_inbody_full['kpi'] == 5)]
            ).reset_index()

var_peso = (peso.Valor.values[0] - peso_ant.Valor.values[0]).round(2)

# Massa de gordura  InBody ATUAL
gordura = (df_inbody_full[['Valor']]
           [(df_inbody_full['ano_mes'] == maxi) & (df_inbody_full['kpi'] == 4)]
           ).reset_index()

gordura_ant = (df_inbody_full[['Valor']]
               [(df_inbody_full['ano_mes'] == mes_ant)
                & (df_inbody_full['kpi'] == 4)]
               ).reset_index()

var_gordura = (gordura.Valor.values[0] - gordura_ant.Valor.values[0]).round(2)

# Massa Muscular Esquelética  InBody ATUAL
massa = (df_inbody_full[['Valor']]
         [(df_inbody_full['ano_mes'] == maxi) & (df_inbody_full['kpi'] == 6)]
         ).reset_index()

massa_ant = (df_inbody_full[['Valor']]
             [(df_inbody_full['ano_mes'] == mes_ant)
              & (df_inbody_full['kpi'] == 6)]
             ).reset_index()

var_massa = (massa.Valor.values[0] - massa_ant.Valor.values[0]).round(2)

# Porcentual de gordura  InBody ATUAL
pgc = (df_inbody_full[['Valor']]
       [(df_inbody_full['ano_mes'] == maxi) & (df_inbody_full['kpi'] == 8)]
       ).reset_index()

pgc_ant = (df_inbody_full[['Valor']]
           [(df_inbody_full['ano_mes'] == mes_ant) & (df_inbody_full['kpi'] == 8)]
           ).reset_index()

var_pgc = (pgc.Valor.values[0] - pgc_ant.Valor.values[0]).round(2)

# ----------------------------------------------------------------------------#
# 2. Análise músculo gordura InBody Historico
df_inbody_full_gr = (df_inbody_full[['ano_mes', 'Metrica', 'kpi', 'Valor']]).query(
    'kpi in (4, 5, 6) ')

# ----------------------------------------------------------------------------#
# 3. Porcentual de gordura  InBody Historico
df_inbody_pgc = (
    df_inbody_full[['ano_mes', 'Metrica', 'kpi', 'Valor']]).query('kpi == 8')

# ----------------------------------------------------------------------------#
# ****************************************************************************#

# 4. Adpometro
# Composição atual Grafico pizza
df_atp_aval = (df_adp[['data', 'ano_mes', 'indicador', 'medida']]
               [(df_adp['ano_mes'] == mes_adp) & ((df_adp['indicador'] == 'peso gordura') |
                                                  (df_adp['indicador'] == 'peso magro'))]
               )

# Historico

# Histórico Adipômetro da composição corporal (%)
# grafico de barras
df_atp_his = (df_adp[['data', 'ano_mes', 'indicador', 'medida']]
              [((df_adp['indicador'] == 'não gordura')
                | (df_adp['indicador'] == 'gordura'))]
              )

# Histórico Adipômetro da composição corporal (Kg)
# grafico de barras
df_atp_his_kg = (df_adp[['data', 'ano_mes', 'indicador', 'medida']]
                 [((df_adp['indicador'] == 'peso gordura')
                   | (df_adp['indicador'] == 'peso magro'))]
                 )

# 4. Adpometro metrics atual vs anterior
df_atp_res = (df_adp[['data', 'ano_mes', 'indicador', 'medida']]
              [((df_adp['ano_mes'] == mes_adp) | (df_adp['ano_mes'] == mes_adp_ant)) & ((df_adp['indicador'] == 'peso gordura') |
                                                                                        (df_adp['indicador'] == 'peso magro') | (df_adp['indicador'] == 'peso') |
                                                                                        (df_adp['indicador'] == 'não gordura') | (df_adp['indicador'] == 'gordura'))]
              )

# SUM(CASE WHEN)
df_atp_res_col = df_atp_res.groupby(['indicador'], as_index=False).apply(lambda x: pd.Series({'mes_adp_ant': x.loc[x.ano_mes == mes_adp_ant]['medida'].sum(),
                                                                                              'mes_adp': x.loc[x.ano_mes == mes_adp]['medida'].sum()
                                                                                              }
                                                                                             ))

df_atp_res_col["dif"] = df_atp_res_col['mes_adp'] - \
    df_atp_res_col['mes_adp_ant']

# variaveis para o st.metric
# Gordura
adp_fat = (df_atp_res_col.mes_adp.values[0]).round(2)
adp_fat_dif = (df_atp_res_col.dif.values[0]).round(2)

# não gordura
adp_mass = (df_atp_res_col.mes_adp.values[1]).round(2)
adp_mass_dif = (df_atp_res_col.dif.values[1]).round(2)

# peso
adp_peso = (df_atp_res_col.mes_adp.values[2]).round(2)
adp_peso_dif = (df_atp_res_col.dif.values[2]).round(2)

# peso gordura
adp_peso_fat = (df_atp_res_col.mes_adp.values[3]).round(2)
adp_peso_fat_dif = (df_atp_res_col.dif.values[3]).round(2)

# peso magro
adp_peso_mass = (df_atp_res_col.mes_adp.values[4]).round(2)
adp_peso_mass_dif = (df_atp_res_col.dif.values[4]).round(2)


# 4.5 Histórico Dobras Cutâneas
df_atp_med = (df_adp[['ano_mes', 'indicador', 'medida']]
              [((df_adp['grupo'] == 'dados'))]
              )

# SUM(CASE WHEN)
df_atp_med_col = df_atp_med.groupby(['indicador'], as_index=False).apply(lambda x: pd.Series({'2024-12': x.loc[x.ano_mes == '2024-12']['medida'].sum(),
                                                                                              '2025-01': x.loc[x.ano_mes == '2025-01']['medida'].sum(),
                                                                                              '2025-02': x.loc[x.ano_mes == '2025-02']['medida'].sum()
                                                                                              }
                                                                                             ))

# Calculando a variação com o ano anterior
# df_atp_med_col['var_202312_202403'] = (df_atp_med_col['2023-12']-df_atp_med_col['2024-03'])
# df_atp_med_col['var_202403_202406'] = (df_atp_med_col['2024-03']-df_atp_med_col['2024-06'])
# df_atp_med_col['var_202406_202410'] = (df_atp_med_col['2024-06']-df_atp_med_col['2024-10'])
# df_atp_med_col['var_202410_202411'] = (df_atp_med_col['2024-10']-df_atp_med_col['2024-11'])
# df_atp_med_col['var_202411_202412'] = (df_atp_med_col['2024-11']-df_atp_med_col['2024-12'])

# Criando campo historico
df_atp_med_col["historico"] = "[" + df_atp_med_col[('2024-12')].apply(str) + ", " + df_atp_med_col[(
    '2025-01')].apply(str) + ", " + df_atp_med_col[('2025-02')].apply(str) + "]"


# 4.6 Histórico Medidas

df_bio_medidas_col = df_bio_medidas.groupby(['antropometria'], as_index=False).apply(lambda x: pd.Series({'2024-12': x.loc[x.ano_mes == '2024-12']['medida'].sum(),
                                                                                                          '2025-01': x.loc[x.ano_mes == '2025-01']['medida'].sum(),
                                                                                                          '2025-02': x.loc[x.ano_mes == '2025-02']['medida'].sum()
                                                                                                          }
                                                                                                         ))

# Criando campo historico
df_bio_medidas_col["historico"] = "[" + df_bio_medidas_col[('2024-12')].apply(
    str) + ", " + df_bio_medidas_col[('2025-01')].apply(str) + ", " + df_bio_medidas_col[('2025-02')].apply(str) + "]"


#######################
# Construção dos Gráficos

# 1. Avaliação InBody ATUAL
# todos os cards foram feitos com st.metric direto no Main Panel

# ----------------------------------------------------------------------------#
# 2. Análise músculo gordura  InBody Historico
hist = px.line(df_inbody_full_gr, x='ano_mes', y='Valor', color='Metrica',
               markers=True, text='Valor',
               # height=600, width=800, #altura x largura
               line_shape="spline",
               template="plotly_dark",
               render_mode="svg",
               color_discrete_sequence=["blue", "green", "red"],
               category_orders={"Metrica": [
                   "Peso", "Massa Muscular Esquelética", "Massa de gordura"]},
               labels=dict(ano_mes="Ano e mês",
                           Valor="Kg", variable="Métrica")
               )

hist.update_layout(legend=dict(
    yanchor="top",
    y=-0.3,
    xanchor="left",
    x=0.01))
# se o type for date, vai respeitar o intervalo
hist.update_xaxes(type="category", title=None)
hist.update_traces(line_width=2, textposition='top center')

# -------------------------------------------------------#
# 3 Porcentual de Gordura   InBody Historico
gr_pcg = px.line(df_inbody_pgc, x='ano_mes', y='Valor', color='Metrica',
                 markers=True, text='Valor',
                 height=150, width=800,  # altura x largura
                 line_shape="spline",
                 template="plotly_dark",
                 render_mode="svg",
                 color_discrete_sequence=["orange"],

                 labels=dict(ano_mes="Ano e mês",
                             Valor="%", variable="Métrica")
                 )
# se o type for date, vai respeitar o intervalo
gr_pcg.update_xaxes(type="category", title=None)
gr_pcg.update_layout(margin=dict(t=1, b=0, l=0, r=0), showlegend=False)
gr_pcg.update_traces(line_width=2, textposition='top center')

# ----------------------------------------------------------------------------#
# 4. Adpometro
# Composição atual
gr_adp_comp = px.pie(df_atp_aval, names='indicador', values='medida',
                     labels=dict(variable="indicador", value="medida"),
                     height=250, width=300, hole=0.5,
                     template="plotly_dark",
                     color_discrete_map={'peso magro': 'lightcyan',
                                         'peso gordura': 'orange'}
                     )
gr_adp_comp.update_traces(textposition='outside',
                          textinfo='percent+value+label', rotation=50)
gr_adp_comp.update_layout(margin=dict(t=0, b=35, l=0, r=0), showlegend=False)
gr_adp_comp.add_annotation(dict(x=0.5, y=0.5,  align='center',
                                xref="paper", yref="paper",
                                showarrow=False, font_size=22,
                                text="Faulkner"))


# Histórico
# Histórico Adipômetro da composição corporal (%)

gr_adp = px.bar(df_atp_his, x="ano_mes", y="medida", color="indicador",
                labels=dict(medida="Medida(%)", ano_mes="Ano/Mês",
                            indicador="Indicador"),
                color_discrete_sequence=["orange", "#1f66bd"],
                template="plotly_dark",  text="medida",
                title="Em %"
                )
# se o type for date, vai respeitar o intervalo
gr_adp.update_xaxes(type="category", title=None)

# Histórico Adipômetro da composição corporal (Kg)
gr_adp_kg = px.bar(df_atp_his_kg, x="ano_mes", y="medida", color="indicador",
                   labels=dict(medida="Medida(Kg)", ano_mes="Ano/Mês",
                               indicador="Indicador"),
                   color_discrete_sequence=["orange", "#1f66bd"],
                   template="plotly_dark",  text="medida",
                   title="Em Kg"
                   )
# se o type for date, vai respeitar o intervalo
gr_adp_kg.update_xaxes(type="category", title=None)


# 4. Adpometro Historico de todas as metricas criado com st.dataframe

#######################
# Dashboard Main Panel

st.image("https://raw.githubusercontent.com/gabrielmprata/viking_evol/main/img/Header_Viking3.jpg")
st.markdown("# :crossed_swords: **Viking Evolution** :hammer_and_pick:")

st.write(":blue[Avaliação:]", maxi, "	:date:")
st.markdown("## :orange[Inbody Bioimpedância]")

style_metric_cards(background_color="#071021",
                   border_left_color="#1f66bd", border_radius_px=5)

with st.expander("Analise Músculo-Gordura", expanded=True):

    col = st.columns((1.1, 1.1, 1.1, 1.1), gap='medium')

    with col[0]:
        #######################
        # Quadro com o total e a variação
        st.markdown('### Peso')
        st.metric(label="", value=str(
            (peso.Valor.values[0]).round(2)), delta=str(var_peso))

    with col[1]:
        st.markdown('### Massa Magra')
        st.metric(label="", value=str(
            (massa.Valor.values[0]).round(2)), delta=str(var_massa))

    with col[2]:
        st.markdown('### Massa Gorda')
        st.metric(delta_color="inverse", label="", value=str(
            (gordura.Valor.values[0]).round(2)), delta=str(var_gordura))

    with col[3]:
        st.markdown('### % Gordura')
        st.metric(delta_color="inverse", label="", value=str(
            (pgc.Valor.values[0]).round(2)), delta=str(var_pgc))

with st.expander("Histórico Músculo-Gordura", expanded=True):
    st.plotly_chart(hist, use_container_width=True)

with st.expander("Histórico do Porcentual de Gordura", expanded=True):
    st.plotly_chart(gr_pcg, use_container_width=True)

################################################################################
## ****************************************************************************##

st.markdown("## :orange[Adipômetro - Método Faulkner]")

with st.expander("Avaliação Atual", expanded=True):

    col = st.columns((1.1, 1.1, 1.1, 1.1), gap='medium')

    with col[0]:
        #######################
        # Quadro com o total e a variação
        st.markdown('### Peso')
        st.metric(label="", value=str(adp_peso), delta=str(adp_peso_dif))

    with col[1]:
        st.markdown('### Massa Magra')
        st.metric(label="", value=str(adp_peso_mass),
                  delta=str(adp_peso_mass_dif))

    with col[2]:
        st.markdown('### Massa Gorda')
        st.metric(delta_color="inverse", label="", value=str(
            adp_peso_fat), delta=str(adp_peso_fat_dif))

    with col[3]:
        st.markdown('### % Gordura')
        st.metric(delta_color="inverse", label="",
                  value=str(adp_fat), delta=str(adp_fat_dif))

    st.markdown(" ")
    st.markdown(" ")

    col = st.columns((4.1, 4.1), gap='medium')

    with col[0]:
        st.dataframe(
            df_atp_res_col,
            column_order=(
                "indicador", "mes_adp_ant", "mes_adp", "dif"),
            column_config={
                "indicador": "Indicador",
                "mes_adp_ant": "Anterior",
                "mes_adp": "Atual",
                "dif": "Dif",
            },
            hide_index=True,
        )

    with col[1]:
        st.plotly_chart(gr_adp_comp, use_container_width=True)


###################################################################################
with st.expander("Histórico Composição Corporal", expanded=True):
    col = st.columns((4.1, 4.1), gap='medium')

    with col[0]:
        st.plotly_chart(gr_adp, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_adp_kg, use_container_width=True)

with st.expander("Histórico Dobras Cutâneas", expanded=True):

    st.dataframe(
        df_atp_med_col,
        column_order=(
            "indicador", "2024-12", "2025-01", "2025-02",   "historico"),
        column_config={
            "indicador": "Indicador",
            "2024-12": "2024-12",
            "2025-01": "2025-01",
            "2025-01": "2025-02",
            "historico": st.column_config.LineChartColumn(
                "Histórico "
            ),
        },
        hide_index=True,
    )

with st.expander("Histórico Medidas Corporais", expanded=True):

    st.dataframe(
        df_bio_medidas_col,
        column_order=(
            "antropometria", "2024-12", "2025-01", "2025-02", "historico"),
        column_config={
            "antropometria": "Antropometria",
            "2024-12": "2024-12",
            "2025-01": "2025-01",
            "2025-02": "2025-02",
            "historico": st.column_config.LineChartColumn(
                "Histórico "
            ),
        },
        hide_index=True,
    )
