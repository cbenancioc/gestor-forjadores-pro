import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# --- CONEXIÓN ---
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")
with st.expander("📜 Ver Reglamento de Desempate"):
    st.write("1. PTS | 2. DG | 3. GF | 4. Aperturas | 5. Fair Play")

# --- ACCESO ADMIN ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.title("🔐 Acceso al Sistema")
    if st.text_input("Clave de Administrador:", type="password") == "230297":
        st.session_state.es_admin = True
        st.success("Mesa de Control Desbloqueada")

# --- CARGA Y RENDERIZADO ---
try:
    partidos = supabase.table('partidos').select('*').execute().data
    if not partidos:
        st.warning("La base de datos está vacía. Agrega partidos en tu panel de Supabase.")
    else:
        col1, col2 = st.columns(2)
        for p in partidos:
            destino = col1 if p.get('cancha') == 'Cancha 1' else col2
            with destino.container(border=True):
                st.subheader(f"{p.get('equipo_local')} vs {p.get('equipo_visitante')}")
                
                if st.session_state.es_admin:
                    g1 = st.number_input(f"Goles {p.get('equipo_local')}", value=p.get('goles_local', 0), key=f"g1_{p['id_partido']}")
                    g2 = st.number_input(f"Goles {p.get('equipo_visitante')}", value=p.get('goles_visitante', 0), key=f"g2_{p['id_partido']}")
                    if st.button("Guardar en Nube", key=f"btn_{p['id_partido']}"):
                        supabase.table('partidos').update({"goles_local": g1, "goles_visitante": g2, "jugado": True}).eq("id_partido", p['id_partido']).execute()
                        st.rerun()
                else:
                    st.markdown(f"## {p.get('goles_local', 0)} - {p.get('goles_visitante', 0)}")
except Exception as e:
    st.error(f"Error de conexión: {e}")
