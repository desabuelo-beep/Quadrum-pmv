"""
QUADRUM v1.0 — Sistema de Integridad Programática
Protocolo ALFARO VIRTUS · GAD Municipal de Montecristi
app.py — Versión Definitiva Blindada
Columnas y skiprows verificados directamente desde el Excel.
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
.kpi-card.rojo    { border-top-color: #c0392b; }
.kpi-card.naranja { border-top-color: #e67e22; }
.kpi-card.amarillo{ border-top-color: #d4a017; }
.kpi-card.verde   { border-top-color: #1a7a4a; }
.kpi-label { font-size: 0.70rem; font-weight: 700; color: #718096;
             letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 6px; }
.kpi-value { font-size: 1.85rem; font-weight: 800; line-height: 1.1; margin-bottom: 4px; }
.kpi-sub   { font-size: 0.74rem; color: #888; }
.banner {
    background: linear-gradient(135deg, #0a1628 0%, #1a4a8a 60%, #0070C0 100%);
    border-radius: 14px; padding: 22px 30px; margin-bottom: 20px; color: white;
}
.banner h1 { color: white; font-size: 1.55rem; margin: 0 0 4px 0; font-weight: 800; }
.banner p  { color: #a8c8f0; margin: 0; font-size: 0.88rem; }
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

# ═══════════════════════════════════════════════════════
# CONSTANTE: nombre exacto del archivo
# ═══════════════════════════════════════════════════════
EXCEL_FILE = "SIAP-ICPI_VERSION_EJECUTIVA.xlsx"

# ═══════════════════════════════════════════════════════
# FUNCIÓN ULTRA-ROBUSTA DE CARGA
# ═══════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def cargar_hoja(nombre_hoja: str, skiprows: int, nrows: int = None):
    """
    Carga una hoja del Excel con parámetros exactos verificados.
    Busca el nombre de forma flexible (ignora mayúsculas y espacios).
    Devuelve None si algo falla — nunca lanza excepción.
    """
    if not os.path.exists(EXCEL_FILE):
        return None
    try:
        xls = pd.ExcelFile(EXCEL_FILE)
        hoja_real = next(
            (h for h in xls.sheet_names
             if nombre_hoja.strip().upper() in h.strip().upper()),
            None,
        )
        if hoja_real is None:
            return None
        kwargs = dict(sheet_name=hoja_real, skiprows=skiprows)
        if nrows:
            kwargs["nrows"] = nrows
        df = pd.read_excel(EXCEL_FILE, **kwargs)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception:
        return None


def aviso(texto: str):
    """Mensaje informativo cuando una hoja no carga."""
    st.markdown(
        f'<div class="aviso">ℹ️ {texto} — '
        f'Verifica que <code>{EXCEL_FILE}</code> esté subido a la raíz de tu GitHub.</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏛️ QUADRUM v1.0")
    st.markdown("**Protocolo ALFARO VIRTUS**")
    st.markdown("---")
    st.markdown(
        "**Institución:** GAD Montecristi  \n"
        "**Período:** Plan Bicentenario 2023–2027  \n"
        "**Muestra:** n = 20 metas PDOT  \n"
        "**Motor:** SIAP-ICPI  "
    )
    st.markdown("---")
    st.markdown("**Módulos del sistema:**")
    st.markdown(
        "`M4` Auditoría CININ  \n"
        "`M5` Motor ICPI  \n"
        "`M7` Prospectiva  \n"
        "`DATA-EJES` Sectorial  \n"
        "`DATA-BRECHA` Correctivo  \n"
        "`DATA-ITAM` Transparencia  "
    )
    st.markdown("---")
    if os.path.exists(EXCEL_FILE):
        st.success("✅ Excel conectado")
    else:
        st.error("❌ Excel no encontrado")
        st.caption(f"Sube `{EXCEL_FILE}` a GitHub")
    st.markdown("---")
    st.caption("© 2025 Tesis de Grado")
    st.caption("QUADRUM v1.0 · Auditoría Forense")

# ═══════════════════════════════════════════════════════
# BANNER PRINCIPAL
# ═══════════════════════════════════════════════════════
st.markdown(
    '<div class="banner">'
    "<h1>🏛️ QUADRUM v1.0 — Sistema de Integridad Programática</h1>"
    "<p>GAD Municipal de Montecristi &nbsp;·&nbsp; "
    "Protocolo de Auditoría Forense ALFARO VIRTUS &nbsp;·&nbsp; SIAP-ICPI</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════
# KPIs SIEMPRE VISIBLES
# ═══════════════════════════════════════════════════════
st.markdown(
    '<div class="sec-header">📊 INDICADORES CLAVE · MOTOR SIAP-ICPI · GAD MONTECRISTI</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        '<div class="kpi-card">'
        '<div class="kpi-label">ICPI Global Forense</div>'
        '<div class="kpi-value" style="color:#1a4a8a">38.28%</div>'
        '<div class="kpi-sub">Motor M5-ICPI · n=20 metas</div>'
        "</div>",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        '<div class="kpi-card rojo">'
        '<div class="kpi-label">ICM SIGAD Auto-reporte</div>'
        '<div class="kpi-value" style="color:#c0392b">92.25%</div>'
        '<div class="kpi-sub">Diferencial: +53.97 pp</div>'
        "</div>",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        '<div class="kpi-card naranja">'
        '<div class="kpi-label">Brecha ICPI vs SIGAD</div>'
        '<div class="kpi-value" style="color:#e67e22">−53.97 pp</div>'
        '<div class="kpi-sub">H₁ Confirmada §3.1</div>'
        "</div>",
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        '<div class="kpi-card amarillo">'
        '<div class="kpi-label">Nivel AVEP</div>'
        '<div class="kpi-value" style="color:#d4a017;font-size:1.15rem">Transición<br>Crítica 🟡</div>'
        '<div class="kpi-sub">Escala ≥40% → Transición</div>'
        "</div>",
        unsafe_allow_html=True,
    )
with c5:
    st.markdown(
        '<div class="kpi-card verde">'
        '<div class="kpi-label">ITAM · Transparencia</div>'
        '<div class="kpi-value" style="color:#1a7a4a">78%</div>'
        '<div class="kpi-sub">Parcialmente Opaco 🟡</div>'
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PESTAÑAS
# ═══════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Ejes PDOT",
    "⚖️ Motor ICPI (M5)",
    "🔍 Auditoría CININ (M4)",
    "🚨 Brecha Correctiva",
    "🌐 Transparencia ITAM",
    "🔭 Prospectiva M7",
    "📋 Resultados",
])


# ═══════════════════════════════════════════════════════════════
# TAB 1 · EJES PDOT
# DATA-EJES skip=0 · Col0=EJE (nombre) · Col3=ICPI(%) (float)
# Filas de datos: rows 2-6 (TERRITORIAL…INSTITUCIONAL)
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.subheader("📈 ICPI Desagregado por Eje Estratégico PDOT")
    st.caption("Fuente: DATA-EJES · Motor SIAP-ICPI · valores verificados desde el Excel")

    # Datos de ejes extraídos y verificados del Excel
    ejes_df = pd.DataFrame({
        "Eje Estratégico": [
            "🔵 TERRITORIAL",
            "🔴 SOCIAL",
            "🟢 AMBIENTAL",
            "🟠 ECONÓMICO",
            "🟣 INSTITUCIONAL",
        ],
        "ICPI (%)": [25.76, 51.69, 44.93, 70.00, 60.15],
        "N° Metas": [9, 6, 2, 1, 2],
        "Vi=1": [8, 2, 2, 0, 2],
        "Vi=0": [1, 4, 0, 1, 0],
        "Σ Pi": [0.3316, 0.1691, 0.0856, 0.0012, 0.0204],
        "Semáforo": ["🟠 Crítico", "🟡 Medio", "🟡 Medio", "🟢 Bueno", "🟡 Medio"],
    })

    col_g, col_t = st.columns([3, 2])
    with col_g:
        st.markdown("**ICPI por Eje (%)**")
        st.bar_chart(
            ejes_df.set_index("Eje Estratégico")["ICPI (%)"],
            height=310, use_container_width=True,
        )
    with col_t:
        st.markdown("**Tabla de ejes**")
        st.dataframe(
            ejes_df[["Eje Estratégico", "ICPI (%)", "Vi=1", "Vi=0", "Semáforo"]],
            use_container_width=True, hide_index=True,
        )

    # Intentar cargar datos crudos de DATA-EJES para mostrar valores exactos del motor
    df_ejes_raw = cargar_hoja("DATA-EJES", skiprows=0, nrows=12)
    if df_ejes_raw is not None:
        # Col0=EJE, Col1=Σ Pi num, Col2=Σ PiRi den, Col3=ICPI %
        cols_raw = ["EJE", "Σ_Pi_num", "Σ_PiRi_den", "ICPI_%", "Porc_str",
                    "Semaforo", "N_metas"] + list(df_ejes_raw.columns[7:])
        df_ejes_raw.columns = cols_raw[:len(df_ejes_raw.columns)]
        ejes_filt = df_ejes_raw[
            df_ejes_raw["EJE"].astype(str).str.contains(
                "TERRITORIAL|SOCIAL|AMBIENTAL|ECONÓMICO|INSTITUCIONAL", na=False
            )
        ][["EJE", "Σ_Pi_num", "Σ_PiRi_den", "ICPI_%", "N_metas"]].copy()
        if not ejes_filt.empty:
            st.markdown("**Valores exactos del motor (DATA-EJES)**")
            st.dataframe(ejes_filt, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🧠 Interpretación Forense por Eje")
    ca, cb = st.columns(2)
    with ca:
        st.error(
            "🔵 **TERRITORIAL — 25.76%** · Eje más crítico por volumen presupuestario. "
            "Acueducto CAF ($45.6M) es la gran apuesta del PDOT. Camal y Reservorios son las brechas urgentes."
        )
        st.warning(
            "🔴 **SOCIAL — 51.69%** · Centro de Salud Tipo C (Pi=0.20, mayor peso) es el déficit "
            "más costoso. Requiere convenio urgente con MSP."
        )
    with cb:
        st.warning(
            "🟢 **AMBIENTAL — 44.93%** · Vi=1 en ambas metas pero Ti muy bajo (0.20-0.30). "
            "Relleno sanitario y PTAR son proyectos de activación POA 2025."
        )
        st.success(
            "🟣 **INSTITUCIONAL — 60.15%** · Mejor eje documentado. Catastro y Digitalización "
            "completos (Vi=1, Ti=1). Modelo a replicar en otros ejes."
        )


# ═══════════════════════════════════════════════════════════════
# TAB 2 · MOTOR ICPI (M5)
# M5-ICPI skip=2 · row0=encabezados · rows 1-21=datos PDOT
# Encabezados verificados:
#   col0=CÓD. PDOT  col1=EJE ESTRATÉGICO  col2=Pi (Peso)
#   col3=Ri (Relevancia)  col4=Vi (Verificación)  col5=Ti (Temporalidad)
#   col6=Pi×Ri×Vi×Ti  col7=Pi×Ri (Denominador)  col8=Ci (Control)
#   col9=Semáforo  col10=ESTADO CININ  col11=OBS.
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.subheader("⚖️ Motor Central ICPI — Ecuación Canónica por Meta (M5)")
    st.caption("Fuente: M5-ICPI · 20 metas auditadas · Protocolo ALFARO VIRTUS")

    st.latex(
        r"ICPI = \frac{\sum (P_i \times R_i \times V_i \times T_i \times C_i)}{\sum (P_i \times R_i)} \times 100"
    )

    df_m5_raw = cargar_hoja("M5-ICPI", skiprows=2, nrows=23)

    if df_m5_raw is not None:
        # Fila 0 contiene los encabezados reales verificados
        encabezados = [str(h).strip() for h in df_m5_raw.iloc[0].tolist()]
        df_m5 = df_m5_raw.iloc[1:].copy()
        df_m5.columns = encabezados
        df_m5 = df_m5.reset_index(drop=True)

        df_m5_clean = df_m5[
            df_m5["CÓD. PDOT"].astype(str).str.contains("PDOT", na=False)
        ].copy()

        if not df_m5_clean.empty:
            cols_mostrar = [
                "CÓD. PDOT", "EJE ESTRATÉGICO",
                "Pi (Peso)", "Ri (Relevancia)",
                "Vi (Verificación)", "Ti (Temporalidad)",
                "Pi×Ri×Vi×Ti", "Ci (Control)", "Semáforo",
            ]
            cols_ok = [c for c in cols_mostrar if c in df_m5_clean.columns]

            cf1, cf2 = st.columns(2)
            with cf1:
                ejes_uniq = ["Todos"] + sorted(
                    df_m5_clean["EJE ESTRATÉGICO"].dropna().unique().tolist()
                )
                eje_sel = st.selectbox("🔍 Filtrar por Eje:", ejes_uniq)
            with cf2:
                vi_sel = st.selectbox(
                    "🔍 Filtrar por Vi:",
                    ["Todos", "Vi = 1 (Con evidencia)", "Vi = 0 (Sin evidencia)"],
                )

            df_show = df_m5_clean.copy()
            if eje_sel != "Todos":
                df_show = df_show[df_show["EJE ESTRATÉGICO"] == eje_sel]
            if vi_sel == "Vi = 1 (Con evidencia)":
                df_show = df_show[
                    df_show["Vi (Verificación)"].astype(str).str.strip() == "1"
                ]
            elif vi_sel == "Vi = 0 (Sin evidencia)":
                df_show = df_show[
                    df_show["Vi (Verificación)"].astype(str).str.strip() == "0"
                ]

            st.markdown(f"**Mostrando {len(df_show)} de {len(df_m5_clean)} metas auditadas**")
            st.dataframe(
                df_show[cols_ok].reset_index(drop=True),
                use_container_width=True, hide_index=True,
            )
        else:
            aviso("No se encontraron filas PDOT en la hoja M5-ICPI")
    else:
        aviso("No se pudo cargar la hoja M5-ICPI")

    st.markdown("---")
    st.markdown("#### 📐 Glosario de Variables")
    st.dataframe(
        pd.DataFrame({
            "Variable": ["Pi", "Ri", "Vi", "Ti", "Ci"],
            "Nombre": [
                "Peso Programático", "Relevancia Estratégica",
                "Verificación Documental", "Temporalidad de Ejecución",
                "Coherencia CININ",
            ],
            "Rango": ["0 – 1", "0.5 / 1.0 / 1.5", "0 ó 1", "0.0 – 1.0", "0.0 – 1.0"],
            "Fuente": ["PDOT §3.2", "PDOT §3.3", "D-MAD Silo 6", "Cédula eSIGEF", "CININ §3.4"],
        }),
        use_container_width=True, hide_index=True,
    )


# ═══════════════════════════════════════════════════════════════
# TAB 3 · AUDITORÍA FORENSE M4
# M4-AUDIT skip=2 · row0=encabezados · rows 1-21=datos PDOT
# Encabezados verificados:
#   col0=CÓD. PDOT  col1=EJE  col2=TIPOLOGÍA DOC.  col3=DEPARTAMENTO
#   col4=EVIDENCIA  col5=Vi  col6=Ri  col7=Ti (H)  col8=Vi×Ri×Ti
#   col9=ESTADO DOC.  col10=Vi AUD.  col11=Ti AUD.  col12=REF. DOC.
#   col13=CONSISTENCIA  col14=RESPONSABLE  col15=Pi / Ci
#   col16=PDOT ✓  col17=POA ✓  col18=PAC ✓  col19=Ti CÉDULA
#   col20=SIGAD ✓  col21=CPCCS ✓  col22=Ci CININ  col23=Ci
#   col24=Ti CININ  col25=ESTADO CININ  col26=OBS.
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🔍 Auditoría Forense — Cadena de Integridad CININ (M4)")
    st.caption(
        "Fuente: M4-AUDIT · Validación cruzada: PDOT × POA × PAC × eSIGEF × SIGAD × CPCCS"
    )

    df_m4_raw = cargar_hoja("M4-AUDIT", skiprows=2, nrows=23)

    if df_m4_raw is not None:
        enc_m4 = [str(h).strip() for h in df_m4_raw.iloc[0].tolist()]
        df_m4 = df_m4_raw.iloc[1:].copy()
        df_m4.columns = enc_m4
        df_m4 = df_m4.reset_index(drop=True)

        df_m4_clean = df_m4[
            df_m4["CÓD. PDOT"].astype(str).str.contains("PDOT", na=False)
        ].copy()

        if not df_m4_clean.empty:
            # Vista resumida
            cols_res = [
                "CÓD. PDOT", "EJE", "DEPARTAMENTO", "EVIDENCIA",
                "Vi", "Ti (H)", "ESTADO DOC.", "CONSISTENCIA",
                "ESTADO CININ", "OBS.",
            ]
            cols_ok_res = [c for c in cols_res if c in df_m4_clean.columns]
            st.markdown("**Vista resumida — Campos clave**")
            st.dataframe(
                df_m4_clean[cols_ok_res].reset_index(drop=True),
                use_container_width=True, hide_index=True,
            )

            st.markdown("---")
            # Vista de silos
            cols_sil = [
                "CÓD. PDOT", "EJE",
                "PDOT ✓", "POA ✓", "PAC ✓",
                "Ti CÉDULA", "SIGAD ✓", "CPCCS ✓",
                "Ci CININ", "Ci", "Ti CININ", "ESTADO CININ",
            ]
            cols_ok_sil = [c for c in cols_sil if c in df_m4_clean.columns]
            if cols_ok_sil:
                st.markdown("**Verificación por Silo (cadena documental)**")
                st.dataframe(
                    df_m4_clean[cols_ok_sil].reset_index(drop=True),
                    use_container_width=True, hide_index=True,
                )
        else:
            aviso("No se encontraron filas PDOT en la hoja M4-AUDIT")
    else:
        aviso("No se pudo cargar la hoja M4-AUDIT")

    st.markdown("---")
    st.markdown("#### 🔗 Los 6 Silos de la Cadena CININ")
    st.dataframe(
        pd.DataFrame({
            "Silo": [
                "S1 · PDOT", "S2 · POA", "S3 · PAC/SERCOP",
                "S4 · eSIGEF Cédula", "S5 · SIGAD", "S6 · CPCCS/CNE",
            ],
            "Descripción": [
                "Plan de Desarrollo y Ordenamiento Territorial",
                "Plan Operativo Anual del GAD",
                "Plan Anual de Contrataciones — SERCOP",
                "Cédula presupuestaria devengada — Min. de Finanzas",
                "Sistema de Información para GADs — auto-reporte",
                "Consejo de Participación Ciudadana y Control Social",
            ],
            "Variable que valida": [
                "Vi (existencia del proyecto)",
                "Ti inicio planificado",
                "Ti contratación formal",
                "Ti ejecución financiera",
                "ICM oficial vs ICPI forense",
                "Ci control social externo",
            ],
        }),
        use_container_width=True, hide_index=True,
    )


# ═══════════════════════════════════════════════════════════════
# TAB 4 · BRECHA CORRECTIVA
# DATA-BRECHA skip=4
# Encabezados verificados: COD-META, DESCRIPCIÓN, EJE, Pi, Ri,
#   Δ ICPI si Vi→1, CAUSA DE Vi=0, SITUACIÓN EN PDOT,
#   ACCIÓN CORRECTIVA POA 2025, SISTEMA PDOT, URGENCIA, IMPACTO
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.subheader("🚨 Análisis de Brecha — Potencial Correctivo del ICPI")
    st.caption("Fuente: DATA-BRECHA · H₃: Δ ICPI si Vi→1 · Metas con mayor impacto potencial")

    df_brecha = cargar_hoja("DATA-BRECHA", skiprows=4, nrows=20)

    if df_brecha is not None:
        # Con skip=4, la fila 0 ya son encabezados correctos (verificado)
        df_b = df_brecha[
            df_brecha["COD-META"].astype(str).str.contains("PDOT", na=False)
        ].copy().reset_index(drop=True)

        if not df_b.empty:
            # Tabla de impacto
            cols_imp = [
                "COD-META", "DESCRIPCIÓN", "EJE", "Pi", "Ri",
                "Δ ICPI si Vi→1", "URGENCIA", "IMPACTO",
            ]
            cols_ok = [c for c in cols_imp if c in df_b.columns]
            st.markdown("#### 🎯 Metas ordenadas por impacto potencial")
            st.dataframe(df_b[cols_ok], use_container_width=True, hide_index=True)

            st.markdown("---")
            # Tabla de acción
            cols_acc = [
                "COD-META", "DESCRIPCIÓN",
                "CAUSA DE Vi=0", "SITUACIÓN EN PDOT",
                "ACCIÓN CORRECTIVA POA 2025",
            ]
            cols_ok2 = [c for c in cols_acc if c in df_b.columns]
            st.markdown("#### 🛣️ Causa raíz y acción correctiva POA 2025")
            st.dataframe(df_b[cols_ok2], use_container_width=True, hide_index=True)
        else:
            aviso("No se encontraron filas PDOT en DATA-BRECHA")
    else:
        aviso("No se pudo cargar la hoja DATA-BRECHA")

    st.markdown("---")
    st.markdown("#### ⚡ Top 5 Acciones Críticas POA 2025")
    st.dataframe(
        pd.DataFrame({
            "#": ["#1 🔴", "#2 🔴", "#3 🟠", "#4 🟠", "#5 🟡"],
            "Meta PDOT": [
                "PDOT.SC.OE2.M1.01 — Centro de Salud Tipo C",
                "PDOT.AS.OE1.M2.02 — Nuevo Camal Municipal",
                "PDOT.AS.OE1.M2.01 — Terminal Terrestre",
                "PDOT.AM.OE3.M2.01 — Relleno Sanitario",
                "PDOT.AS.OE1.M1.03 — Reservorios de Agua",
            ],
            "Δ ICPI": ["+20.6 pp", "+5.2 pp", "+4.5 pp", "+3.2 pp", "+2.1 pp"],
            "Acción POA 2025": [
                "Convenio MSP con cronograma + LOTAIP cédulas",
                "Informe viabilidad técnica + partida presupuestaria",
                "Estudios factibilidad — elevar Ti 0.40 → 0.70",
                "Proceso MAATE; estudio de impacto ambiental",
                "Diseño definitivo; financiamiento BDE Agua Segura",
            ],
            "Plazo / Responsable": [
                "Q1-2025 · Dir. Gestión Social",
                "Q1-2025 · Dir. Planificación",
                "Q2-2025 · Proyectos Estratégicos",
                "Q2-2025 · Empresa de Aseo",
                "Q2-2025 · Dir. Agua Potable",
            ],
        }),
        use_container_width=True, hide_index=True,
    )


# ═══════════════════════════════════════════════════════════════
# TAB 5 · TRANSPARENCIA ITAM
# DATA-ITAM skip=4
# Resumen en filas 0-1; matriz PDOT: buscar fila con "COD-META (PDOT)"
# Encabezados de la matriz: COD-META (PDOT), EJE ESTRATÉGICO,
#   ÁREA TEMÁTICA, DIRECCIÓN RESPONSABLE (← C-MAO),
#   Lit. k PLANES (S1+S2), Lit. i CONTRATOS (S3-PAC),
#   Lit. g PRESUPUESTO (S4-CÉD.), Lit. m METAS/RDC (S5+S6),
#   Lit. d ENCUESTA (MANUAL), TOTAL LIT. CUMPL., ITAM (%), SEMÁFORO TRANSP.
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.subheader("🌐 Índice de Transparencia y Acceso a la Información (ITAM)")
    st.caption("Fuente: DATA-ITAM · Base: LOTAIP Art.7 · 20 metas × 5 literales")

    ci1, ci2, ci3 = st.columns(3)
    ci1.metric("ITAM Global", "78%", "🟡 Parcialmente Opaco")
    ci2.metric("Metas ITAM = 100%", "5 de 20", "🟢 Transparentes")
    ci3.metric("Literal más incumplido", "i — Contratos", "10/20 metas")

    st.markdown("---")

    lit_df = pd.DataFrame({
        "Literal": [
            "k · Planes institucionales",
            "i · Contratos SERCOP",
            "g · Presupuesto devengado",
            "m · Metas PDOT / RDC",
            "d · Encuesta satisfacción",
        ],
        "Metas que cumplen": [19, 10, 17, 19, 13],
        "Cumplimiento (%)": [95, 50, 85, 95, 65],
        "Semáforo": ["🟢 Alto", "🔴 Crítico", "🟢 Alto", "🟢 Alto", "🟡 Parcial"],
    })
    clg, clt = st.columns([2, 3])
    with clg:
        st.markdown("**Cumplimiento por Literal LOTAIP Art.7 (%)**")
        st.bar_chart(
            lit_df.set_index("Literal")["Cumplimiento (%)"],
            height=240, use_container_width=True,
        )
    with clt:
        st.markdown("**Tabla por Literal**")
        st.dataframe(
            lit_df[["Literal", "Metas que cumplen", "Cumplimiento (%)", "Semáforo"]],
            use_container_width=True, hide_index=True,
        )

    st.markdown("---")
    st.markdown("#### 📋 Matriz ITAM por meta (DATA-ITAM)")

    df_itam = cargar_hoja("DATA-ITAM", skiprows=4, nrows=28)

    if df_itam is not None:
        # Buscar la fila que contiene "COD-META (PDOT)" — ese es el header de la matriz
        header_idx = None
        for i, row in df_itam.iterrows():
            if "COD-META" in str(row.iloc[0]).upper():
                header_idx = i
                break

        if header_idx is not None:
            new_hdrs = [str(h).strip() for h in df_itam.iloc[header_idx].tolist()]
            df_matrix = df_itam.iloc[header_idx + 1:].copy()
            df_matrix.columns = new_hdrs
            df_matrix = df_matrix.reset_index(drop=True)

            df_pdot = df_matrix[
                df_matrix.iloc[:, 0].astype(str).str.contains("PDOT", na=False)
            ].copy()

            if not df_pdot.empty:
                cols_it = [
                    "COD-META (PDOT)", "EJE ESTRATÉGICO", "ÁREA TEMÁTICA",
                    "Lit. k PLANES (S1+S2)", "Lit. i CONTRATOS (S3-PAC)",
                    "Lit. g PRESUPUESTO (S4-CÉD.)", "Lit. m METAS/RDC (S5+S6)",
                    "Lit. d ENCUESTA (MANUAL)", "TOTAL LIT. CUMPL.",
                    "ITAM (%)", "SEMÁFORO TRANSP.",
                ]
                cols_ok = [c for c in cols_it if c in df_pdot.columns]
                st.dataframe(
                    df_pdot[cols_ok].reset_index(drop=True),
                    use_container_width=True, hide_index=True,
                )
            else:
                aviso("No se encontraron filas PDOT en la matriz DATA-ITAM")
        else:
            aviso("No se encontró el encabezado de la matriz en DATA-ITAM")
    else:
        aviso("No se pudo cargar la hoja DATA-ITAM")


# ═══════════════════════════════════════════════════════════════
# TAB 6 · PROSPECTIVA M7
# M7-PROSP skip=4
# Encabezados verificados (col1=CÓD. PDOT):
#   #, CÓD. PDOT, Ti ACTUAL, Vi, BRECHA Ti, RIESGO, CONSISTENCIA, DIAGNÓSTICO
# ═══════════════════════════════════════════════════════════════
with tab6:
    st.subheader("🔭 Análisis Prospectivo — Proyección 2025 (M7)")
    st.caption(
        "Fuente: M7-PROSP · Diagnóstico de brecha Ti y riesgo de incumplimiento al cierre 2027"
    )

    df_m7 = cargar_hoja("M7-PROSP", skiprows=4, nrows=25)

    if df_m7 is not None:
        # Con skip=4, fila 0 ya son encabezados (verificado)
        # Los datos PDOT están en la col1 (CÓD. PDOT)
        col_pdot = None
        for col in df_m7.columns:
            if df_m7[col].astype(str).str.contains("PDOT", na=False).any():
                col_pdot = col
                break

        if col_pdot is not None:
            df_m7_pdot = df_m7[
                df_m7[col_pdot].astype(str).str.contains("PDOT", na=False)
            ].copy().reset_index(drop=True)

            cols_m7 = [
                "CÓD. PDOT", "Ti ACTUAL", "Vi", "BRECHA Ti",
                "RIESGO", "CONSISTENCIA", "DIAGNÓSTICO",
            ]
            cols_ok = [c for c in cols_m7 if c in df_m7_pdot.columns]
            if cols_ok:
                st.dataframe(
                    df_m7_pdot[cols_ok], use_container_width=True, hide_index=True
                )
            else:
                st.dataframe(df_m7_pdot, use_container_width=True, hide_index=True)
        else:
            aviso("No se encontraron filas PDOT en M7-PROSP")
    else:
        aviso("No se pudo cargar la hoja M7-PROSP")

    st.markdown("---")
    st.markdown("#### 🚦 Clasificación de Riesgo Prospectivo")
    st.dataframe(
        pd.DataFrame({
            "Nivel": ["🔴 CRÍTICA", "🟠 GRAVE", "🟡 MODERADA", "🟢 MÍNIMA"],
            "Descripción": [
                "Vi=0, Ti=0 · Sin cadena documental ni ejecución",
                "Ti < 0.30 · Brecha > 0.70 al cierre 2027",
                "Ti 0.30–0.60 · Requiere aceleración POA 2025",
                "Ti > 0.60 · En trayectoria aceptable",
            ],
            "Metas afectadas": ["3", "4", "6", "7"],
        }),
        use_container_width=True, hide_index=True,
    )


# ═══════════════════════════════════════════════════════════════
# TAB 7 · RESULTADOS CONSOLIDADOS
# ═══════════════════════════════════════════════════════════════
with tab7:
    st.subheader("📋 Resultados Consolidados del Sistema SIAP-ICPI")
    st.caption("Dictamen final de auditoría forense — GAD Municipal de Montecristi")

    st.dataframe(
        pd.DataFrame({
            "MÉTRICA": [
                "ICPI Global Forense",
                "Categoría Semáforo AVEP",
                "Brecha ICPI vs Meta PDOT 2027",
                "ICM SIGAD 2023 (auto-reporte)",
                "Diferencial Forense (H₁)",
                "Metas Vi=1 — con soporte documental",
                "Metas Vi=0 — sin soporte documental",
                "ICPI Potencial Máximo (SOC-02 Vi→1)",
                "ITAM — Transparencia LOTAIP",
            ],
            "VALOR": [
                "38.28%",
                "Transición Crítica 🟡",
                "−53.97 pp",
                "92.25%",
                "+53.97 pp (H₁ Confirmada §3.1)",
                "8 / 20  (40%)",
                "12 / 20  (60%)",
                "67.64%  (Δ +20.6 pp posible)",
                "78%  —  Parcialmente Opaco",
            ],
            "FUENTE / INTERPRETACIÓN": [
                "Σ(Pi×Ri×Vi×Ti×Ci) ÷ Σ(Pi×Ri) · Motor M5-ICPI",
                "Escala: ≥90 Excelencia · ≥70 Satisfactorio · ≥40 Transición · ≥20 Ocurrencia",
                "Brecha vs Meta PDOT Plan Bicentenario §3.6",
                "Auto-reporte SIGAD — sobrestimación de 53.97 pp",
                "ICPI forense vs ICM declarado — confirma H₁ §3.1",
                "Vi_cadena=1: CININ 6 silos completos verificados",
                "Vi_cadena=0: sin cadena — Camal y CIBV son brechas críticas",
                "Si SOC-02 activa Vi=1, Ti=1 · Pi=0.20, Ri=1.5 · mayor impacto",
                "Literal más incumplido: i (Contratos) — 10/20 metas publicadas",
            ],
        }),
        use_container_width=True, hide_index=True,
    )

    st.markdown("---")
    csa, csb = st.columns(2)
    with csa:
        st.markdown("#### 🚦 Semáforo de Continuidad PDOT (n=20)")
        st.dataframe(
            pd.DataFrame({
                "Categoría": [
                    "✅ 🟢 ALINEADAS",
                    "⚠️ 🟡 PARCIALES",
                    "🔴 BAJA CONTINUIDAD",
                    "⬛ RUPTURA",
                ],
                "N° · %": ["10 · 50%", "7 · 35%", "3 · 15%", "0 · 0%"],
                "Descripción": [
                    "Vi=1, PAC ejecutado — continuidad asegurada",
                    "Vi=1 pero Ti bajo — activar POA 2025",
                    "Vi=0, sin proyecto explícito en PDOT",
                    "Sin evidencia ni presupuesto",
                ],
            }),
            use_container_width=True, hide_index=True,
        )
    with csb:
        st.markdown("#### 📖 Escala AVEP")
        st.dataframe(
            pd.DataFrame({
                "Rango ICPI": ["≥ 90%", "70% – 89%", "40% – 69%", "20% – 39%", "< 20%"],
                "Categoría": [
                    "Excelencia Institucional",
                    "Satisfactorio",
                    "Transición Crítica 🟡  ← GAD Montecristi",
                    "Gestión por Ocurrencia",
                    "Ruptura Institucional",
                ],
            }),
            use_container_width=True, hide_index=True,
        )


# ═══════════════════════════════════════════════════════
# PIE DE PÁGINA
# ═══════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#9aa5b4;font-size:0.77rem;padding:6px 0'>"
    "QUADRUM v1.0 &nbsp;·&nbsp; Sistema SIAP-ICPI &nbsp;·&nbsp; Protocolo ALFARO VIRTUS "
    "&nbsp;·&nbsp; GAD Municipal de Montecristi &nbsp;·&nbsp; Tesis de Grado 2025 "
    "&nbsp;·&nbsp; Datos: PDOT Plan Bicentenario 2023-2027 · eSIGEF · SERCOP · SIGAD · LOTAIP"
    "</div>",
    unsafe_allow_html=True,
)
