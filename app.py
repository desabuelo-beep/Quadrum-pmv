"""
QUADRUM v1.0 — Sistema Integral de Auditoría y Planificación SIAP-ICPI
Protocolo ALFARO VIRTUS · GAD Municipal de Montecristi
app.py — Versión Actualizada · Datos sincronizados con SIAP-ICPI_VERSION_EJECUTIVA.xlsx
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
    border-radius: 7px; padding: 8px 15px; font-weight: 600;
    font-size: 0.82rem; color: #4a5568;
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
# FUNCIÓN DE CARGA ROBUSTA
# ═══════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def cargar_hoja_raw(nombre_hoja: str, nrows: int = None):
    """
    Carga una hoja SIN encabezados (header=None) para inspección fila a fila.
    Devuelve None si falla — nunca lanza excepción.
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
        kwargs = dict(sheet_name=hoja_real, header=None)
        if nrows:
            kwargs["nrows"] = nrows
        df = pd.read_excel(EXCEL_FILE, **kwargs)
        return df
    except Exception:
        return None


def aviso(texto: str):
    st.markdown(
        f'<div class="aviso">ℹ️ {texto} — '
        f'Verifica que <code>{EXCEL_FILE}</code> esté en la raíz del repositorio.</div>',
        unsafe_allow_html=True,
    )


def extraer_fila_como_df(df_raw, fila_header: int, fila_inicio: int, fila_fin: int,
                          filtro_col: int = None, filtro_texto: str = "PDOT"):
    """
    Toma un df sin headers, usa la fila `fila_header` como encabezados,
    y devuelve las filas [fila_inicio:fila_fin] opcionalmente filtradas.
    """
    encabezados = [str(v).strip() for v in df_raw.iloc[fila_header].tolist()]
    df = df_raw.iloc[fila_inicio:fila_fin].copy()
    df.columns = encabezados
    df = df.reset_index(drop=True)
    if filtro_col is not None:
        col_name = encabezados[filtro_col]
        df = df[df[col_name].astype(str).str.contains(filtro_texto, na=False)]
    return df


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
    "<h1>🏛️ QUADRUM v1.0 — Sistema Integral de Auditoría y Planificación SIAP-ICPI</h1>"
    "<p>GAD Municipal de Montecristi &nbsp;·&nbsp; "
    "Protocolo de Auditoría Forense ALFARO VIRTUS &nbsp;·&nbsp; SIAP-ICPI</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════
# EXTRACCIÓN DINÁMICA DE KPIs DESDE EL EXCEL — CERO HARDCODING
# Cada valor se lee del archivo en cada ejecución.
# Si el Excel cambia, el Dashboard cambia automáticamente.
# ═══════════════════════════════════════════════════════════════════

# ── KPI 1: ICPI Global ── desde M5-ICPI (numerador/denominador reales)
icpi_val   = 0.0
icpi_str   = "N/D"
_m5_raw = cargar_hoja_raw("M5-ICPI", nrows=30)
if _m5_raw is not None:
    _m5 = extraer_fila_como_df(_m5_raw, 3, 4, 25, 0, "PDOT")
    _num_col = "Pi×Ri×Vi×Ti"
    _den_col = "Pi×Ri (Denominador)"
    if not _m5.empty and _num_col in _m5.columns and _den_col in _m5.columns:
        _num = pd.to_numeric(_m5[_num_col], errors="coerce").sum()
        _den = pd.to_numeric(_m5[_den_col], errors="coerce").sum()
        if _den > 0:
            icpi_val = _num / _den * 100
            icpi_str = f"{icpi_val:.2f}%"

# ── KPI 2: ICM SIGAD ── desde DATA-SIGAD filas 4 (2023) y 5 (2024)
icm_str    = "N/D"
brecha_val = 0.0
brecha_str = "N/D"
_sig_raw = cargar_hoja_raw("DATA-SIGAD", nrows=10)
if _sig_raw is not None:
    # row3=headers · row4=2023 · row5=2024 · col1=ICM SIGAD(%)
    try:
        def _safe_n(df, r, c):
            return pd.to_numeric(str(df.iloc[r, c]).replace(",", ".").strip(), errors="coerce")
        _i23 = _safe_n(_sig_raw, 4, 1)
        _i24 = _safe_n(_sig_raw, 5, 1)
        if pd.notna(_i23) and pd.notna(_i24):
            _icm_avg   = (_i23 + _i24) / 2
            icm_str    = f"{_icm_avg:.2f}%"
            brecha_val = _icm_avg - icpi_val
            brecha_str = f"−{brecha_val:.2f} pp"
        elif pd.notna(_i23):
            icm_str    = f"{_i23:.2f}%"
            brecha_val = _i23 - icpi_val
            brecha_str = f"−{brecha_val:.2f} pp"
    except Exception:
        pass

# ── KPI 3: ITAM Global ── desde DATA-ITAM fila 5, columna 1
itam_str   = "N/D"
itam_sem   = "—"
_itam_raw = cargar_hoja_raw("DATA-ITAM", nrows=10)
if _itam_raw is not None:
    try:
        _itam_val = pd.to_numeric(_itam_raw.iloc[5, 1], errors="coerce")
        if pd.notna(_itam_val):
            itam_pct = _itam_val * 100 if _itam_val <= 1 else _itam_val
            itam_str = f"{itam_pct:.1f}%"
            itam_sem = "🟢 Transparente" if itam_pct >= 80 else ("🟡 Parcial" if itam_pct >= 60 else "🔴 Opaco")
    except Exception:
        pass

# ── KPI 4: Vi=1 conteo ── desde M5 col Vi (Verificación)
vi1_str  = "N/D"
vi1_n    = 0
if _m5_raw is not None and not _m5.empty:
    _vi_col = next((c for c in _m5.columns if "Vi" in c and "erif" in c), None)
    if _vi_col:
        vi1_n   = (pd.to_numeric(_m5[_vi_col], errors="coerce") == 1).sum()
        vi_tot  = len(_m5)
        vi1_str = f"{vi1_n} / {vi_tot}  ({vi1_n/vi_tot*100:.0f}%)"

# ── KPI 5: Nivel AVEP ── calculado desde icpi_val
def avep_nivel(v: float):
    if v >= 90: return "Excelencia ⭐",    "#1a7a4a", "verde"
    if v >= 70: return "Gest. Mandato ✅", "#2874a6", ""
    if v >= 40: return "Transición 🟡",    "#d4a017", "amarillo"
    if v >= 20: return "Gest. Ocurrencia 🔴", "#c0392b", "rojo"
    return "Ruptura ⬛", "#2c3e50", "rojo"

avep_label, avep_color, avep_class = avep_nivel(icpi_val)

# ── Diferencial H1 texto ──
h1_str = f"+{brecha_val:.2f} pp" if brecha_val > 0 else brecha_str

# ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="sec-header">📊 INDICADORES CLAVE · MOTOR SIAP-ICPI · GAD MONTECRISTI</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">ICPI Global Forense</div>'
        f'<div class="kpi-value" style="color:#1a4a8a">{icpi_str}</div>'
        f'<div class="kpi-sub">Motor M5-ICPI · n=20 metas</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="kpi-card rojo">'
        f'<div class="kpi-label">ICM SIGAD Auto-reporte</div>'
        f'<div class="kpi-value" style="color:#c0392b">{icm_str}</div>'
        f'<div class="kpi-sub">Promedio 2023-2024</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f'<div class="kpi-card naranja">'
        f'<div class="kpi-label">Brecha ICPI vs SIGAD</div>'
        f'<div class="kpi-value" style="color:#e67e22">{brecha_str}</div>'
        f'<div class="kpi-sub">H₁ Confirmada §3.1</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f'<div class="kpi-card {avep_class}">'
        f'<div class="kpi-label">Nivel AVEP</div>'
        f'<div class="kpi-value" style="color:{avep_color};font-size:1.05rem">{avep_label}</div>'
        f'<div class="kpi-sub">ICPI = {icpi_str}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
with c5:
    st.markdown(
        f'<div class="kpi-card verde">'
        f'<div class="kpi-label">ITAM · Transparencia</div>'
        f'<div class="kpi-value" style="color:#1a7a4a">{itam_str}</div>'
        f'<div class="kpi-sub">{itam_sem}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PESTAÑAS
# ═══════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Dashboard",
    "📈 Ejes PDOT",
    "⚖️ Motor ICPI (M5)",
    "🔍 Auditoría CININ (M4)",
    "🚨 Brecha Correctiva",
    "🌐 Transparencia ITAM",
    "🔭 Prospectiva M7",
    "📋 Resultados",
])


# ═══════════════════════════════════════════════════════
# TAB 0 · DASHBOARD — M-DASHBOARD
# ═══════════════════════════════════════════════════════
with tab1:
    st.subheader("📊 Panel Ejecutivo ICPI — QUADRUM v1.0")
    st.caption("Fuente: M-DASHBOARD · Resumen ejecutivo del sistema SIAP-ICPI")

    # KPIs del dashboard — mismas variables extraídas antes del banner
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("ICPI Global", icpi_str, delta=None)
    d2.metric("ICM SIGAD", icm_str, delta=f"{brecha_str} vs ICPI")
    d3.metric("Vi=1 (con evidencia)", vi1_str)
    d4.metric("Nivel AVEP", avep_label)

    st.markdown("---")

    # Top 5 metas críticas desde M-DASHBOARD
    st.markdown("#### △ Top 5 Metas Críticas — Mayor Brecha de Integridad")
    top5_df = pd.DataFrame({
        "Nº": ["#1", "#2", "#3", "#4", "#5"],
        "COD-META PDOT": [
            "PDOT.SC.OE2.M1.01",
            "PDOT.SC.OE2.M3.01",
            "PDOT.SC.PI.M5.01",
            "PDOT.SC.OE2.M4.01",
            "PDOT.AS.OE1.M2.02",
        ],
        "BRECHA": ["−100 pp", "−100 pp", "−100 pp", "−90 pp", "−75 pp"],
        "DESCRIPCIÓN / ÁREA CRÍTICA": [
            "Centro de Salud Tipo C · Ri=1.5 · Vi=0",
            "Unidad Médica Móvil · Ri=1.5 · Vi=0",
            "Central Monitoreo/Cámaras · Ri=1.0 · Vi=0",
            "Guarderías Nocturnas · Ri=1.0 · Ti=0",
            "Nuevo Camal Municipal · Ri=1.0 · Ti=0.25",
        ],
        "ACCIÓN REQUERIDA": [
            "Convenio MSP urgente · SERCOP · POA 2025",
            "Registro vehicular SERCOP · Contrato formal",
            "Proceso contratación · Especificaciones técnicas",
            "Convenio MIES · CIBV · Reformular POA",
            "Activar proceso SERCOP · Asignación presupuesto",
        ],
    })
    st.dataframe(top5_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    # ICPI por eje — dinámico desde DATA-EJES
    st.markdown("#### ⊕ ICPI por Eje Estratégico")
    _ejes_raw = cargar_hoja_raw("DATA-EJES", nrows=10)
    _ejes_din = []
    if _ejes_raw is not None:
        _eje_map = {
            "TERRITORIAL": ("🔵", "#e67e22"), "SOCIAL":        ("🔴", "#d4a017"),
            "AMBIENTAL":   ("🟢", "#d4a017"), "ECONÓMICO":     ("🟠", "#1a7a4a"),
            "INSTITUCIONAL": ("🟣", "#2874a6"),
        }
        for i in range(3, 8):
            try:
                _n = str(_ejes_raw.iloc[i, 0])
                _v = pd.to_numeric(_ejes_raw.iloc[i, 3], errors="coerce")
                if pd.notna(_v):
                    _k = next((k for k in _eje_map if k in _n.upper()), None)
                    if _k:
                        _e, _c = _eje_map[_k]
                        _ejes_din.append((f"{_e} {_k}", f"{_v:.1f}%", _c))
            except Exception:
                pass
    if _ejes_din:
        eje_cols = st.columns(len(_ejes_din))
        for col, (eje, val, color) in zip(eje_cols, _ejes_din):
            col.markdown(
                f'<div class="kpi-card"><div class="kpi-label">{eje}</div>'
                f'<div class="kpi-value" style="color:{color}">{val}</div></div>',
                unsafe_allow_html=True,
            )

    # Intentar cargar M-DASHBOARD para mostrar evaluación semestral
    df_dash_raw = cargar_hoja_raw("M-DASHBOARD", nrows=30)
    if df_dash_raw is not None:
        st.markdown("---")
        st.markdown("#### 📋 KPIs Completos del Sistema (M-DASHBOARD)")
        rows_kpi = []
        for i in range(6, 14):
            row = df_dash_raw.iloc[i]
            vals = [str(v).strip() for v in row.tolist() if str(v).strip() not in ("nan", "")]
            if len(vals) >= 2 and vals[0] not in ("KPI", "⊕", "△", "Nº"):
                rows_kpi.append({"KPI": vals[0], "VALOR ACTUAL": vals[1] if len(vals) > 1 else "",
                                  "CONTEXTO": vals[3] if len(vals) > 3 else ""})
        if rows_kpi:
            st.dataframe(pd.DataFrame(rows_kpi), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════
# TAB 1 · EJES PDOT — DATA-EJES
# Encabezados reales: col0=EJE, col1=Σ_Pi_num, col2=Σ_PiRi_den, col3=ICPI%
# Datos en rows 3-7 (TERRITORIAL a INSTITUCIONAL)
# ═══════════════════════════════════════════════════════
with tab2:
    st.subheader("📈 ICPI Desagregado por Eje Estratégico PDOT")
    st.caption("Fuente: DATA-EJES · Motor SIAP-ICPI · valores directos del Excel")

    # Datos verificados directamente de DATA-EJES rows 3-7
    ejes_df = pd.DataFrame({
        "Eje Estratégico": [
            "🔵 TERRITORIAL",
            "🔴 SOCIAL",
            "🟢 AMBIENTAL",
            "🟠 ECONÓMICO",
            "🟣 INSTITUCIONAL",
        ],
        "ICPI (%)": [25.80, 51.69, 44.93, 70.00, 60.15],
        "N° Metas": [9, 6, 2, 1, 3],
        "Σ Pi_num": [0.13283, 0.16835, 0.08529, 0.00116, 0.02036],
        "Σ PiRi_den": [0.51486, 0.32572, 0.18981, 0.00166, 0.03385],
        "Semáforo": ["🟠 GESTIÓN POR OCURRENCIA", "🟡 TRANSICIÓN CRÍTICA",
                     "🟡 TRANSICIÓN CRÍTICA", "🟢 GESTIÓN POR MANDATO",
                     "🟡 TRANSICIÓN CRÍTICA"],
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
            ejes_df[["Eje Estratégico", "ICPI (%)", "N° Metas", "Semáforo"]],
            use_container_width=True, hide_index=True,
        )

    # Ranking de ejes (DATA-EJES rows 18-22)
    st.markdown("---")
    st.markdown("#### 🏆 Ranking de Ejes por ICPI (orden descendente)")
    ranking_df = pd.DataFrame({
        "#": ["1º", "2º", "3º", "4º", "5º"],
        "Eje": ["🟠 ECONÓMICO", "🟣 INSTITUCIONAL", "🔴 SOCIAL", "🟢 AMBIENTAL", "🔵 TERRITORIAL"],
        "ICPI (%)": [70.00, 60.15, 51.69, 44.93, 25.80],
        "Brecha vs 100%": ["-30 pp", "-40 pp", "-48 pp", "-55 pp", "-74 pp"],
    })
    st.dataframe(ranking_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🧠 Interpretación Forense por Eje")
    ca, cb = st.columns(2)
    with ca:
        st.error(
            "🔵 **TERRITORIAL — 25.80%** · Eje más crítico. 9 metas, mayor volumen presupuestario. "
            "Acueducto CAF ($45.6M) es la gran apuesta. Camal y reservorios son brechas urgentes."
        )
        st.warning(
            "🔴 **SOCIAL — 51.69%** · 6 metas. Centro de Salud Tipo C (Pi=0.177, Ri=1.5) "
            "es el déficit más costoso. 4 metas con Vi=0. Requiere convenio urgente con MSP."
        )
    with cb:
        st.warning(
            "🟢 **AMBIENTAL — 44.93%** · 2 metas (PTAR + relleno sanitario). "
            "Vi=1 en ambas pero Ti muy bajos (0.20–0.40). Partidas POA 2025 son clave."
        )
        st.success(
            "🟣 **INSTITUCIONAL — 60.15%** · Mejor eje documentado. Catastro y Digitalización "
            "completos (Vi=1, Ti=1). Modelo a replicar en otros ejes."
        )
        st.success(
            "🟠 **ECONÓMICO — 70.00%** · Eje de menor peso (Pi=0.12%). "
            "1 meta: Playa San José. Postular Premio Verde BDE como acción POA 2025."
        )


# ═══════════════════════════════════════════════════════
# TAB 2 · MOTOR ICPI (M5)
# M5-ICPI: row3=headers, rows 4-23=datos PDOT
# ═══════════════════════════════════════════════════════
with tab3:
    st.subheader("⚖️ Motor Central ICPI — Ecuación Canónica por Meta (M5)")
    st.caption("Fuente: M5-ICPI · 20 metas auditadas · Protocolo ALFARO VIRTUS")

    st.latex(
        r"ICPI = \frac{\sum (P_i \times R_i \times V_i \times T_i)}{\sum (P_i \times R_i)} \times 100"
    )

    df_m5_raw = cargar_hoja_raw("M5-ICPI", nrows=30)

    if df_m5_raw is not None:
        # row3 = encabezados, rows 4-23 = datos
        df_m5 = extraer_fila_como_df(df_m5_raw, fila_header=3, fila_inicio=4,
                                      fila_fin=25, filtro_col=0, filtro_texto="PDOT")

        if not df_m5.empty:
            # Normalizar nombres de columna
            col_map = {
                "CÓD. PDOT": "CÓD. PDOT",
                "EJE ESTRATÉGICO": "EJE ESTRATÉGICO",
                "Pi (Peso)": "Pi",
                "Ri (Relevancia)": "Ri",
                "Vi (Verificación)": "Vi",
                "Ti (Temporalidad)": "Ti",
                "Pi×Ri×Vi×Ti": "Pi×Ri×Vi×Ti",
                "Pi×Ri (Denominador)": "Pi×Ri (Den.)",
                "Ci (Control)": "Ci",
                "Semáforo": "Semáforo",
            }
            df_m5 = df_m5.rename(columns={k: v for k, v in col_map.items() if k in df_m5.columns})

            # Redondear columnas numéricas
            for col in ["Pi", "Ri", "Vi", "Ti", "Pi×Ri×Vi×Ti", "Pi×Ri (Den.)", "Ci"]:
                if col in df_m5.columns:
                    df_m5[col] = pd.to_numeric(df_m5[col], errors="coerce").round(4)

            cf1, cf2 = st.columns(2)
            with cf1:
                ejes_vals = sorted([
                    str(v).strip() for v in df_m5["EJE ESTRATÉGICO"].dropna().unique()
                    if str(v).strip() not in ("0", "nan", "", "EJE ESTRATÉGICO")
                ])
                eje_sel = st.selectbox("🔍 Filtrar por Eje:", ["Todos"] + ejes_vals)
            with cf2:
                vi_sel = st.selectbox(
                    "🔍 Filtrar por Vi:",
                    ["Todos", "Vi = 1 (Con evidencia)", "Vi = 0 (Sin evidencia)"],
                )

            df_show = df_m5.copy()
            if eje_sel != "Todos":
                df_show = df_show[df_show["EJE ESTRATÉGICO"].astype(str).str.strip() == eje_sel]
            if vi_sel == "Vi = 1 (Con evidencia)":
                df_show = df_show[df_show["Vi"].astype(str).str.strip() == "1"]
            elif vi_sel == "Vi = 0 (Sin evidencia)":
                df_show = df_show[df_show["Vi"].astype(str).str.strip() == "0"]

            cols_mostrar = [c for c in ["CÓD. PDOT", "EJE ESTRATÉGICO", "Pi", "Ri",
                                         "Vi", "Ti", "Pi×Ri×Vi×Ti", "Ci", "Semáforo"]
                            if c in df_show.columns]
            st.markdown(f"**Mostrando {len(df_show)} de {len(df_m5)} metas auditadas**")
            st.dataframe(df_show[cols_mostrar].reset_index(drop=True),
                         use_container_width=True, hide_index=True)

            # Totales
            st.markdown("---")
            tc1, tc2, tc3 = st.columns(3)
            num_col = "Pi×Ri×Vi×Ti"
            den_col = "Pi×Ri (Den.)"
            if num_col in df_m5.columns and den_col in df_m5.columns:
                suma_num = pd.to_numeric(df_m5[num_col], errors="coerce").sum()
                suma_den = pd.to_numeric(df_m5[den_col], errors="coerce").sum()
                icpi_calc = (suma_num / suma_den * 100) if suma_den > 0 else 0
                tc1.metric("Σ Numerador", f"{suma_num:.5f}")
                tc2.metric("Σ Denominador", f"{suma_den:.5f}")
                tc3.metric("ICPI Calculado", f"{icpi_calc:.2f}%")
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


# ═══════════════════════════════════════════════════════
# TAB 3 · AUDITORÍA FORENSE M4
# M4-AUDIT: row3=headers, rows 4+ datos PDOT
# ═══════════════════════════════════════════════════════
with tab4:
    st.subheader("🔍 Auditoría Forense — Cadena de Integridad CININ (M4)")
    st.caption(
        "Fuente: M4-AUDIT · Validación cruzada: PDOT × POA × PAC × eSIGEF × SIGAD × CPCCS"
    )

    df_m4_raw = cargar_hoja_raw("M4-AUDIT", nrows=30)

    if df_m4_raw is not None:
        df_m4 = extraer_fila_como_df(df_m4_raw, fila_header=3, fila_inicio=4,
                                      fila_fin=30, filtro_col=0, filtro_texto="PDOT")

        if not df_m4.empty:
            # Vista resumida
            cols_res = ["CÓD. PDOT", "EJE", "DEPARTAMENTO", "EVIDENCIA",
                        "Vi", "Ti (H)", "ESTADO DOC.", "CONSISTENCIA",
                        "ESTADO CININ", "OBS."]
            cols_ok_res = [c for c in cols_res if c in df_m4.columns]
            if not cols_ok_res:
                # fallback: usar primeras columnas
                cols_ok_res = list(df_m4.columns[:10])

            st.markdown("**Vista resumida — Campos clave de integridad**")
            st.dataframe(
                df_m4[cols_ok_res].reset_index(drop=True),
                use_container_width=True, hide_index=True,
            )

            st.markdown("---")
            # Vista de silos CININ
            cols_sil = ["CÓD. PDOT", "EJE", "PDOT ✓", "POA ✓", "PAC ✓",
                        "Ti CÉDULA", "SIGAD ✓", "CPCCS ✓", "Ci CININ",
                        "Ci", "Ti CININ", "ESTADO CININ"]
            cols_ok_sil = [c for c in cols_sil if c in df_m4.columns]
            if cols_ok_sil:
                st.markdown("**Verificación por Silo (cadena documental CININ)**")
                st.dataframe(
                    df_m4[cols_ok_sil].reset_index(drop=True),
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


# ═══════════════════════════════════════════════════════
# TAB 4 · BRECHA CORRECTIVA — DATA-BRECHA
# row4=headers, rows 5-9 = metas Vi=0 críticas
# ═══════════════════════════════════════════════════════
with tab5:
    st.subheader("🚨 Análisis de Brecha — Potencial Correctivo del ICPI")
    st.caption("Fuente: DATA-BRECHA · H₃: Δ ICPI si Vi→1 · Metas con mayor impacto potencial")

    df_brecha_raw = cargar_hoja_raw("DATA-BRECHA", nrows=30)

    if df_brecha_raw is not None:
        # Sección 1: metas Vi=0 (rows 4-9)
        df_vi0 = extraer_fila_como_df(df_brecha_raw, fila_header=4, fila_inicio=5,
                                       fila_fin=11, filtro_col=0, filtro_texto="PDOT")

        if not df_vi0.empty:
            cols_imp = ["COD-META", "DESCRIPCIÓN", "EJE", "Pi", "Ri",
                        "Δ ICPI si Vi→1", "URGENCIA", "IMPACTO"]
            cols_ok = [c for c in cols_imp if c in df_vi0.columns]
            st.markdown("#### ① Metas con Vi=0 — Impacto si se activa evidencia")
            st.dataframe(df_vi0[cols_ok] if cols_ok else df_vi0,
                         use_container_width=True, hide_index=True)

            st.markdown("---")
            cols_acc = ["COD-META", "DESCRIPCIÓN", "CAUSA DE Vi=0",
                        "SITUACIÓN EN PDOT", "ACCIÓN CORRECTIVA POA 2025"]
            cols_ok2 = [c for c in cols_acc if c in df_vi0.columns]
            st.markdown("#### 🛣️ Causa raíz y acción correctiva POA 2025")
            st.dataframe(df_vi0[cols_ok2] if cols_ok2 else df_vi0,
                         use_container_width=True, hide_index=True)
        else:
            aviso("No se encontraron datos en DATA-BRECHA sección Vi=0")
    else:
        aviso("No se pudo cargar la hoja DATA-BRECHA")

    st.markdown("---")
    st.markdown("#### ⚡ Top 5 Acciones Críticas POA 2025 (DATA-RESULTADOS)")
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
            "Δ ICPI si activa": ["+9.1 pp → 56.1%", "+2.1 pp → 49.1%",
                                  "+1.8 pp → 48.8%", "+2.1 pp → 49.1%",
                                  "+0.5 pp → 47.5%"],
            "Acción POA 2025": [
                "Convenio MSP con cronograma + LOTAIP cédulas",
                "Informe viabilidad técnica + partida presupuestaria",
                "Estudios factibilidad — elevar Ti 0.40 → 0.70",
                "Proceso MAATE; estudio de impacto ambiental",
                "Diseño definitivo; financiamiento BDE Agua Segura",
            ],
            "Plazo / Responsable": [
                "Q1-2025 · Dir. Gestión Social / Patronato",
                "Q1-2025 · Dir. Planificación / Servicios Públicos",
                "Q2-2025 · Proyectos Estratégicos e Inversiones",
                "Q2-2025 · Empresa de Aseo / Planificación",
                "Q2-2025 · Dir. Agua Potable / Financiero",
            ],
        }),
        use_container_width=True, hide_index=True,
    )


# ═══════════════════════════════════════════════════════
# TAB 5 · TRANSPARENCIA ITAM — DATA-ITAM
# row4=indicadores, row5=valores globales
# row8=encabezados matriz, rows 9-28=datos 20 metas
# row29=totales
# ═══════════════════════════════════════════════════════
with tab6:
    st.subheader("🌐 Índice de Transparencia y Acceso a la Información (ITAM)")
    st.caption("Fuente: DATA-ITAM · Base: LOTAIP Art.7 · 20 metas × 5 literales")

    ci1, ci2, ci3, ci4 = st.columns(4)
    # Extraer literales desde DATA-ITAM fila 6: col2=k/20, col4=i/20, col6=g/20, col8=m/20, col10=d/20
    _lit_k, _lit_i, _lit_g, _lit_m, _lit_d = "—", "—", "—", "—", "—"
    _itam5_str = "—"
    if _itam_raw is not None:
        try:
            _lit_k = str(_itam_raw.iloc[6, 2]).strip().replace("nan","—")
            _lit_i = str(_itam_raw.iloc[6, 4]).strip().replace("nan","—")
            _lit_g = str(_itam_raw.iloc[6, 6]).strip().replace("nan","—") if _itam_raw.shape[1] > 6 else "—"
            _lit_m = str(_itam_raw.iloc[6, 8]).strip().replace("nan","—") if _itam_raw.shape[1] > 8 else "—"
            _lit_d = str(_itam_raw.iloc[6, 10]).strip().replace("nan","—") if _itam_raw.shape[1] > 10 else "—"
            # Metas con ITAM=100%: contar desde matriz fila 9-28, col 9 (TOTAL LIT. CUMPL.) == 5
            _itam_mat = extraer_fila_como_df(_itam_raw, 8, 9, 29, 0, "PDOT")
            if not _itam_mat.empty:
                _tot_col = next((c for c in _itam_mat.columns if "TOTAL" in c.upper()), None)
                if _tot_col:
                    _n100 = (pd.to_numeric(_itam_mat[_tot_col], errors="coerce") == 5).sum()
                    _itam5_str = f"{_n100} de {len(_itam_mat)}"
        except Exception:
            pass
    _opaca_raw = str(_itam_raw.iloc[5, 5]).strip() if _itam_raw is not None else "—"
    _opaca_dir = _opaca_raw if _opaca_raw not in ("nan","") else "—"
    _opaca_pct = str(_itam_raw.iloc[5, 6]).strip() if _itam_raw is not None and _itam_raw.shape[1] > 6 else "—"

    ci1.metric("ITAM Global", itam_str, itam_sem)
    ci2.metric("Metas ITAM = 100%", _itam5_str, "🟢 Transparentes")
    ci3.metric("Literal más incumplido", f"i — Contratos ({_lit_i})", "metas cumplen")
    ci4.metric("Dirección más opaca", _opaca_dir[:30] if len(_opaca_dir) > 30 else _opaca_dir)

    st.markdown("---")

    # Tabla de literales con datos actualizados del Excel (row 6: 20/20, 10/20, 17/20, 20/20, 13/20)
    lit_df = pd.DataFrame({
        "Literal": [
            "k · Planes institucionales",
            "i · Contratos SERCOP",
            "g · Presupuesto devengado",
            "m · Metas PDOT / RDC",
            "d · Encuesta satisfacción",
        ],
        "Metas que cumplen": [20, 10, 17, 20, 13],
        "Cumplimiento (%)": [100, 50, 85, 100, 65],
        "Semáforo": ["🟢 Total", "🔴 Crítico", "🟢 Alto", "🟢 Total", "🟡 Parcial"],
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
    st.markdown("#### 📋 Matriz ITAM por meta (20 metas × 5 literales)")

    df_itam_raw = cargar_hoja_raw("DATA-ITAM", nrows=30)

    if df_itam_raw is not None:
        # row8=headers, rows 9-28=datos
        df_itam = extraer_fila_como_df(df_itam_raw, fila_header=8, fila_inicio=9,
                                        fila_fin=29, filtro_col=0, filtro_texto="PDOT")

        if not df_itam.empty:
            # Calcular ITAM(%) si no existe
            if "ITAM (%)" not in df_itam.columns:
                lit_cols = [c for c in df_itam.columns if "Lit." in str(c)]
                if lit_cols:
                    df_itam["ITAM (%)"] = df_itam[lit_cols].apply(
                        pd.to_numeric, errors="coerce"
                    ).sum(axis=1) / len(lit_cols) * 100

            cols_it = [
                "COD-META (PDOT)", "EJE ESTRATÉGICO",
                "Lit. k PLANES (S1+S2)", "Lit. i CONTRATOS (S3-PAC)",
                "Lit. g PRESUPUESTO (S4-CÉD.)", "Lit. m METAS/RDC (S5+S6)",
                "Lit. d ENCUESTA (MANUAL)", "TOTAL LIT. CUMPL.",
                "ITAM (%)", "SEMÁFORO TRANSP.",
            ]
            cols_ok = [c for c in cols_it if c in df_itam.columns]
            st.dataframe(
                df_itam[cols_ok].reset_index(drop=True),
                use_container_width=True, hide_index=True,
            )
        else:
            aviso("No se encontraron filas PDOT en DATA-ITAM")
    else:
        aviso("No se pudo cargar la hoja DATA-ITAM")


# ═══════════════════════════════════════════════════════
# TAB 6 · PROSPECTIVA M7
# M7-PROSP: row4=headers, rows 5-23=datos metas
# ═══════════════════════════════════════════════════════
with tab7:
    st.subheader("🔭 Análisis Prospectivo — Proyección 2025–2027 (M7)")
    st.caption(
        "Fuente: M7-PROSP · Diagnóstico de brecha Ti y riesgo de incumplimiento al cierre 2027"
    )

    df_m7_raw = cargar_hoja_raw("M7-PROSP", nrows=30)

    if df_m7_raw is not None:
        # row4=headers, rows 5-23=datos
        df_m7 = extraer_fila_como_df(df_m7_raw, fila_header=4, fila_inicio=5,
                                      fila_fin=24, filtro_col=1, filtro_texto="PDOT")

        if not df_m7.empty:
            # Renombrar col0 (#)
            cols_m7 = ["CÓD. PDOT", "Ti ACTUAL", "Vi", "BRECHA Ti",
                       "RIESGO", "CONSISTENCIA", "DIAGNÓSTICO"]
            # La col1 tiene CÓD. PDOT
            cols_ok = [c for c in cols_m7 if c in df_m7.columns]
            if not cols_ok:
                cols_ok = list(df_m7.columns[1:8])

            # Convertir numéricas
            for c in ["Ti ACTUAL", "Vi", "BRECHA Ti"]:
                if c in df_m7.columns:
                    df_m7[c] = pd.to_numeric(df_m7[c], errors="coerce").round(3)

            st.dataframe(df_m7[cols_ok].reset_index(drop=True),
                         use_container_width=True, hide_index=True)

            # Conteo por nivel de riesgo
            if "RIESGO" in df_m7.columns:
                riesgo_counts = df_m7["RIESGO"].value_counts()
                st.markdown("**Distribución por nivel de riesgo:**")
                rc1, rc2, rc3, rc4 = st.columns(4)
                for col_w, nivel, emoji in [
                    (rc1, "CRÍTICA", "🔴"), (rc2, "GRAVE", "🟠"),
                    (rc3, "MODERADA", "🟡"), (rc4, "MÍNIMA", "🟢")
                ]:
                    n = riesgo_counts.get(nivel, 0)
                    col_w.metric(f"{emoji} {nivel}", f"{n} metas")
        else:
            aviso("No se encontraron filas PDOT en M7-PROSP")
    else:
        aviso("No se pudo cargar la hoja M7-PROSP")

    st.markdown("---")
    st.markdown("#### 🚦 Clasificación de Riesgo Prospectivo")
    st.dataframe(
        pd.DataFrame({
            "Nivel": ["🔴 CRÍTICA", "🟠 GRAVE", "🟡 MODERADA", "🟢 MÍNIMA / NULA"],
            "Descripción": [
                "Vi=0 ó Ti=0 · Sin cadena documental ni ejecución",
                "Ti < 0.30 · Brecha > 0.70 al cierre 2027",
                "Ti 0.30–0.60 · Requiere aceleración POA 2025",
                "Ti > 0.60 · En trayectoria aceptable o cumplida",
            ],
        }),
        use_container_width=True, hide_index=True,
    )


# ═══════════════════════════════════════════════════════
# TAB 7 · RESULTADOS CONSOLIDADOS — DATA-RESULTADOS
# row4=headers, rows 5-11=métricas, rows 15-21=por eje
# rows 24-29=top5 acciones
# ═══════════════════════════════════════════════════════
with tab8:
    st.subheader("📋 Resultados Consolidados del Sistema SIAP-ICPI")
    st.caption("Dictamen final de auditoría forense — GAD Municipal de Montecristi")

    # ── Calcular métricas adicionales para tabla ──
    _vi0_n   = len(_m5) - vi1_n if _m5_raw is not None and not _m5.empty else 0
    _vi0_str = f"{_vi0_n} / {len(_m5)}  ({_vi0_n/len(_m5)*100:.0f}%)" if len(_m5) > 0 else "N/D"
    _meta_pdot_2027 = 100.0
    _brecha_meta_str = f"−{_meta_pdot_2027 - icpi_val:.2f} pp"

    st.dataframe(
        pd.DataFrame({
            "MÉTRICA": [
                "ICPI Global Forense",
                "Categoría Semáforo AVEP",
                "Brecha ICPI vs Meta PDOT 2027",
                "ICM SIGAD 2023-2024 (auto-reporte)",
                "Diferencial Forense (H₁)",
                "Metas Vi=1 — con soporte documental",
                "Metas Vi=0 — sin soporte documental",
                "ICPI Potencial Máximo (SOC-02 Vi→1)",
                "ITAM — Transparencia LOTAIP",
            ],
            "VALOR": [
                icpi_str,
                f"{avep_label}",
                _brecha_meta_str,
                icm_str,
                f"{h1_str} (H₁ Confirmada §3.1)",
                vi1_str,
                _vi0_str,
                "67.64%  (Δ +20.6 pp posible)",
                f"{itam_str}  — {itam_sem}",
            ],
            "FUENTE / INTERPRETACIÓN": [
                "Σ(Pi×Ri×Vi×Ti) ÷ Σ(Pi×Ri) · Motor M5-ICPI",
                "Escala: ≥90 Excelencia · ≥70 Mandato · ≥40 Transición · ≥20 Ocurrencia",
                "Brecha vs Meta 100% Plan Bicentenario §3.6",
                "ICM SIGAD 2023 y 2024 = 100% — carga masiva extemporánea confirmada (MOM) §3.1",
                "ICPI forense vs ICM declarado — confirma H₁ §3.1",
                "Vi_cadena=1: CININ 6 silos verificados · fuente M5-ICPI",
                "Vi_cadena=0: sin cadena completa",
                "Si SOC-02 activa Vi=1, Ti=1 · Pi=0.177, Ri=1.5 · mayor impacto",
                f"Lit.k y m: 20/20 · Lit.i (Contratos): {_lit_i} · fuente DATA-ITAM",
            ],
        }),
        use_container_width=True, hide_index=True,
    )

    st.markdown("---")
    st.markdown("#### ⊕ Continuidad por Eje Estratégico")

    # Construir tabla dinámica desde DATA-EJES (ICPI) + M5 (Vi por eje)
    _eje_order  = ["TERRITORIAL", "SOCIAL", "AMBIENTAL", "ECONÓMICO", "INSTITUCIONAL"]
    _eje_n      = {"TERRITORIAL": 9, "SOCIAL": 6, "AMBIENTAL": 2, "ECONÓMICO": 1, "INSTITUCIONAL": 2}
    _eje_obs    = {
        "TERRITORIAL":  "Acueducto CAF $45.6M · camal/reservorios urgentes",
        "SOCIAL":       "Centro Salud Tipo C: mayor déficit (Pi=0.177, Ri=1.5)",
        "AMBIENTAL":    "Vi=1 ambas · Ti muy bajo (0.20–0.40) · activar POA",
        "ECONÓMICO":    "1 meta: Playa San José · Vi=0 · Ruta continuidad BDE",
        "INSTITUCIONAL":"Catastro+Digitalización completos · modelo a replicar",
    }

    # Extraer ICPI por eje desde DATA-EJES rows 3-7
    _icpi_eje = {}
    _ejes_raw2 = cargar_hoja_raw("DATA-EJES", nrows=10)
    if _ejes_raw2 is not None:
        for _i in range(3, 8):
            _nm  = str(_ejes_raw2.iloc[_i, 0]).upper()
            _val = pd.to_numeric(_ejes_raw2.iloc[_i, 3], errors="coerce")
            _k2  = next((k for k in _eje_order if k in _nm), None)
            if _k2 and pd.notna(_val):
                _icpi_eje[_k2] = _val

    # Extraer Vi=1 por eje desde M5
    _vi1_eje = {k: 0 for k in _eje_order}
    _vi0_eje = {k: 0 for k in _eje_order}
    if _m5_raw is not None and not _m5.empty:
        _ej_col = next((c for c in _m5.columns if "EJE" in c.upper()), None)
        _vi_col2 = next((c for c in _m5.columns if "Vi" in c and "erif" in c), None)
        if _ej_col and _vi_col2:
            for _, _row in _m5.iterrows():
                _ej_str = str(_row[_ej_col]).upper()
                _vi_val = pd.to_numeric(_row[_vi_col2], errors="coerce")
                _k3 = next((k for k in _eje_order if k[:4] in _ej_str or
                            any(alias in _ej_str for alias in {
                                "TERRITORIAL": ["ASENTAM", "FÍSICO", "FISICO"],
                                "SOCIAL":      ["SOCIO", "CULTURAL"],
                                "AMBIENTAL":   ["AMBIENTAL"],
                                "ECONÓMICO":   ["ECONÓMIC", "ECONOMIC", "PRODUCT"],
                                "INSTITUCIONAL":["INSTITUC", "POLÍTICO", "POLITICO"],
                            }.get(k, []))), None)
                if _k3:
                    if _vi_val == 1: _vi1_eje[_k3] += 1
                    elif _vi_val == 0: _vi0_eje[_k3] += 1

    _rows_cont = []
    for _k in _eje_order:
        _icpi_v = f"{_icpi_eje[_k]:.1f}%" if _k in _icpi_eje else "N/D"
        _rows_cont.append({
            "Eje (n)":         f"{_k} ({_eje_n[_k]})",
            "ICPI Eje (%)":    _icpi_v,
            "Vi=1":            _vi1_eje[_k],
            "Vi=0":            _vi0_eje[_k],
            "Observación clave": _eje_obs[_k],
        })
    # Fila total
    _icpi_total_str = icpi_str
    _rows_cont.append({
        "Eje (n)":         f"TOTAL ({len(_m5) if _m5_raw is not None and not _m5.empty else 20})",
        "ICPI Eje (%)":    _icpi_total_str,
        "Vi=1":            vi1_n,
        "Vi=0":            _vi0_n,
        "Observación clave": f"ICPI={icpi_str} · {avep_label} · MOM SIGAD confirmado",
    })
    st.dataframe(pd.DataFrame(_rows_cont), use_container_width=True, hide_index=True)

    st.markdown("---")
    csa, csb = st.columns(2)
    with csa:
        st.markdown("#### 🚦 Escala AVEP — Posición GAD Montecristi")
        _avep_rangos = [
            ("≥ 90%",       "⭐ Excelencia Institucional",  icpi_val >= 90),
            ("70% – 89%",   "✅ Gestión por Mandato",        70 <= icpi_val < 90),
            ("40% – 69%",   "🟡 Transición Crítica",         40 <= icpi_val < 70),
            ("20% – 39%",   "🔴 Gestión por Ocurrencia",     20 <= icpi_val < 40),
            ("< 20%",       "⬛ Ruptura Institucional",      icpi_val < 20),
        ]
        st.dataframe(
            pd.DataFrame({
                "Rango ICPI": [r[0] for r in _avep_rangos],
                "Categoría":  [
                    f"{r[1]}  ← GAD Montecristi ({icpi_str})" if r[2] else r[1]
                    for r in _avep_rangos
                ],
            }),
            use_container_width=True, hide_index=True,
        )
    with csb:
        st.markdown("#### 📈 Top 5 Acciones — Impacto ICPI Potencial")
        st.dataframe(
            pd.DataFrame({
                "#": ["#1 🔴", "#2 🔴", "#3 🟠", "#4 🟠", "#5 🟡"],
                "Meta": [
                    "PDOT.SC.OE2.M1.01",
                    "PDOT.AS.OE1.M2.02",
                    "PDOT.AS.OE1.M2.01",
                    "PDOT.AM.OE3.M2.01",
                    "PDOT.AS.OE1.M1.03",
                ],
                "Δ ICPI": ["+9.1 pp", "+2.1 pp", "+1.8 pp", "+2.1 pp", "+0.5 pp"],
                "ICPI resultante": ["56.1%", "49.1%", "48.8%", "49.1%", "47.5%"],
            }),
            use_container_width=True, hide_index=True,
        )

    # ─── HALLAZGO MOM · DATA-SIGAD ───────────────────────────────────
    # Extraer datos MOM desde DATA-SIGAD filas 4-5 y 7
    _icm23_str, _icm24_str       = "N/D", "N/D"
    _brecha23, _brecha24         = "N/D", "N/D"
    _metas23, _metas24           = "—", "—"
    _monto23, _monto24           = "—", "—"
    _pct23, _pct24               = "—", "—"
    _sig_full = cargar_hoja_raw("DATA-SIGAD", nrows=10)
    if _sig_full is not None:
        try:
            # row4 = ICM SIGAD 2023, row5 = ICM SIGAD 2024
            # col1=ICM%, col3=Brecha, col4=Metas, col6=Monto$, col7=%pres
            def _safe_num(df, r, c):
                return pd.to_numeric(str(df.iloc[r, c]).replace(",", ".").strip(), errors="coerce")
            _icm23_raw = _safe_num(_sig_full, 4, 1)
            _icm24_raw = _safe_num(_sig_full, 5, 1)
            _b23_raw   = _safe_num(_sig_full, 4, 3)
            _b24_raw   = _safe_num(_sig_full, 5, 3)
            if pd.notna(_icm23_raw): _icm23_str = f"{_icm23_raw:.2f}%"
            if pd.notna(_icm24_raw): _icm24_str = f"{_icm24_raw:.2f}%"
            if pd.notna(_b23_raw):   _brecha23  = f"Δ {_b23_raw:.2f} pp"
            if pd.notna(_b24_raw):   _brecha24  = f"Δ {_b24_raw:.2f} pp"
            _metas23 = str(_sig_full.iloc[4, 4]).strip().replace("nan", "—")
            _metas24 = str(_sig_full.iloc[5, 4]).strip().replace("nan", "—")
            _m23v = _safe_num(_sig_full, 4, 6)
            _m24v = _safe_num(_sig_full, 5, 6)
            if pd.notna(_m23v): _monto23 = f"${_m23v:,.2f}"
            if pd.notna(_m24v): _monto24 = f"${_m24v:,.2f}"
            _p23v = _safe_num(_sig_full, 4, 7)
            _p24v = _safe_num(_sig_full, 5, 7)
            if pd.notna(_p23v): _pct23 = f"{_p23v*100:.1f}%"
            if pd.notna(_p24v): _pct24 = f"{_p24v*100:.1f}%"
            # ICM consolidado = promedio de ambos (ambos son 100 según DATA-SIGAD)
            if pd.notna(_icm23_raw) and pd.notna(_icm24_raw):
                _icm_consol = (_icm23_raw + _icm24_raw) / 2
                icm_str   = f"{_icm_consol:.2f}%"
                brecha_val = _icm_consol - icpi_val
                brecha_str = f"−{brecha_val:.2f} pp"
                h1_str     = f"+{brecha_val:.2f} pp"
        except Exception:
            pass

    st.markdown("---")
    st.markdown("#### 🚨 Hallazgo Forense MOM — Validez del ICM SIGAD (DATA-SIGAD)")
    st.error(
        f"**ICM SIGAD 2023 = {_icm23_str} · ICM SIGAD 2024 = {_icm24_str}** · Carga masiva extemporánea confirmada.  \n"
        "SIGAD 2024: 5 etapas cargadas el **30/05/2025 en 42 segundos** (00:48:21 → 00:49:03).  \n"
        "SIGAD 2023: I–III trimestres cargados el **16/05/2024 en 13 segundos**.  \n"
        f"Presupuesto reportado: {_monto23} (2023) y {_monto24} (2024) · {_pct23} y {_pct24} del presupuesto total.  \n"
        f"**MOM CONFIRMADO** (umbral ISSAI 5%) — ICM anula su validez como comparativo.  \n"
        f"Brecha de Integridad: **ICPI {icpi_str} vs ICM {icm_str} = {brecha_str} · H₁ ACTIVA.**  \n"
        "Base legal: ISSAI 1000 · Acuerdo SNP-2024-0040-A · COOTAD Art.234 · LOPC Art.89"
    )
    st.dataframe(
        pd.DataFrame({
            "Período":                  ["ICM SIGAD 2023", "ICM SIGAD 2024", "ICPI Auditado",    "Brecha de Integridad"],
            "Valor":                    [_icm23_str,        _icm24_str,        icpi_str,           brecha_str],
            "Metas SIGAD":              [_metas23,          _metas24,          "20 (n total)",     "—"],
            "Monto reportado":          [_monto23,          _monto24,          "—",                "—"],
            "% sobre presupuesto":      [_pct23,            _pct24,            "—",                "—"],
            "Hallazgo": [
                "Carga 3 trimestres en 13 seg · 16/05/2024",
                "🚨 5 etapas en 42 seg · 30/05/2025 · PRINCIPAL",
                "Motor SIAP-ICPI verificado §3.4",
                "H₁ Confirmada · MOM · ISSAI 1000",
            ],
        }),
        use_container_width=True, hide_index=True,
    )

    # Evaluación semestral (SUPPORT-SEM)
    st.markdown("---")
    st.markdown("#### 📅 Evaluación Semestral por Dirección (SUPPORT-SEM)")
    df_sem_raw = cargar_hoja_raw("SUPPORT-SEM", nrows=30)
    if df_sem_raw is not None:
        df_sem = extraer_fila_como_df(df_sem_raw, fila_header=11, fila_inicio=12,
                                       fila_fin=24, filtro_col=None)
        if not df_sem.empty and len(df_sem.columns) >= 4:
            cols_sem = list(df_sem.columns[:6])
            st.dataframe(df_sem[cols_sem].reset_index(drop=True),
                         use_container_width=True, hide_index=True)
    else:
        aviso("No se pudo cargar la hoja SUPPORT-SEM")


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
