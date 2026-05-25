import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# Configuración
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"

# --- SEGURIDAD ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    if st.text_input("Clave:", type="password") == "230297": st.session_state.es_admin = True

# --- DATOS HÍBRIDOS ---
fixture_inicial = [
    {"id_partido": "P1", "cancha": "Cancha 1", "equipo_local": "7ma", "equipo_visitante": "3ra", "goles_local": 0, "goles_visitante": 0, "jugado": False},
    {"id_partido": "P2", "cancha": "Cancha 1", "equipo_local": "9na", "equipo_visitante": "1ra", "goles_local": 0, "goles_visitante": 0, "jugado": False}
]

def obtener_datos():
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        res = supabase.table('partidos').select('*').execute()
        return res.data, True
    except:
        return fixture_inicial, False

st.title("⚽ Campeonato Relámpago Forjadores")
partidos, conectado = obtener_datos()

if not conectado:
    st.info("🌐 Modo Respaldo: Visualizando fixture local (Nube inaccesible)")

for p in partidos:
    with st.container(border=True):
        st.subheader(f"{p['equipo_local']} vs {p['equipo_visitante']}")
        st.metric("Marcador", f"{p['goles_local']} - {p['goles_visitante']}")
