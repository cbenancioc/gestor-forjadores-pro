import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores", layout="wide")

# Conexión
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("⚽ Campeonato Relámpago Forjadores")

# Carga de datos
try:
    response = supabase.table('partidos').select('*').execute()
    partidos = response.data
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    partidos = []

if not partidos:
    st.info("La tabla 'partidos' está vacía. Inserta registros desde el Table Editor.")
else:
    for p in partidos:
        # Usamos los nombres de columna EXACTOS de tu SQL
        with st.container(border=True):
            st.subheader(f"{p.get('equipo_local')} vs {p.get('equipo_visitante')}")
            
            # --- ZONA DE EDICIÓN ---
            if st.session_state.get('es_admin', False):
                g_local = st.number_input(f"Goles {p.get('equipo_local')}", value=p.get('goles_local', 0), key=f"gl_{p['id_partido']}")
                g_visita = st.number_input(f"Goles {p.get('equipo_visitante')}", value=p.get('goles_visitante', 0), key=f"gv_{p['id_partido']}")
                
                if st.button("Guardar", key=f"btn_{p['id_partido']}"):
                    supabase.table('partidos').update({
                        "goles_local": g_local, 
                        "goles_visitante": g_visita
                    }).eq("id_partido", p['id_partido']).execute()
                    st.rerun()
            else:
                st.metric("Marcador", f"{p.get('goles_local', 0)} - {p.get('goles_visitante', 0)}")
