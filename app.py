import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# Inicialización segura
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- PANEL DE CONTROL ---
if 'admin' not in st.session_state: st.session_state.admin = False

with st.sidebar:
    st.title("🔐 Acceso")
    clave = st.text_input("Clave:", type="password")
    if clave == "230297": 
        st.session_state.admin = True
        st.success("Mesa de Control Desbloqueada")
    else: 
        st.session_state.admin = False

# --- LÓGICA DE ACTUALIZACIÓN ---
@st.fragment # Solo refresca la parte modificada
def render_partido(p):
    with st.expander(f"{p['equipo_local']} vs {p['equipo_visitante']}", expanded=True):
        if st.session_state.admin:
            cols = st.columns(2)
            g1 = cols[0].number_input(f"Goles {p['equipo_local']}", value=p['goles_local'], key=f"g1_{p['id_partido']}")
            g2 = cols[1].number_input(f"Goles {p['equipo_visitante']}", value=p['goles_visitante'], key=f"g2_{p['id_partido']}")
            
            if st.button("Guardar", key=f"btn_{p['id_partido']}"):
                supabase.table('partidos').update({
                    "goles_local": g1, "goles_visitante": g2, "jugado": True
                }).eq("id_partido", p['id_partido']).execute()
                st.rerun() # Fuerza la actualización de la UI
        
        st.metric("Marcador", f"{p['goles_local']} - {p['goles_visitante']}")
        st.caption(f"Estado: {'✅ Finalizado' if p['jugado'] else '⏳ En Juego'}")

# --- ESTRUCTURA PRINCIPAL ---
st.title("⚽ Campeonato Relámpago Forjadores")
res = supabase.table('partidos').select('*').execute()
partidos = res.data

col1, col2 = st.columns(2)
for p in partidos:
    if p['cancha'] == 'Cancha 1': render_partido(p)
    else: render_partido(p)
