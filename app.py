import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="QUADRUM v1.0 | Montecristi", layout="wide")

# Nombre exacto del archivo
EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

# SIDEBAR CORPORATIVO
st.sidebar.title("🏛️ QUADRUM v1.0")
st.sidebar.markdown("**Protocolo Alfaro Virtus**")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegación:", ["📊 Dashboard Ejecutivo", "⚖️ Auditoría por Metas", "📥 Ingesta Forense"])

if os.path.exists(EXCEL_FILE):
    # Carga de hojas
    df_res = pd.read_excel(EXCEL_FILE, sheet_name="DATA-RESULTADOS", skiprows=3)
    df_ejes = pd.read_excel(EXCEL_FILE, sheet_name="DATA-EJES", skiprows=1)
    
    if menu == "📊 Dashboard Ejecutivo":
        st.title("Panel de Integridad Programática")
        st.success("✅ Base de Datos Conectada exitosamente")
        
        # MÉTRICAS
        c1, c2, c3 = st.columns(3)
        c1.metric("ICPI Global", "38.28%", "-53.97 pp", delta_color="inverse")
        c2.metric("Brecha vs SIGAD", "29.22%", "Sobrestimación", delta_color="inverse")
        c3.metric("Nivel AVEP", "Transición Crítica", "🟡")
        
        st.markdown("---")
        st.subheader("Análisis de Cumplimiento por Eje Estratégico")
        # Gráfico de Barras Real
        st.bar_chart(df_ejes.set_index('EJE')['ICPI EJE'])

    elif menu == "⚖️ Auditoría por Metas":
        st.title("Motor SIAP-ICPI | Desglose Forense")
        st.write("Variables: $P_i \times R_i \times V_i \times T_i \times C_i$")
        st.dataframe(df_res[['MÉTRICA', 'VALOR', 'NOTA / INTERPRETACIÓN']])

else:
    st.error("Archivo no encontrado. Verifica que el Excel esté en GitHub.")
