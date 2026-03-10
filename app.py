import streamlit as st
import pandas as pd

st.set_page_config(page_title="QUADRUM v1.0", layout="wide")

st.sidebar.title("🏛️ QUADRUM v1.0")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegación:", ["Dashboard", "Ingesta", "Auditoría"])

if menu == "Dashboard":
    st.title("📊 Panel Ejecutivo de Integridad")
    st.metric("ICPI Global", "38.28%", "-53.97 pp")
    st.info("Estado: Transición Crítica 🟡")

elif menu == "Ingesta":
    st.title("📥 Ingesta de Datos eSIGEF/SERCOP")
    st.file_uploader("Subir Cédula Presupuestaria (CSV)")

elif menu == "Auditoría":
    st.title("⚖️ Motor SIAP-ICPI")
    st.write("Variables: Pi, Ri, Vi, Ti, Ei, Ci")
