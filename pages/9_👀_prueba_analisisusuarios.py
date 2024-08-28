import os
import pandas as pd
import statsmodels.api as sm
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

st.set_page_config(page_title="Empezando", page_icon="👶")

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

# Configuración de las credenciales de Google Analytics
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pichu/Documentos/api-ga4/informes/service_account.json'

# ID de la propiedad de Google Analytics 4
property_id = "347166373"
client = BetaAnalyticsDataClient()

# Configurando la solicitud
request = RunReportRequest(
    property=f'properties/{property_id}',
    dimensions=[Dimension(name="date")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="2023-01-01", end_date="2024-08-20")]
)

# Ejecutar la consulta
response = client.run_report(request)

# Extraer datos para análisis
data = [(row.dimension_values[0].value, int(row.metric_values[0].value)) for row in response.rows]

# Convertir datos a DataFrame
df = pd.DataFrame(data, columns=['Fecha', 'UsuariosActivos'])
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Conversión de la fecha a ordinal para regresión
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['FechaOrdinal'] = df['Fecha'].map(pd.Timestamp.toordinal)

# Streamlit UI
st.title('Análisis de Usuarios Activos de Google Analytics')
st.write("### Datos de Usuarios Activos:")
st.dataframe(df.set_index('Fecha'))

# Modelo de regresión
X = sm.add_constant(df['FechaOrdinal'])  # Añadir constante
y = df['UsuariosActivos']
model = sm.OLS(y, X).fit()

# Mostrar resultados de la regresión
st.write("### Resultados de la Regresión Lineal:")
st.text(str(model.summary()))

# Gráfica de los datos
st.write("### Gráfica de Usuarios Activos:")
fig, ax = plt.subplots()
ax.plot(df['Fecha'], df['UsuariosActivos'], marker='o', linestyle='-')
ax.set_title("Número de Usuarios Activos por Fecha")
ax.set_xlabel("Fecha")
ax.set_ylabel("Usuarios Activos")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
