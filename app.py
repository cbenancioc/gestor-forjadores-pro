import streamlit as st
import pandas as pd
from supabase import create_client

# Configuración y Conexión
st.set_page_config(page_title="Gestor Oficial Forjadores", layout="wide")
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- PANEL DE CONTROL ---
if 'admin' not in st.session_state: st.session_state.admin = False
with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297": st.session_state.admin = True
    else: st.session_state.admin = False

# --- LÓGICA DE DATOS ---
def get_partidos():
    return supabase.table('partidos').select('*').execute().data

# --- INTERFAZ AMIGABLE ---
st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")
with st.expander("📜 Ver Reglamento de Desempate"):
    st.write("1. Puntos | 2. Dif. Goles | 3. Goles a Favor | 4. Aperturas | 5. Fair Play")

# Renderizado de partidos con todas sus variables
partidos = get_partidos()
col1, col2 = st.columns(2)

for p in partidos:
    target = col1 if p['cancha'] == 'Cancha 1' else col2
    with target:
        with st.expander(f"{p['equipo_local']} vs {p['equipo_visitante']}", expanded=True):
            if st.session_state.admin:
                g1 = st.number_input(f"Goles {p['equipo_local']}", value=p['goles_local'], key=f"g1_{p['id_partido']}")
                g2 = st.number_input(f"Goles {p['equipo_visitante']}", value=p['goles_visitante'], key=f"g2_{p['id_partido']}")
                pg = st.selectbox("1er Gol:", ["Ninguno", "Local", "Visitante"], index=["Ninguno", "Local", "Visitante"].index(p['primer_gol']), key=f"pg_{p['id_partido']}")
                
                if st.button("💾 Guardar en Nube", key=f"btn_{p['id_partido']}"):
                    supabase.table('partidos').update({
                        "goles_local": g1, "goles_visitante": g2, "primer_gol": pg, "jugado": True
                    }).eq("id_partido", p['id_partido']).execute()
                    st.rerun()
            else:
                st.metric("Marcador", f"{p['goles_local']} - {p['goles_visitante']}")
                st.write(f"⚽ 1er gol: {p['primer_gol']} | Estado: {'✅ Finalizado' if p['jugado'] else '⏳ En Juego'}")
