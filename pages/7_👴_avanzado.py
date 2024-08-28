import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import streamlit as st
import matplotlib.dates as mdates

from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

st.set_page_config(page_title="Avanzado", page_icon="👨‍🦳")

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

st.markdown("## Usamos machine learning para hacer una previsión de tráfico")
st.write("Tenemos que tener en cuenta que para hacer ya estos trabajos dependemos también de la cantidad de datos que podamos acumular")
st.write("""
        Si tenemos una cantidad de datos pequeña como vemos en estos casos, (No me han dejado usar una base de datos más grande) la predicción que tenemos no será fiable
        Para ello podremos un modelo de puntuación que son el R² y el MSE (error cuadrático Medio)
        """)
st.latex(r'''MSE = (\frac{1}{n})\sum(y_n-\bar{y}_i)²''')
st.write("""
        Todo el código, o al menos la parte pricipal que hemos visto es igual a lo ya visto anteriormente, lo único que estamos haciendo ya es ampliar este código para sacar esa
        información que precisamos para nuestro proyecto o bien la información que nos han pedido.
        Las librerías como vemos son las mismas incluyendo lo que vamos a hacer con esos datos, en este caso sklearn""")

st.image("images/libreria-avanzado.png")

# ID de la propiedad de Google Analytics 4
property_id = "347166373"
client = BetaAnalyticsDataClient()

# Función para obtener datos de la API de Google Analytics
def fetch_data(property_id, start_date, end_date):
    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
    )
    response = client.run_report(request)
    data = [(row.dimension_values[0].value, int(row.metric_values[0].value)) for row in response.rows]
    return pd.DataFrame(data, columns=['Fecha', 'Sesiones'])

# Cargar datos
df = fetch_data(property_id, "2023-01-01", "today")
df['Fecha'] = pd.to_datetime(df['Fecha'])

st.markdown("### Selección de gurpo de datos")
# Opciones de agrupamiento
option = st.selectbox(
    'Cómo desea agrupar los datos?',
    ('Diario', 'Semanal', 'Mensual')
)

if option == 'Semanal':
    df = df.resample('W', on='Fecha').sum().reset_index()
elif option == 'Mensual':
    df = df.resample('M', on='Fecha').sum().reset_index()

# Preparar datos para regresión
df['FechaOrdinal'] = df['Fecha'].map(pd.Timestamp.toordinal)
X = df[['FechaOrdinal']]
y = df['Sesiones']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo de regresión
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Evaluación del modelo
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# Streamlit UI para mostrar gráfica y resultados
st.write("### Métricas de Evaluación del Modelo:")
st.write("MSE: óptimo debería ser lo más cercano a 0")
st.write(f"MSE: {mse:.2f}")
st.write("El R² óptimo sería le más cercano a 1")
st.write(f"R2 Score: {r2:.2f}")
st.info("Hay que tener en cuenta que unos datos muy óptimos puede darnos indicios de overfitting")
st.divider()

if st.button("Ver gráfica"):
    st.write("### Gráfica de Predicción vs Realidad:")
    fig, ax = plt.subplots(figsize=(10, 6))
    X_test_dates = pd.to_datetime(X_test['FechaOrdinal'].map(pd.Timestamp.fromordinal))
    ax.scatter(X_test_dates, y_test, color='blue', label='Datos Reales')
    ax.plot(X_test_dates, predictions, color='red', label='Predicciones')
    ax.set_title("Predicción vs Realidad de las Sesiones")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Sesiones")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
