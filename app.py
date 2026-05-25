import streamlit as st
import pandas as pd
from supabase import create_client

# Configuración inicial (Estilo de la interfaz amigable)
st.set_page_config(page_title="Gestor Forjadores", layout="wide")

# Conexión a Base de Datos (Supabase)
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- PANEL LATERAL (Diseño amigable) ---
with st.sidebar:
    st.title("🔐 Acceso al Sistema")
    st.info("MODO VISOR: Estás viendo resultados en vivo.")
    clave = st.text_input("Clave de Administrador:", type="password")
    es_admin = (clave == "230297")
    if es_admin: st.success("✅ Mesa de Control Desbloqueada")

# --- DISEÑO PRINCIPAL (Igual al de tu imagen) ---
st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")

with st.expander("📜 Ver Reglamento de Desempate en Fases de Grupos"):
    st.write("1. PTS | 2. DG | 3. GF | 4. Aperturas | 5. Fair Play")

st.header("📋 Primera Rueda")

# Carga de datos de la Nube
res = supabase.table('partidos').select('*').execute()
partidos = res.data

# Organización en columnas (Cancha 1 y 2)
col1, col2 = st.columns(2)

def render_partido(p, col):
    with col:
        with st.expander(f"{p['equipo_local']} vs {p['equipo_visitante']}", expanded=True):
            st.markdown(f"<h1 style='text-align:center;'>{p['goles_local']} - {p['goles_visitante']}</h1>", unsafe_allow_html=True)
            st.write(f"⚽ **1er gol:** {p['primer_gol']} | **Estado:** {'✅ Finalizado' if p['jugado'] else '⏳ En Juego'}")
            st.write(f"{p['equipo_local']}: 🟨{p['amarillas_local']} 🟥{p['rojas_local']} | {p['equipo_visitante']}: 🟨{p['amarillas_visitante']} 🟥{p['rojas_visitante']}")
            
            if es_admin:
                if st.button(f"Gestionar {p['id_partido']}"):
                    st.session_state.partido_seleccionado = p

# Renderizado
c1_partidos = [p for p in partidos if p['cancha'] == 'Cancha 1']
c2_partidos = [p for p in partidos if p['cancha'] == 'Cancha 2']

for p in c1_partidos: render_partido(p, col1)
for p in c2_partidos: render_partido(p, col2)
 
