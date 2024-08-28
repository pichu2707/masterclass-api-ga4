import os

import pandas as pd
import streamlit as st

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

st.set_page_config(page_title="Prueba reportes", page_icon="👀")

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
client=BetaAnalyticsDataClient()


request = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name="date")],
    metrics=[Metric(name="sessions")],
    date_ranges=[DateRange(start_date="2023-08-20", end_date="today")],
)
response = client.run_report(request)

tabla=[]
for rowIdx, row in enumerate(response.rows):
  for dimension_value, metric_value in zip(row.dimension_values, row.metric_values):
      fecha=dimension_value.value
      sesiones=metric_value.value
      tabla.append([fecha, sesiones])

    
df = pd.DataFrame(tabla, columns=['Fecha', 'Sesiones'])
df['Fecha']=pd.to_datetime(df['Fecha'])
df['Sesiones']=pd.to_numeric(df['Sesiones'], errors='coerce')
st.dataframe(df)
st.line_chart(df,
            x="Fecha",
            y="Sesiones",
            x_label="Fecha",
            y_label="Sesiones")