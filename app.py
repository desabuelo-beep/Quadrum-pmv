import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="QUADRUM v1.0 | Dashboard Forense", layout="wide")

@st.cache_data
def load_all_data():
    # Esta función lee las partes críticas de tus 38 módulos
    path = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"
    resumen = pd.read_excel(path, sheet_name="DATA-RESULTADOS", skiprows=3)
    ejes = pd.read_excel(path, sheet_name="DATA-EJES", skiprows=1)
    auditoria = pd.read_excel(path, sheet_name="M4-AUDIT", skiprows=3)
    return resumen, ejes, auditoria

# Intentar cargar el motor
try:
    df_res, df_eje, df_audit = load_all_data()
    
    # 2. CABECERA EJECUTIVA
    st.title("🏛️ QUADRUM v1.0: Sistema de Integridad Programática")
    st.markdown("### GAD Municipal de Montecristi | Protocolo ALFARO VIRTUS")
    
    # 3. MÉTRICAS DE IMPACTO (Fase 6: Dashboard)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ICPI GLOBAL", "38.28%", "-53.97 pp (Brecha)")
    with col2:
        st.metric("TRANSPARENCIA (ITAM)", "78.00%", "Nivel: Parcial")
    with col3:
        st.metric("METAS VI=1", "15 / 20", "75% Verificado")

    # 4. VISUALIZACIÓN POR CAPAS
    menu = st.tabs(["📊 Resultados por Eje", "⚖️ Auditoría de Metas", "📥 Ingesta Forense"])
    
    with menu[0]:
        st.subheader("Análisis Sectorial del ICPI")
        # Filtramos solo las columnas de interés de tu hoja DATA-EJES
        df_plot = df_eje[['EJE', 'ICPI EJE']].dropna().head(5)
        st.bar_chart(df_plot.set_index('EJE'))
        st.dataframe(df_eje)

    with menu[1]:
        st.subheader("Capa 3: Matriz de Auditoría Documental (M4-AUDIT)")
        st.write("Estado de la Cadena de Integridad Intersistémica (CININ):")
        st.dataframe(df_audit[['CÓD. PDOT', 'EJE', 'Vi', 'Ti', 'ESTADO CININ']])

    with menu[2]:
        st.subheader("Capa 2: Ingesta de Evidencia Digital")
        st.info("El sistema está sincronizado con el archivo maestro de la Tesis.")
        st.file_uploader("Actualizar Cédula Presupuestaria (eSIGEF)", type=["xlsx", "csv"])

except Exception as e:
    st.error(f"⚠️ Error de Conexión: {e}")
    st.info("Asegúrate de que el archivo .xlsx esté en la raíz de tu GitHub.")
