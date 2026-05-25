import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# --- 1. CONFIGURACIÓN ---
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"

# --- 2. SEGURIDAD (Siempre se dibuja) ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297":
        st.session_state.es_admin = True
        st.success("Mesa de Control Activa")

# --- 3. INTERFAZ FIJA (Siempre se dibuja) ---
st.title("⚽ Campeonato Relámpago Forjadores")
st.write("---")

# --- 4. CARGA BLINDADA ---
@st.cache_data(ttl=5)
def obtener_datos():
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase.table('partidos').select('*').execute().data, True
    except:
        return [
            {"id_partido": "P1", "cancha": "Cancha 1", "equipo_local": "7ma", "equipo_visitante": "3ra", "goles_local": 0, "goles_visitante": 0},
            {"id_partido": "P2", "cancha": "Cancha 1", "equipo_local": "9na", "equipo_visitante": "1ra", "goles_local": 0, "goles_visitante": 0}
        ], False

partidos, conectado = obtener_datos()

if not conectado:
    st.warning("⚠️ Funcionando en modo local (sin conexión a Supabase).")

# --- 5. RENDERIZADO ESTABLE ---
for p in partidos:
    with st.container(border=True):
        st.subheader(f"{p.get('equipo_local')} vs {p.get('equipo_visitante')}")
        st.metric("Marcador", f"{p.get('goles_local')} - {p.get('goles_visitante')}")
