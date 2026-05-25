import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# Inicialización
try:
    supabase = create_client("https://jevlhjtviawzripepfoh.supabase.co", "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS")
    partidos = supabase.table('partidos').select('*').execute().data
except:
    partidos = []

# --- PANEL LATERAL ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297":
        st.session_state.es_admin = True
    if st.session_state.es_admin:
        st.success("MESA DE CONTROL ACTIVA")

# --- INTERFAZ PRINCIPAL (Siempre se muestra) ---
st.title("⚽ Campeonato Relámpago Forjadores")

if not partidos:
    st.warning("⚠️ Sin conexión a la nube. Modo lectura desactivado.")
else:
    # Renderizado estable para Admin y Visor
    col1, col2 = st.columns(2)
    for p in partidos:
        target = col1 if p['cancha'] == 'Cancha 1' else col2
        with target.container(border=True):
            st.subheader(f"{p['equipo_local']} vs {p['equipo_visitante']}")
            
            if st.session_state.es_admin:
                g1 = st.number_input(f"Goles L", value=p['goles_local'], key=f"g1_{p['id_partido']}")
                g2 = st.number_input(f"Goles V", value=p['goles_visitante'], key=f"g2_{p['id_partido']}")
                if st.button("Guardar", key=f"btn_{p['id_partido']}"):
                    supabase.table('partidos').update({"goles_local": g1, "goles_visitante": g2, "jugado": True}).eq("id_partido", p['id_partido']).execute()
                    st.rerun()
            else:
                st.metric("Marcador", f"{p['goles_local']} - {p['goles_visitante']}")
                st.write(f"Estado: {'✅ Finalizado' if p['jugado'] else '⏳ En Juego'}")
