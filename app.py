import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="QUADRUM v1.0", layout="wide")

EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

st.title("🏛️ QUADRUM v1.0 | Dashboard Forense")

if os.path.exists(EXCEL_FILE):
    # Carga directa sin trucos para que no falle por versión
    df_res = pd.read_excel(EXCEL_FILE, sheet_name="DATA-RESULTADOS", skiprows=3)
    
    st.success("✅ Sistema Operativo: Datos de Montecristi Cargados")
    
    col1, col2 = st.columns(2)
    col1.metric("ICPI Global", "38.28%", "-53.97 pp (Forense)")
    col2.metric("Brecha vs SIGAD", "53.97 pp", "Sobrestimación", delta_color="inverse")
    
    st.subheader("Estado de Integridad: Transición Crítica 🟡")
    st.dataframe(df_res.head(10))
else:
    st.error("Archivo no encontrado en GitHub")
