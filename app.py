import streamlit as st
from supabase import create_client

# Configuración de página
st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# Conexión Supabase
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("⚽ Campeonato Relámpago Forjadores")

# --- LÓGICA DE DATOS ---
def cargar_partidos():
    try:
        return supabase.table('partidos').select('*').execute().data
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return []

# --- PANEL DE ACCESO ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297":
        st.session_state.es_admin = True
        st.success("Panel de Control Activo")

# --- INTERFAZ PRINCIPAL ---
partidos = cargar_partidos()

if not partidos:
    st.warning("La base de datos está vacía. Inserta partidos en el Table Editor de Supabase.")
else:
    col1, col2 = st.columns(2)
    for p in partidos:
        # Asignar a la columna correspondiente
        target = col1 if p.get('cancha') == 'Cancha 1' else col2
        with target.container(border=True):
            st.subheader(f"{p.get('equipo_local', 'Local')} vs {p.get('equipo_visitante', 'Visita')}")
            
            if st.session_state.es_admin:
                # Interfaz de Edición
                g1 = st.number_input(f"Goles {p.get('equipo_local')}", value=p.get('goles_local', 0), key=f"g1_{p['id_partido']}")
                g2 = st.number_input(f"Goles {p.get('equipo_visitante')}", value=p.get('goles_visitante', 0), key=f"g2_{p['id_partido']}")
                if st.button("Guardar en Nube", key=f"btn_{p['id_partido']}"):
                    supabase.table('partidos').update({"goles_local": g1, "goles_visitante": g2, "jugado": True}).eq("id_partido", p['id_partido']).execute()
                    st.rerun()
            else:
                # Visualización
                st.metric("Marcador", f"{p.get('goles_local', 0)} - {p.get('goles_visitante', 0)}")
