import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# Configuración
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")

# --- CARGA DE DATOS ---
partidos = supabase.table('partidos').select('*').execute().data

# --- PANEL DE ADMIN (Desbloquea funciones avanzadas) ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.title("🔐 Acceso Admin")
    if st.text_input("Clave:", type="password") == "230297":
        st.session_state.es_admin = True

# --- INTERFAZ DE GESTIÓN ---
for p in partidos:
    with st.container(border=True):
        st.subheader(f"{p['equipo_local']} vs {p['equipo_visitante']}")
        
        if st.session_state.es_admin:
            # Campos de edición avanzada
            col1, col2, col3 = st.columns(3)
            with col1:
                g_l = st.number_input(f"Goles {p['equipo_local']}", value=p.get('goles_local', 0), key=f"gl_{p['id_partido']}")
                a_l = st.number_input(f"Amarillas L", value=p.get('amarillas_local', 0), key=f"al_{p['id_partido']}")
            with col2:
                g_v = st.number_input(f"Goles {p['equipo_visitante']}", value=p.get('goles_visitante', 0), key=f"gv_{p['id_partido']}")
                a_v = st.number_input(f"Amarillas V", value=p.get('amarillas_visitante', 0), key=f"av_{p['id_partido']}")
            with col3:
                primer_gol = st.text_input("Primer gol (nombre)", value=p.get('primer_gol', ''), key=f"pg_{p['id_partido']}")
                if st.button("Guardar Cambios", key=f"btn_{p['id_partido']}"):
                    supabase.table('partidos').update({
                        "goles_local": g_l, "goles_visitante": g_v,
                        "amarillas_local": a_l, "amarillas_visitante": a_v,
                        "primer_gol": primer_gol
                    }).eq("id_partido", p['id_partido']).execute()
                    st.rerun()
        else:
            # Vista pública
            st.metric("Marcador", f"{p.get('goles_local')} - {p.get('goles_visitante')}")
            st.caption(f"Primer gol: {p.get('primer_gol', 'N/A')}")
