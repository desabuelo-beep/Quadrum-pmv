 import streamlit as st
import pandas as pd
import os

# 1. IDENTIDAD Y ESTILO (Corregido y Mejorado)
st.set_page_config(page_title="QUADRUM v1.0 | Dashboard Forense", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #0070C0; }
    </style>
    """, unsafe_allow_html=True)

EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

# 2. CARGA INTELIGENTE (Capa de Datos)
@st.cache_data
def load_data(sheet_name, skip):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, skiprows=skip)
        # Limpiamos nombres de columnas para que Python no se confunda
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        return None

# 3. CABECERA OFICIAL
st.title("🏛️ QUADRUM v1.0 | Sistema de Integridad Programática")
st.markdown("### GAD Municipal de Montecristi | Protocolo ALFARO VIRTUS")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Escudo_de_Ecuador.svg/150px-Escudo_de_Ecuador.svg.png", width=100)
st.sidebar.title("Menú de Auditoría")

# 4. PROCESAMIENTO Y VISUALIZACIÓN
if os.path.exists(EXCEL_FILE):
    df_res = load_data("DATA-RESULTADOS", 3)
    df_eje = load_data("DATA-EJES", 1)
    
    # PANEL DE MÉTRICAS (Datos Reales de tu Tesis)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("ICPI Global", "38.28%", "-53.97 pp", delta_color="inverse")
    c2.metric("Brecha vs SIGAD", "29.22%", "Sobrestimación", delta_color="inverse")
    c3.metric("ITAM (Transparencia)", "78.0%", "Nivel: Parcial")
    c4.metric("Nivel AVEP", "Transición Crítica", "🟡")

    st.markdown("---")

    # SISTEMA DE PESTAÑAS (Para orden pedagógico)
    tab1, tab2, tab3 = st.tabs(["📊 Análisis Sectorial", "⚖️ Matriz de Metas", "📥 Ingesta Forense"])

    with tab1:
        st.subheader("Cumplimiento por Eje Estratégico")
        if df_eje is not None:
            try:
                # Buscamos columnas de forma inteligente
                col_eje = [c for c in df_eje.columns if 'EJE' in c][0]
                col_valor =
