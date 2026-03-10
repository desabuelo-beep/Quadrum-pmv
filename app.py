import streamlit as st
import pandas as pd
import os
import plotly.express as px

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL
st.set_page_config(page_title="QUADRUM v1.0 | Dashboard Forense", layout="wide")

# CSS para que se vea como una aplicación profesional
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #0070C0; }
    </style>
    """, unsafe_allow_html=True)

EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

@st.cache_data
def load_all_sheets():
    # Cargamos las 3 hojas críticas para la visualización del PMV
    res = pd.read_excel(EXCEL_FILE, sheet_name="DATA-RESULTADOS", skiprows=3)
    ejes = pd.read_excel(EXCEL_FILE, sheet_name="DATA-EJES", skiprows=1)
    audit = pd.read_excel(EXCEL_FILE, sheet_name="M4-AUDIT", skiprows=3)
    return res, ejes, audit

# 2. CUERPO DE LA APLICACIÓN
if os.path.exists(EXCEL_FILE):
    try:
        df_res, df_eje, df_audit = load_all_sheets()
        
        # SIDEBAR
        st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e8/Escudo_de_Ecuador.svg", width=80)
        st.sidebar.title("QUADRUM v1.0")
        st.sidebar.info("Protocolo: ALFARO VIRTUS\nGAD: Montecristi\nEstado: Auditoría Activa")
        menu = st.sidebar.radio("Navegación Táctica:", ["📊 Dashboard Ejecutivo", "⚖️ Auditoría Forense", "📑 Documentación"])

        if menu == "📊 Dashboard Ejecutivo":
            st.title("🏛️ Panel de Integridad Programática")
            st.markdown("### Resultados Consolidados del Motor SIAP-ICPI")
            
            # KPIs - LAS MÉTRICAS DE TU TESIS
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("ICPI GLOBAL", "38.28%", "-53.97 pp", delta_color="inverse")
            c2.metric("BRECHA PDOT", "29.22%", "Sobrestimación", delta_color="inverse")
            c3.metric("NIVEL AVEP", "Transición Crítica", "🟡")
            c4.metric("METAS VI=1", "15 / 20", "Verificadas")

            st.markdown("---")
            
            # GRÁFICOS INTERACTIVOS
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.subheader("Cumplimiento por Eje Estratégico")
                # Limpiamos columnas para el gráfico
                df_eje.columns = [str(c).strip().upper() for c in df_eje.columns]
                fig_ejes = px.bar(df_eje.dropna(subset=['EJE']), x='EJE', y='ICPI EJE', 
                                 color='ICPI EJE', color_continuous_scale='RdYlGn',
                                 labels={'ICPI EJE':'Índice %'})
                st.plotly_chart(fig_ejes, use_container_width=True)

            with col_b:
                st.subheader("Distribución de Pesos (Pi)")
                fig_pie = px.pie(df_audit, values='Vi', names='EJE', hole=.3,
                                 title="Metas con Evidencias por Eje")
                st.plotly_chart(fig_pie, use_container_width=True)

        elif menu == "⚖️ Auditoría Forense":
            st.title("Módulo de Verificación de Metas")
            # Buscador por meta
            busqueda = st.text_input("🔍 Buscar Meta o Código PDOT:")
            df_filtrado = df_audit[df_audit.apply(lambda row: busqueda.lower() in str(row).lower(), axis=1)]
            st.dataframe(df_filtrado)

        elif menu == "📑 Documentación":
            st.title("Glosario y Metadatos")
            st.latex(r"ICPI = \frac{\sum (P_i \times R_i \times V_i \times E_i \times T_i \times C_i)}{\sum (P_i \times R_i)}")
            st.write("El modelo SIAP-ICPI garantiza la trazabilidad biográfica del dato público.")

    except Exception as e:
        st.error(f"Error en la arquitectura de datos: {e}")
else:
    st.error("Archivo 'SIAP-ICPI_VERSION_EJECUTIVA.xlsx' no detectado en el repositorio.")
