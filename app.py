import streamlit as st
import pandas as pd
import os

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="QUADRUM v1.0 | Montecristi", layout="wide")

st.title("🏛️ QUADRUM v1.0 | Dashboard Forense")
st.markdown("---")

# 1. VERIFICACIÓN DE ARCHIVOS
EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

if not os.path.exists(EXCEL_FILE):
    st.error(f"❌ No se encuentra el archivo '{EXCEL_FILE}' en GitHub.")
    st.stop()

@st.cache_data
def load_data(sheet, skip):
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name=sheet, skiprows=skip)
    except Exception as e:
        st.warning(f"No se pudo cargar la hoja {sheet}: {e}")
        return None

# CARGA DE DATOS
df_res = load_data("DATA-RESULTADOS", 3)
df_eje = load_data("DATA-EJES", 1)

# INTERFAZ PRINCIPAL
if df_res is not None:
    # MÉTRICAS MAESTRAS
    c1, c2, c3 = st.columns(3)
    c1.metric("ICPI GLOBAL", "38.28%", "-53.97 pp")
    c2.metric("Nivel AVEP", "Transición Crítica", "🟡")
    c3.metric("Metas Auditadas", "20", "n=20")

    st.markdown("---")

    # SOLUCIÓN AL ERROR 'EJE' (Detección automática de columnas)
    st.subheader("📊 Análisis Sectorial")
    if df_eje is not None:
        # Buscamos las columnas correctas sin importar si tienen espacios o mayúsculas
        df_eje.columns = [str(c).strip().upper() for c in df_eje.columns]
        
        if 'EJE' in df_eje.columns and 'ICPI EJE' in df_eje.columns:
            st.bar_chart(df_eje.set_index('EJE')['ICPI EJE'])
        else:
            st.warning("Estructura de columnas en 'DATA-EJES' no reconocida. Mostrando tabla cruda:")
            st.dataframe(df_eje)

    # TABLA DE AUDITORÍA
    st.subheader("⚖️ Matriz de Resultados (DATA-RESULTADOS)")
    st.dataframe(df_res)
else:
    st.error("Error crítico: No se pudieron procesar los datos del Excel.")
