
import os

import streamlit as st
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

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


st.markdown("## Activación de la API")
st.write("""
        Podemos creaer primeramente un proyecto para hacer esta conexión, a partir de aquí es común en los demás trabajos
        * Activamos al API de Google analytics data
        * Creamos las credenciales
        * Tenemos el correo de la API: ga4-masterclass@api-ga4-433322.iam.gserviceaccount.com
        * Creamos una cuenta de servicio para la privacidad de la API
        * Después en la página de las credenciales damos  al correo y entramos en clave, agregamos una clave como JSON y la descargamos
        
        Ahora en GA4 vamos a toamr la ID de nuestro proyecto:
        * Vamos a tomar la ID del proyecto que vamos a medir que están en la pestaña de propiedad: 347166373
        * Con la cuenta le damos los permisos de editor al correo que hemos copiado anteriormente de la API
        
        La página para saber las dimensiones y métricas que hay en GA4 es: https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema?hl=es-419 
        """)
st.markdown("## Librerías")
st.write("""Las librerías que vamos a utilizar son las que nos indica Google para descargarlas 
        solamente tienes que escribir pip install google-analytics-data con lo que la gran mayoría de nuestros
        códigos comenzarán igual.""")
st.markdown("### BetaAnalyticsDataClient()")
st.write("""Es la clase que nos ayudará a conectar con la API para la autenticación, por la instancia 
        podremos hacer solicitudes a la API y haremos una consulta porque ahí es donde podemos hacer
        la especificación de las dimensiones, métricas y otros filtros """)
st.markdown("### BetaAnalyticsDataClient()")
st.write("Lugar donde vamos a especificar, métricas, dimensiones, filtros y segmentos.")
st.image("/home/pichu/Documentos/api-ga4/informes/images/librerias.png")

st.markdown("## Conexión con las credenciales de la API")
st.write("Aquí hacemos la conexión de la API con las credenciales que tenemos en el JSON que hemos descargado")
st.image("/home/pichu/Documentos/api-ga4/informes/images/personal_code.png")

st.markdown("## Haciendo las peticiones que necesitamos")
st.write("Las peticiones con las métricas, dimensiones, filtros y segmentos que necesitamos lo hacemos en el request")
st.image("/home/pichu/Documentos/api-ga4/informes/images/request.png")

st.markdown("## Mostrando los datos")
st.write("Después hacemos el muestreo de los datos según necesitmos")
st.image("/home/pichu/Documentos/api-ga4/informes/images/muestreo.png")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pichu/Documentos/api-ga4/informes/service_account.json'

"""Ejecuta un informe simple sobre una propiedad de Google Analytics 4."""
"""La parte anterior en el código demo de GA4 viene comentado, hay que descomentar y escribir el ID que hemos copiado anteriormente de la propiedad
de GA4"""
property_id = "347166373"

client = BetaAnalyticsDataClient()

request = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name="city")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="2023-05-30", end_date="today")],
)
response = client.run_report(request)

st.markdown("## Nos devuelve")
st.write("Los resultados son:")
tabla=[]
for row in response.rows:
    ciudad=row.dimension_values[0].value
    usuarios_activos=row.metric_values[0].value
    tabla.append([ciudad, usuarios_activos])

df = pd.DataFrame(tabla, columns=['Ciudad', 'Usuarios Activos'])
st.dataframe(df, width=500)