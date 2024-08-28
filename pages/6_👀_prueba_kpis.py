import os
from datetime import datetime
import csv

import streamlit as st
import pandas as pd 
import sqlite3
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

st.set_page_config(page_title="Prueba KPIs", page_icon="👀")

logo=("/home/pichu/Documentos/api-ga4/informes/images/logo.png")

st.html("""
  <style>
    [alt=Logo] {
      height: 6rem;
    }
  </style>
        """)
st.title("MasterClass sobre el uso de la API Analytics Data")
st.logo(
    logo,
    link="https://javilazaro.es",
)
st.sidebar.markdown("## Donde me podeis encontrar")

logo_arriaka=st.sidebar.markdown("[![Arriaka Marketing & Consulting](https://arriakamarketing.com/wp-content/uploads/logo-arriaka-marketing.png)](https://arriakamarketing.com)")

logo_arriaka=st.sidebar.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Logo.svg.original.svg)](https://www.linkedin.com/in/javi-lazaro/)")

logo_analaizer=st.sidebar.markdown("[![analaizer.digital](https://analaizer.digital/wp-content/uploads/2024/07/logo-.webp)](https://analaizer.digital/)")

logo_git=st.sidebar.markdown("[![github](https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png)](https://github.com/pichu2707)")   



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pichu/Documentos/api-ga4/informes/service_account.json'

property_id = "347166373"
client = BetaAnalyticsDataClient()

def get_ga_data(property_id, start_date, end_date):
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date"),  # Asegúrate de que esta dimensión se solicita correctamente
        ],
        metrics=[
            Metric(name="activeUsers"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    response = client.run_report(request)
    rows = []
    for row in response.rows:
        date = row.dimension_values[0].value
        users = row.metric_values[0].value
        rows.append([date, int(users)])
    if rows:  # Verifica que hay filas antes de crear el DataFrame
        df = pd.DataFrame(rows, columns=['date', 'activeUsers'])
        df['date'] = pd.to_datetime(df['date'])
        return df
    else:
        return pd.DataFrame()  # Retorna un DataFrame vacío si no hay datos

# Función para obtener datos de Google Trends
def get_trends_data(kw_list, timeframe):
    pytrends = TrendReq(hl='es-ES', tz=360)
    pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo='ES')
    return pytrends.interest_over_time()

# Streamlit UI
st.title('Comparativa de KPIs con Google Trends y Google Analytics 4')

kw_list = st.text_input('Ingrese palabras clave separadas por comas:', 'SEO, Python, IA')
start_date = st.date_input('Fecha de inicio')
end_date = st.date_input('Fecha de fin')

def normalize_data(series):
    if pd.api.types.is_numeric_dtype(series):
        min_val = series.min()
        max_val = series.max()
        if max_val != min_val:  # Evitar división por cero
            return (series - min_val) / (max_val - min_val)
    return series  # Retorna la serie sin cambios si no es numérica


if st.button('Cargar Datos'):
    df = get_ga_data(property_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    if not df.empty:
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)  # Asegúrate de ordenar después de establecer el índice

        timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"
        trends_data = get_trends_data(kw_list.split(','), timeframe)
        trends_data.index = pd.to_datetime(trends_data.index)
        trends_data.sort_index(inplace=True)

        df = df.reindex(trends_data.index, method='nearest')  # Solo reindexa si df no está vacío

        # Normalización y visualización aquí dentro de esta condición
        st.write("Datos de Google Analytics:", df)
        st.write("Datos de Google Trends:", trends_data)

        # Crear y mostrar la gráfica aquí dentro
        # Asegúrate de que la visualización se crea solo si df no está vacío

        # Visualización de datos
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Usuarios activos de Google Analytics', color='tab:red')
        ax1.plot(df.index, df['activeUsers'], color='tab:red')
        ax1.tick_params(axis='y', labelcolor='tab:red')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Interés de Google Trends', color='tab:blue')
        for col in trends_data.columns:
            if col != 'isPartial':
                ax2.plot(trends_data.index, trends_data[col], label=col)
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.error("No se encontraron datos de Google Analytics para las fechas seleccionadas.")
