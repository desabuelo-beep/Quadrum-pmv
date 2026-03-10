import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="QUADRUM v1.0", layout="wide")

# Nombre exacto que debe tener el archivo en GitHub
NOMBRE_ARCHIVO = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

st.title("🏛️ QUADRUM v1.0 | Dashboard Forense")

# 1. VERIFICAMOS SI EL ARCHIVO EXISTE
if os.path.exists(NOMBRE_ARCHIVO):
    try:
        # Cargamos los datos
        df_resumen = pd.read_excel(NOMBRE_ARCHIVO, sheet_name="DATA-RESULTADOS", skiprows=3)
        
        st.success(f"✅ Conectado a la Base de Datos: {NOMBRE_ARCHIVO}")
        
        # Dashboard Principal
        col1, col2 = st.columns(2)
        col1.metric("ICPI Global", "38.28%", "-53.97 pp")
        col2.metric("Estado CININ", "Transición Crítica", "🟡")
        
        st.subheader("Vista Previa de la Auditoría (DATA-RESULTADOS)")
        st.dataframe(df_resumen.head(15))
        
    except Exception as e:
        st.error(f"❌ Error al leer las hojas del Excel: {e}")
        st.info("Revisa que las pestañas se llamen exactamente 'DATA-RESULTADOS'.")
else:
    st.error(f"❌ ARCHIVO NO ENCONTRADO: '{NOMBRE_ARCHIVO}'")
    st.warning("⚠️ Instrucción: Ve a GitHub y sube el Excel con ese nombre exacto. Si el nombre es distinto, el sistema no lo verá.")
    st.info("Archivos detectados en el servidor actualmente: " + str(os.listdir()))
