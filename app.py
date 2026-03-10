"""
QUADRUM v1.0 — Sistema Integral de Auditoría y Planificación SIAP-ICPI
Protocolo ALFARO VIRTUS · GAD Municipal de Montecristi
app.py — Versión Definitiva Blindada
"""

import streamlit as st
import pandas as pd
import os

# ═══════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="QUADRUM v1.0 · GAD Montecristi",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.main { background-color: #f0f4f9; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #0d2040 100%);
    border-right: 2px solid #1a4a8a;
}
[data-testid="stSidebar"] * { color: #c8d8f0 !important; }
[data-testid="stSidebar"] h2 { color: #ffffff !important; font-size: 1.1rem !important; }
.stTabs [data-baseweb="tab-list"] {
    gap: 4px; background-color: #e2e8f0; border-radius: 10px; padding: 5px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px; padding: 8px 15px; font-weight: 600; font-size: 0.82rem; color: #4a5568;
}
.stTabs [aria-selected="true"] { background-color: #1a4a8a !important; color: #ffffff !important; }
.kpi-card {
    background: #ffffff; border-radius: 12px; padding: 18px 20px;
    border-top: 4px solid #1a4a8a;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07); text-align: center;
}
.kpi-card.rojo { border-top-color: #c0392b; }
.kpi-card.naranja { border-top-color: #e67e22; }
.kpi-card.amarillo{ border-top-color: #d4a017; }
.kpi-card.verde { border-top-color: #1a7a4a; }
.kpi-label { font-size: 0.70rem; font-weight: 700; color: #718096; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 6px; }
.kpi-value { font-size: 1.85rem; font-weight: 800; line-height: 1.1; margin-bottom: 4px; }
.kpi-sub { font-size: 0.74rem; color: #888; }
.banner {
    background: linear-gradient(135deg, #0a1628 0%, #1a4a8a 60%, #0070C0 100%);
    border-radius: 14px; padding: 22px 30px; margin-bottom: 20px; color: white;
}
.banner h1 { color: white; font-size: 1.55rem; margin: 0 0 4px 0; font-weight: 800; }
.banner p { color: #a8c8f0; margin: 0; font-size: 0.88rem; }
.sec-header {
    background: linear-gradient(90deg, #1a4a8a, #0070C0);
    color: white; padding: 9px 18px; border-radius: 8px;
    font-weight: 700; font-size: 0.88rem; margin: 16px 0 10px 0;
}
.aviso {
    background: #ebf4ff; border-left: 4px solid #0070C0;
    padding: 12px 16px; border-radius: 6px;
    font-size: 0.84rem; color: #1a3a5c; margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

@st.cache_data(show_spinner=False)
def cargar_hoja(nombre_hoja: str, skiprows: int, nrows: int = None):
    if not os.path.exists(EXCEL_FILE):
        return None
    try:
        xls = pd.ExcelFile(EXCEL_FILE)
        hoja_real = next((h for h in xls.sheet_names if nombre_hoja.strip().upper() in h.strip().upper()), None)
        if hoja_real is None: return None
        kwargs = dict(sheet_name=hoja_real, skiprows=skiprows)
        if nrows: kwargs["nrows"] = nrows
        df = pd.read_excel(EXCEL_FILE, **kwargs)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception:
        return None

with st.sidebar:
    st.markdown("## 🏛️ QUADRUM v1.0")
    st.markdown("**Protocolo ALFARO VIRTUS**")
    st.markdown("---")
    st.markdown("**Institución:** GAD Montecristi\n**Período:** 2023–2027\n**Muestra:** n = 20 metas PDOT\n**Motor:** SIAP-ICPI")
    if os.path.exists(EXCEL_FILE): st.success("✅ Excel conectado")
    else: st.error("❌ Excel no encontrado")

st.markdown('<div class="banner"><h1>🏛️ QUADRUM v1.0 — SIAP-ICPI</h1><p>Protocolo ALFARO VIRTUS | GAD Montecristi</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📈 Ejes PDOT", "⚖️ Motor ICPI (M5)", "🔍 Auditoría (M4)", "🚨 Brecha", "🌐 ITAM", "🔭 Prospectiva", "📋 Resultados"])

with tab2:
    st.subheader("⚖️ Motor Central ICPI — Ecuación Canónica (M5)")
    st.latex(r"ICPI = \frac{\sum (P_i \times R_i \times V_i \times T_i \times C_i)}{\sum (P_i \times R_i)} \times 100")
    df_m5_raw = cargar_hoja("M5-ICPI", skiprows=2, nrows=23)
    if df_m5_raw is not None:
        st.dataframe(df_m5_raw)

with tab7:
    st.subheader("📋 Resultados Consolidados")
    st.info("Resumen final de la auditoría forense.")
