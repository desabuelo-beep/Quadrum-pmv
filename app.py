import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="QUADRUM v1.0 | Dashboard Forense", layout="wide")

# Estilo visual simple y efectivo
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #0070C0; }
    </style>
    """, unsafe_allow_html=True)

EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

st.title("🏛️ QUADRUM v1.0 | Sistema de Integridad Programática")
st.markdown("### GAD Municipal de Montecristi | Protocolo ALFARO VIRTUS")

# 2. FUNCIÓN DE CARGA SIMPLE (Sin decoradores que den error)
def cargar_datos_seguro(hoja, salto_filas):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=hoja, skiprows=salto_filas)
        # Limpiar nombres de columnas
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error en hoja {hoja}: {e}")
        return None

# 3. VERIFICACIÓN Y DESPLIEGUE
if os.path.exists(EXCEL_FILE):
    # Cargamos los datos directamente
    df_res = cargar_datos_seguro("DATA-RESULTADOS", 3)
    df_eje = cargar_datos_seguro("DATA-EJES", 1)
    
    # MÉTRICAS (Datos fijos de tu tesis para asegurar el impacto visual)
    col1, col2, col3 = st.columns(3)
    col1.metric("ICPI Global", "38.28%", "-53.97 pp", delta_color="inverse")
    col2.metric("Brecha vs SIGAD", "29.22%", "Sobrestimación", delta_color="inverse")
    col3.metric("Nivel AVEP", "Transición Crítica", "🟡")

    st.markdown("---")

    # VISUALIZACIÓN DE TABLAS
    st.subheader("⚖️ Resultados de Auditoría (DATA-RESULTADOS)")
    if df_res is not None:
        st.dataframe(df_res)
    
    st.subheader("📊 Análisis por Ejes (DATA-EJES)")
    if df_eje is not None:
        st.dataframe(df_eje)

else:
    st.error(f"🚨 No encuentro el archivo '{EXCEL_FILE}'.")
    st.info("Asegúrate de que el Excel esté subido a la carpeta principal de tu GitHub.")
