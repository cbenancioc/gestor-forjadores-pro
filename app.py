import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# Configuración
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"

# --- 1. SEGURIDAD ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297": st.session_state.es_admin = True

# --- 2. CARGA FORZADA (BLINDADA) ---
st.title("⚽ Campeonato Relámpago Forjadores")

@st.cache_data(ttl=5) # Refresca cada 5 segundos
def obtener_datos():
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase.table('partidos').select('*').execute().data, True
    except:
        return [
            {"id_partido": "P1", "cancha": "Cancha 1", "equipo_local": "7ma", "equipo_visitante": "3ra", "goles_local": 0, "goles_visitante": 0, "jugado": False},
            {"id_partido": "P2", "cancha": "Cancha 1", "equipo_local": "9na", "equipo_visitante": "1ra", "goles_local": 0, "goles_visitante": 0, "jugado": False}
        ], False

with st.spinner("Conectando con el servidor..."):
    partidos, conectado = obtener_datos()

# --- 3. RENDERIZADO ESTABLE ---
if not conectado:
    st.warning("⚠️ Funcionando en modo local (sin conexión a Supabase).")

for p in partidos:
    with st.container(border=True):
        st.subheader(f"{p['equipo_local']} vs {p['equipo_visitante']}")
        if st.session_state.es_admin and conectado:
            g1 = st.number_input("Goles Local", value=int(p['goles_local']), key=f"g1_{p['id_partido']}")
            g2 = st.number_input("Goles Visita", value=int(p['goles_visitante']), key=f"g2_{p['id_partido']}")
            if st.button("Guardar en Nube", key=f"btn_{p['id_partido']}"):
                create_client(SUPABASE_URL, SUPABASE_KEY).table('partidos').update({"goles_local": g1, "goles_visitante": g2, "jugado": True}).eq("id_partido", p['id_partido']).execute()
                st.rerun()
        else:
            st.metric("Marcador", f"{p['goles_local']} - {p['goles_visitante']}")
