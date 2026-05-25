import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# 1. Configuración de cliente
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"

# 2. Inicialización de sesión
if 'es_admin' not in st.session_state: st.session_state.es_admin = False

# 3. Interfaz fija (Siempre se dibuja primero)
st.title("⚽ Campeonato Relámpago Forjadores")

with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297":
        st.session_state.es_admin = True

# 4. Intentamos cargar datos pero SIN detener el script si falla
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table('partidos').select('*').execute()
    partidos = response.data
except Exception as e:
    # Si falla, usamos un fixture por defecto para que la app no se quede en blanco
    partidos = [
        {"id_partido": "P1", "cancha": "Cancha 1", "equipo_local": "7ma", "equipo_visitante": "3ra", "goles_local": 0, "goles_visitante": 0, "jugado": False},
        {"id_partido": "P2", "cancha": "Cancha 1", "equipo_local": "9na", "equipo_visitante": "1ra", "goles_local": 0, "goles_visitante": 0, "jugado": False}
    ]
    st.error("Modo Offline: No se pudo conectar a la nube.")

# 5. Renderizado final (Se ejecuta siempre)
for p in partidos:
    with st.container(border=True):
        st.subheader(f"{p['equipo_local']} vs {p['equipo_visitante']}")
        st.metric("Marcador", f"{p['goles_local']} - {p['goles_visitante']}")
        if st.session_state.es_admin:
            if st.button(f"Editar {p['id_partido']}"):
                st.write("Interfaz de edición abierta")
