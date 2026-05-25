import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# 1. TÍTULO SIEMPRE VISIBLE
st.title("⚽ Campeonato Relámpago Forjadores")

# 2. ACCESO SIEMPRE VISIBLE
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297":
        st.session_state.es_admin = True
        st.success("Mesa de Control Activa")

# 3. CARGA DE DATOS BLINDADA
try:
    supabase = create_client("https://jevlhjtviawzripepfoh.supabase.co", "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS")
    partidos = supabase.table('partidos').select('*').execute().data
except:
    partidos = [] # Lista vacía si falla la conexión

# 4. RENDERIZADO SIEMPRE VISIBLE
if not partidos:
    st.warning("⚠️ No se cargaron datos. Mostrando interfaz de control vacía.")
else:
    for p in partidos:
        with st.container(border=True):
            st.subheader(f"{p.get('equipo_local', 'Local')} vs {p.get('equipo_visitante', 'Visita')}")
            st.metric("Marcador", f"{p.get('goles_local', 0)} - {p.get('goles_visitante', 0)}")

# Si eres admin, siempre muestras los controles, incluso si la lista está vacía
if st.session_state.es_admin:
    st.markdown("---")
    st.subheader("🛠️ Panel de Administración")
    st.write("Usa este panel para gestionar partidos manualmente si la nube falla.")
    if st.button("Recargar Conexión"):
        st.rerun()
