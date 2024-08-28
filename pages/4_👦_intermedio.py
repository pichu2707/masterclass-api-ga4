import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, FilterExpression, Filter

#Header de la página

st.set_page_config(page_title="Intermedio", page_icon="👨")

logo=("/home/pichu/Documentos/api-ga4/informes/images/logo.png")
st.html("""
  <style>
    [alt=Logo] {
      height: 6rem;
    }
  </style>
        """)
st.title("MasterClass sobre el uso de la API Analytics Data")
st.markdown("## Dashboard de Análisis de Eventos GA4")
st.logo(
    logo,
    link="https://javilazaro.es",
)

#Documentación del sidebar
    
st.sidebar.markdown("## Donde me podeis encontrar")

logo_arriaka=st.sidebar.markdown("[![Arriaka Marketing & Consulting](https://arriakamarketing.com/wp-content/uploads/logo-arriaka-marketing.png)](https://arriakamarketing.com)")

logo_arriaka=st.sidebar.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Logo.svg.original.svg)](https://www.linkedin.com/in/javi-lazaro/)")

logo_analaizer=st.sidebar.markdown("[![analaizer.digital](https://analaizer.digital/wp-content/uploads/2024/07/logo-.webp)](https://analaizer.digital/)")

logo_git=st.sidebar.markdown("[![github](https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png)](https://github.com/pichu2707)")   

#Lógica de la API
    
# Configuración de las credenciales de Google Analytics
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pichu/Documentos/api-ga4/informes/service_account.json'

# ID de la propiedad de Google Analytics 4
property_id = "347166373"
client = BetaAnalyticsDataClient()

request = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name="date"), Dimension(name="eventName")],
    metrics=[Metric(name="eventCount")],
    date_ranges=[DateRange(start_date="2023-01-01", end_date="today")],
)

# Ejecuta la consulta
response = client.run_report(request)

# Procesamiento de los datos
data = {
    "Fecha": [row.dimension_values[0].value for row in response.rows],
    "Evento": [row.dimension_values[1].value for row in response.rows],
    "Conteo": [int(row.metric_values[0].value) for row in response.rows]
}

st.write("""Aquí podemos hacer el trabajo del Explorador, que si bien GA4 ya nos lo ha dejado bastante bien para trabajarlo
        quizás quieras hacer estos trabajos con un cruzamiento de datos más extenso como podría ser de GSC o quizás Google Trends.
        Es por eso que es útil aprender estos pequeños trucos para trabajarlos""")

st.image("images/filtro-kpis.png")

"""Muestreo de los datos"""
df = pd.DataFrame(data, columns=['Fecha','Evento','Conteo'])
df['Fecha'] = pd.to_datetime(df['Fecha'])

eventos_unicos=df['Evento'].unique().tolist()

selected_events = st.multiselect(
    "Selecciona el/los eventos que quieres filtrar",
    eventos_unicos,
)

# Filtrar el DataFrame basado en la selección
filtered_df = df[df['Evento'].isin(selected_events)]

# Mostrar el DataFrame filtrado
st.write("DataFrame Filtrado:", filtered_df)

# Verificar que el DataFrame filtrado no esté vacío
if not filtered_df.empty:
    # Crear un DataFrame pivotado para el gráfico
    pivot_df = filtered_df.pivot_table(index='Fecha', columns='Evento', values='Conteo', aggfunc='sum')
    
    # Usar Streamlit para graficar
    st.line_chart(pivot_df)
else:
    st.write("No hay datos para mostrar basados en la selección.")