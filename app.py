import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores", layout="wide", page_icon="⚽")

# --- CONEXIÓN ---
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"

@st.cache_data(ttl=5)
def obtener_partidos():
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase.table('partidos').select('*').execute().data
    except:
        return [
            {"id_partido": "P1", "cancha": "Cancha 1", "equipo_local": "7ma SEC", "equipo_visitante": "3ra SEC", "goles_local": 0, "goles_visitante": 0, "jugado": False},
            {"id_partido": "P2", "cancha": "Cancha 2", "equipo_local": "5ta SEC", "equipo_visitante": "8va SEC", "goles_local": 0, "goles_visitante": 0, "jugado": False}
        ]

# --- UI PRINCIPAL ---
st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")
with st.expander("📜 Ver Reglamento de Desempate"):
    st.write("1. PTS | 2. DG | 3. GF | 4. Aperturas | 5. Fair Play")

partidos = obtener_partidos()
col1, col2 = st.columns(2)

# --- RENDERIZADO EN COLUMNAS (Igual a tu original) ---
for p in partidos:
    destino = col1 if p.get('cancha') == 'Cancha 1' else col2
    with destino:
        with st.expander(f"{p['equipo_local']} vs {p['equipo_visitante']}", expanded=True):
            st.markdown(f"<h1 style='text-align:center;'>{p['goles_local']} - {p['goles_visitante']}</h1>", unsafe_allow_html=True)
            st.write(f"Estado: {'✅ Finalizado' if p['jugado'] else '⏳ En Juego'}")

# --- ACCESO ADMIN ---
with st.sidebar:
    st.title("🔐 Acceso al Sistema")
    if st.text_input("Clave de Administrador:", type="password") == "230297":
        st.success("Mesa de Control Desbloqueada")
