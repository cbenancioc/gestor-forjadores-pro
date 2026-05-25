import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# --- 1. DATOS DE RESPALDO (FIXTURE LOCAL) ---
# Estos datos se muestran si la nube falla, evitando la pantalla vacía
fixture_respaldo = [
    {"id_partido": "P1", "cancha": "Cancha 1", "equipo_local": "7ma", "equipo_visitante": "3ra", "goles_local": 0, "goles_visitante": 0, "jugado": False},
    {"id_partido": "P2", "cancha": "Cancha 1", "equipo_local": "9na", "equipo_visitante": "1ra", "goles_local": 0, "goles_visitante": 0, "jugado": False}
]

# --- 2. INTENTO DE CONEXIÓN A LA NUBE ---
def obtener_datos():
    try:
        supabase = create_client("https://jevlhjtviawzripepfoh.supabase.co", "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS")
        response = supabase.table('partidos').select('*').execute()
        return response.data # Retorna los datos de Supabase
    except:
        return fixture_respaldo # Retorna el respaldo local si falla

# --- 3. INTERFAZ (SIEMPRE VISIBLE) ---
st.title("⚽ Campeonato Relámpago Forjadores")

# Intentamos cargar, pero si falla, usamos el respaldo
partidos = obtener_datos()

# --- 4. SEGURIDAD ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297":
        st.session_state.es_admin = True
        st.success("Mesa de Control Activa")

# --- 5. RENDERIZADO ESTABLE ---
# Este bucle se ejecuta SIEMPRE, con datos de nube o de respaldo
for p in partidos:
    with st.container(border=True):
        st.subheader(f"{p.get('equipo_local', 'Local')} vs {p.get('equipo_visitante', 'Visita')}")
        st.metric("Marcador", f"{p.get('goles_local', 0)} - {p.get('goles_visitante', 0)}")
        
        if st.session_state.es_admin:
            st.write("Panel de edición desbloqueado.")
