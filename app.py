 import streamlit as st
import pandas as pd
import os

# 1. IDENTIDAD Y ESTILO (Corregido al 100%)
st.set_page_config(page_title="QUADRUM v1.0 | Dashboard Forense", layout="wide")

# Estilo para que se vea profesional
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #0070C0; }
    </style>
    """, unsafe_allow_html=True)

EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

# 2. CARGA DE DATOS
@st.cache_data
def load_data(sheet_name, skip):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, skiprows=skip)
        # Limpieza de columnas para evitar errores de nombres
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        return None

# 3. CABECERA
st.title("🏛️ QUADRUM v1.0 | Sistema de Integridad Programática")
st.markdown("### GAD Municipal de Montecristi | Protocolo ALFARO VIRTUS")
st.sidebar.title("Menú de Auditoría")

# 4. LÓGICA DE VISUALIZACIÓN
if os.path.exists(EXCEL_FILE):
    df_res = load_data("DATA-RESULTADOS", 3)
    df_eje = load_data("DATA-EJES", 1)
    
    # MÉTRICAS MAESTRAS (Extraídas de tu tesis)
    c1, c2, c3 = st.columns(3)
    c1.metric("ICPI Global", "38.28%", "-53.97 pp", delta_color="inverse")
    c2.metric("Brecha vs SIGAD", "29.22%", "Sobrestimación", delta_color="inverse")
    c3.metric("Nivel AVEP", "Transición Crítica", "🟡")

    st.markdown("---")

    # PESTAÑAS
    tab1, tab2 = st.tabs(["📊 Análisis Sectorial", "⚖️ Matriz de Metas"])

    with tab1:
        st.subheader("Cumplimiento por Eje Estratégico")
        if df_eje is not None:
            try:
                # Buscamos columnas de forma inteligente
                col_eje = [c for c in df_eje.columns if 'EJE' in c][0]
                col_valor = [c for c in df_eje.columns if 'ICPI' in c][0]
                chart_data = df_eje[[col_eje, col_valor]].dropna().head(5)
                st.bar_chart(chart_data.set_index(col_eje))
            except:
                st.dataframe(df_eje)

    with tab2:
        st.subheader("Resultados
