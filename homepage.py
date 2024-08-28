import streamlit as st 
import time
import base64

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
# st.sidebar.header("Seleccionando")

# logo_arriaka=st.sidebar.image("/home/pichu/Documentos/api-ga4/informes/images/arriakamarketing.png", width=150)
logo_arriaka=st.sidebar.markdown("[![Arriaka Marketing & Consulting](https://arriakamarketing.com/wp-content/uploads/logo-arriaka-marketing.png)](https://arriakamarketing.com)")

logo_arriaka=st.sidebar.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Logo.svg.original.svg)](https://www.linkedin.com/in/javi-lazaro/)")

logo_analaizer=st.sidebar.markdown("[![analaizer.digital](https://analaizer.digital/wp-content/uploads/2024/07/logo-.webp)](https://analaizer.digital/)")

logo_git=st.sidebar.markdown("[![github](https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png)](https://github.com/pichu2707)")   

        
st.write("""
        En esta primera página creo que es el momento de presentarme, soy Javi Lázaro CEO de Arriaka Marketing & Consulting, Co-CEO de AnalAIzer.digital y me dedico normalmente
        a hacer temas de analítica, código y quitar todos los marrones que se me vayan poniendo por el camino, además de eso, en mis ratos libre me pongo ha hacer frikadas con código
        python como podéis ver en https://interfaz.arriakamarketing.com/.
        """)

EMPEZANDO_API=("""
                Y hoy es el momento de hablar de la API de Google Analytics Data (https://developers.google.com/analytics/devguides/reporting/data/v1?hl=es-419)
                y las cosas que podemos hacer con esta API.
                
                Tened en cuenta que aunque la herramienta es buena no es perfecta, encontraremos problemas que tenemos también en GA4 como por ejemplo:
                """)

def stream_data():
    for palabra in EMPEZANDO_API.split(" "):
        yield palabra + " "
        time.sleep(0.06)
        
if st.button("Empezamos"):
    st.write_stream(stream_data)
    
st.subheader("Problemas de umbrales de datos", divider="blue")
st.write("Si tenemos conectado Googgle Signal puede hacer que por privacidad de los datos tengamos el umbral de datos ")
st.subheader("Problemas de cardinalidad de datos", divider="blue")
st.write("Si tenemos una gran cantidad de datos para una dimensión es superior a 100k filas. ")