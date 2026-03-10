import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN Y ESTILO GOVTECH
st.set_page_config(page_title="QUADRUM v1.0 | Sistema de Integridad", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-top: 5px solid #0070C0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #e1e4e8; border-radius: 4px 4px 0px 0px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0070C0 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

# 2. MOTOR DE CARGA MULTI-CAPA
def cargar_capa(hoja, saltar=0):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=hoja, skiprows=saltar)
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except:
        return None

# 3. INTERFAZ PRINCIPAL
st.title("🏛️ QUADRUM v1.0")
st.markdown("### Plataforma de Auditoría Forense Programática | GAD Montecristi")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Escudo_de_Ecuador.svg/150px-Escudo_de_Ecuador.svg.png", width=100)
st.sidebar.title("Navegación Forense")
st.sidebar.info("Protocolo Alfaro Virtus v1.0")

if os.path.exists(EXCEL_FILE):
    # Definición de las Pestañas (Tabs)
    tab_dash, tab_ejes, tab_metas, tab_vars = st.tabs([
        "📊 Dashboard Ejecutivo", 
        "📈 Análisis por Ejes", 
        "⚖️ Auditoría de Metas (M4)", 
        "📚 Diccionario de Variables"
    ])

    # --- PESTAÑA 1: DASHBOARD ---
    with tab_dash:
        c1, c2, c3 = st.columns(3)
        c1.metric("ICPI Global", "38.28%", "-53.97 pp (Brecha)")
        c2.metric("ITAM (Transparencia)", "78.00%", "Nivel: Parcial")
        c3.metric("Nivel AVEP", "Transición Crítica", "🟡")
        
        st.markdown("---")
        st.subheader("Resumen de Resultados Consolidados")
        df_res = cargar_capa("DATA-RESULTADOS", 3)
        if df_res is not None:
            st.dataframe(df_res[['MÉTRICA', 'VALOR', 'NOTA / INTERPRETACIÓN']], use_container_width=True)

    # --- PESTAÑA 2: EJES ---
    with tab_ejes:
        st.subheader("Desempeño de Integridad por Eje Estratégico")
        df_ejes = cargar_capa("DATA-EJES", 1)
        if df_ejes is not None:
            col_eje = [c for c in df_ejes.columns if 'EJE' in c][0]
            col_val = [c for c in df_ejes.columns if 'ICPI' in c][0]
            
            # Gráfico de barras
            st.bar_chart(df_ejes[[col_eje, col_val]].dropna().set_index(col_eje))
            st.dataframe(df_ejes, use_container_width=True)

    # --- PESTAÑA 3: AUDITORÍA (M4) ---
    with tab_metas:
        st.subheader("Capa 3: Matriz de Auditoría Documental (M4-AUDIT)")
        st.markdown("Validación de la Cadena de Integridad Intersistémica (CININ)")
        df_audit = cargar_capa("M4-AUDIT", 3)
        if df_audit is not None:
            # Seleccionamos solo las columnas clave para no saturar
            cols_ver = [c for c in df_audit.columns if c in ['CÓD. PDOT', 'EJE', 'VI', 'TI', 'ESTADO CININ', 'OBS.']]
            st.dataframe(df_audit[cols_ver], use_container_width=True)

    # --- PESTAÑA 4: VARIABLES ---
    with tab_vars:
        st.subheader("Definición de las Variables del Modelo")
        df_vars = cargar_capa("M-TECH-VARS", 1)
        if df_vars is not None:
            st.table(df_vars[['VARIABLE', 'NOMBRE COMPLETO', 'DEFINICIÓN OPERACIONAL']])
            st.latex(r"ICPI = \frac{\sum (P_i \times R_i \times V_i \times E_i \times T_i \times C_i)}{\sum (P_i \times R_i)}")

else:
    st.error(f"🚨 Archivo '{EXCEL_FILE}' no detectado. Por favor, súbelo a tu repositorio de GitHub.")
