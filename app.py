import streamlit as st
import pandas as pd

# 1. CARGA DE DATOS (El motor lee tu Excel)
@st.cache_data
def load_data():
    file_path = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"
    # Leemos las hojas clave de tu archivo
    df_resumen = pd.read_excel(file_path, sheet_name="DATA-RESULTADOS", skiprows=3)
    df_ejes = pd.read_excel(file_path, sheet_name="DATA-EJES", skiprows=1)
    return df_resumen, df_ejes

try:
    df_resumen, df_ejes = load_data()
    st.success("✅ Base de Datos QUADRUM conectada exitosamente")
except:
    st.error("❌ Error: Asegúrate de que el archivo Excel esté subido a GitHub con el nombre correcto.")

# 2. INTERFAZ EJECUTIVA
st.title("🏛️ QUADRUM v1.0 | Dashboard Forense")

# Mostramos el ICPI Real que está en tu Excel
icpi_valor = "38.28%" # Esto lo podemos extraer dinámicamente
st.metric(label="ICPI Global - GAD Montecristi", value=icpi_valor, delta="-53.97 pp vs Meta 2027")

# 3. MOSTRAR TABLAS REALES DEL EXCEL
st.subheader("Visualización de Matrices de la Tesis")
tab1, tab2 = st.tabs(["Resultados por Eje", "Vista Previa de Datos"])

with tab1:
    # Mostramos los datos de tu hoja DATA-EJES
    st.write("Análisis Sectorial extraído de la hoja DATA-EJES:")
    st.dataframe(df_ejes.head(10)) # Muestra las primeras 10 filas

with tab2:
    st.write("Resultados Consolidados extraídos de DATA-RESULTADOS:")
    st.dataframe(df_resumen.head(10))
