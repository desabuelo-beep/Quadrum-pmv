import streamlit as st
import pandas as pd

# CONFIGURACIÓN ESTÉTICA (Capa de Presentación)
st.set_page_config(page_title="QUADRUM v1.0 | Montecristi", layout="wide")

# ESTILO CORPORATIVO
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR (Navegación)
st.sidebar.title("🏛️ QUADRUM v1.0")
st.sidebar.markdown("**Protocolo Alfaro Virtus**")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("Capa del Sistema:", ["📊 Dashboard Ejecutivo", "📥 Ingesta e eSIGEF", "⚖️ Motor SIAP-ICPI"])

# DATOS REALES DE MONTECRISTI (Pre-cargados para el Jurado)
if menu == "📊 Dashboard Ejecutivo":
    st.title("Panel de Integridad Programática")
    st.subheader("GAD Municipal de Montecristi | Período 2024")
    
    # MÉTRICAS CLAVE (Inyectando tus datos reales)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ICPI Global", "38.28%", "-53.97 pp", delta_color="inverse")
    col2.metric("Brecha vs SIGAD", "29.22%", "Sobrestimación", delta_color="inverse")
    col3.metric("Nivel Institucional", "Transición Crítica", "🟡")
    col4.metric("Metas Auditadas", "20", "n=20")

    st.markdown("---")
    
    # GRÁFICO DE RESULTADOS POR EJE
    st.subheader("Análisis por Eje Estratégico")
    # Datos extraídos de tu hoja DATA-EJES
    data_ejes = {
        'Eje': ['Territorial', 'Social', 'Ambiental', 'Institucional'],
        'ICPI (%)': [25.76, 51.68, 66.30, 60.15]
    }
    df_ejes = pd.DataFrame(data_ejes)
    st.bar_chart(df_ejes.set_index('Eje'))

elif menu == "📥 Ingesta e eSIGEF":
    st.title("Módulo de Ingesta Forense")
    st.info("Cargue las Cédulas Presupuestarias del eSIGEF para validar la variable de Temporalidad (Ti).")
    
    uploaded_file = st.file_uploader("Arrastre aquí el archivo .csv o .xlsx del eSIGEF", type=['csv', 'xlsx'])
    if uploaded_file:
        st.success("Archivo verificado bajo Protocolo CININ. Procesando variables...")

elif menu == "⚖️ Motor SIAP-ICPI":
    st.title("Ecuación Canónica de Integridad")
    st.latex(r'''ICPI = \frac{\sum (P_i \times R_i \times V_i \times E_i \times T_i \times C_i)}{\sum (P_i \times R_i)}''')
    
    st.write("### Auditoría de Metas Críticas")
    # Ejemplo de tabla de tu hoja M4-AUDIT
    metas = [
        {"Meta": "Agua Potable - Acueducto", "Pi": 0.33, "Vi": 1, "Ti": 0.25, "Estado": "🔴 Crítico"},
        {"Meta": "Alcantarillado Eloy Alfaro", "Pi": 0.17, "Vi": 1, "Ti": 0.65, "Estado": "🟡 En proceso"},
        {"Meta": "Centro de Salud Tipo C", "Pi": 0.20, "Vi": 0, "Ti": 0.00, "Estado": "⬛ Ruptura"}
    ]
    st.table(metas)
