import os
from datetime import datetime
import csv

import streamlit as st
import pandas as pd 

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

st.set_page_config(page_title="Prueba Forms", page_icon="👀")

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

request = RunReportRequest(
property=f"properties/{property_id}",
dimensions=[
    Dimension(name="pageLocation"),
    Dimension(name="eventName"),
    Dimension(name="date"),
],
metrics=[
        Metric(name="sessions"),
        Metric(name="conversions")
        ],
date_ranges=[DateRange(start_date="2023-06-01", end_date="today")],
)

response = client.run_report(request)
print(response)
tabla = []

for fila in response.rows:
    urls = fila.dimension_values[0].value
    eventName = fila.dimension_values[1].value
    fecha_string = fila.dimension_values[2].value
    fecha = datetime.strptime(fecha_string, '%Y%m%d').date()
    sesiones = fila.metric_values[0].value
    conversions = fila.metric_values[1].value

    tabla.append([fecha, urls, sesiones, eventName, conversions])
    
df = pd.DataFrame(tabla, columns=['Fecha', 'URL', 'Sesiones', 'Nombre del evento', 'Conversiones'])
st.dataframe(df)

st.markdown("## Configuración de los diferentes campos")
st.image("/home/pichu/Documentos/api-ga4/informes/images/dimensio-metricas-forms.png")
st.write("""Como vemos ahora tenemos que hacer un bucle for para hacer las separaciones 
        de cada uno de los puntos""")

if st.button("Crear CSV"):
    nombre_archivo = "forms_mensuales-streamit.csv"
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #Escribiendo encabezados
        writer.writerow(['sessionDefaultChannelGroup', 'fecha', 'sesiones','Evento', 'conversiones'])

        #Escribir datos
        for fila in tabla:
            writer.writerow(fila)
        
    st.success("csv creado")