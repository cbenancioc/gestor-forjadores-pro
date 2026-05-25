import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# --- 1. DATOS DE RESPALDO (JSON LOCAL) ---
# Si la nube falla, estos son los datos que verán los asistentes
fixture_local = [
    {"id_partido": "P1", "cancha": "Cancha 1", "equipo_local": "7ma", "equipo_visitante": "3ra", "goles_local": 0, "goles_visitante": 0, "jugado": False},
    {"id_partido": "P2", "cancha": "Cancha 1", "equipo_local": "9na", "equipo_visitante": "1ra", "goles_local": 0, "goles_visitante": 0, "jugado": False}
]

# --- 2. INTENTO DE CONEXIÓN ---
@st.cache_resource
def get_supabase_client():
    return create_client("https://jevlhjtviawzripepfoh.supabase.co", "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS")

def obtener_partidos():
    try:
        supabase = get_supabase_client()
        return supabase.table('partidos').select('*').execute().data, True
    except:
        return fixture_local, False

# --- 3. INTERFAZ ---
st.title("⚽ Campeonato Relámpago Forjadores")
partidos, conectado = obtener_partidos()

# --- SEGURIDAD ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297": st.session_state.es_admin = True

# --- RENDERIZADO SIEMPRE ACTIVO ---
for p in partidos:
    with st.container(border=True):
        st.subheader(f"{p['equipo_local']} vs {p['equipo_visitante']}")
        if st.session_state.es_admin and conectado:
            g1 = st.number_input("Goles Local", value=p['goles_local'], key=f"g1_{p['id_partido']}")
            g2 = st.number_input("Goles Visita", value=p['goles_visitante'], key=f"g2_{p['id_partido']}")
            if st.button("Guardar", key=f"btn_{p['id_partido']}"):
                get_supabase_client().table('partidos').update({"goles_local": g1, "goles_visitante": g2, "jugado": True}).eq("id_partido", p['id_partido']).execute()
                st.rerun()
        else:
            st.metric("Marcador", f"{p['goles_local']} - {p['goles_visitante']}")
