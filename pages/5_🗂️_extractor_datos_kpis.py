import streamlit as st
import pandas as pd
import sqlite3
from pytrends.request import TrendReq

st.set_page_config(page_title="Extractor de tendencias", page_icon="🗂️")

# Función para conectarse a la base de datos SQLite
def connect_db():
    db_filename = "/home/pichu/Documentos/api-ga4/informes/bbdd_datos/trends.db"
    return sqlite3.connect(db_filename)

def get_trends_data(keywords):
    pytrends = TrendReq(hl='es-ES', tz=60)
    pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo="ES")
    data = pytrends.interest_over_time()
    if not data.empty:
        if 'isPartial' in data.columns:
            is_partial = data.pop('isPartial')
            data['isPartial'] = is_partial  # Asegúrate de mantener este campo si es necesario
        data.columns = [k.replace(" ", "_") for k in keywords] + ['isPartial']
        # Convertir los datos numéricos para asegurar compatibilidad
        for col in keywords:
            data[col.replace(" ", "_")] = pd.to_numeric(data[col.replace(" ", "_")], errors='coerce')
    return data

def create_table_if_not_exists(keywords):
    conn = connect_db()
    cursor = conn.cursor()
    columns = ', '.join([f"{k.replace(' ', '_')} INTEGER" for k in keywords] + ['isPartial BOOLEAN'])
    sql = f'''
        CREATE TABLE IF NOT EXISTS trends_data (
            date TEXT PRIMARY KEY,
            {columns}
        );
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()

def insert_data_to_sql(data, table_name="trends_data"):
    conn = connect_db()
    try:
        data.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al guardar los datos: {e}")
        return False
    finally:
        conn.close()

# Streamlit UI
st.title('Dashboard de Análisis de Eventos GA4')

keywords_input = st.text_input('Introduce palabras clave separadas por comas', 'SEO, Python, IA')
keywords = [x.strip() for x in keywords_input.split(',')]

if st.button('Cargar datos'):
    create_table_if_not_exists(keywords)
    data = get_trends_data(keywords)
    st.write(data)
    if st.button('Guardar en la base de datos'):
        if insert_data_to_sql(data, 'trends_data'):
            st.success('Datos guardados exitosamente en la base de datos')
        else:
            st.error("No se pudieron guardar los datos en la base de datos.")

if st.button('Eliminar tabla de tendencias'):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS trends_data")
    conn.commit()
    conn.close()
    st.success('Tabla eliminada exitosamente')

if st.checkbox('Mostrar datos existentes'):
    conn = connect_db()
    df = pd.read_sql('SELECT * FROM trends_data', conn)
    conn.close()
    st.write(df)
