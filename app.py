import streamlit as st
import pandas as pd
import os

# 1. IDENTIDAD Y ESTILO
st.set_page_config(page_title="QUADRUM v1.0 | Montecristi", layout="wide")
st.markdown("<style> .main { background-color: #f8f9fa; } </style>", unsafe_allow_True)

EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

st.title("🏛️ QUADRUM v1.0 | Dashboard Forense")
st.sidebar.title("Menú Principal")

@st.cache_data
def load_data(sheet_name, skip):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, skiprows=skip)
        # LIMPIEZA AUTOMÁTICA DE COLUMNAS (Para evitar KeyErrors)
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        return None

# PROCESAMIENTO
if os.path.exists(EXCEL_FILE):
    df_res = load_data("DATA-RESULTADOS", 3)
    df_eje = load_data("DATA-EJES", 1)
    
    # 2. PANEL DE MÉTRICAS (Fijas para asegurar visualización)
    c1, c2, c3 = st.columns(3)
    c1.metric("ICPI Global", "38.28%", "-53.97 pp", delta_color="inverse")
    c2.metric("Brecha vs SIGAD", "29.22%", "Sobrestimación", delta_color="inverse")
    c3.metric("Nivel AVEP", "Transición Crítica", "🟡")

    st.markdown("---")

    # 3. GRÁFICO SECTORIAL (Con manejo de errores)
    st.subheader("📊 Cumplimiento por Eje Estratégico")
    if df_eje is not None:
        try:
            # Buscamos columnas parecidas a 'EJE' e 'ICPI'
            col_eje = [c for c in df_eje.columns if 'EJE' in c][0]
            col_valor = [c for c in df_eje.columns if 'ICPI' in c][0]
            
            chart_data = df_eje[[col_eje, col_valor]].dropna().head(5)
            st.bar_chart(chart_data.set_index(col_eje))
        except:
            st.warning("Estructura de gráficos en ajuste. Mostrando tabla de datos:")
            st.dataframe(df_eje)

    # 4. TABLA DE METAS
    st.subheader("⚖️ Matriz de Auditoría (DATA-RESULTADOS)")
    if df_res is not None:
        st.dataframe(df_res)
else:
    st.error(f"Archivo '{EXCEL_FILE}' no detectado. Súbelo a GitHub.")
