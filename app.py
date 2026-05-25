import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# Configuración
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- SEGURIDAD ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False

with st.sidebar:
    st.title("🔐 Acceso")
    pwd = st.text_input("Clave:", type="password")
    if pwd == "230297": st.session_state.es_admin = True
    if st.session_state.es_admin: st.success("MESA DE CONTROL ACTIVA")

# --- LÓGICA DE DATOS ---
def obtener_datos():
    try:
        # Intentamos traer datos de la nube
        res = supabase.table('partidos').select('*').execute()
        return res.data
    except:
        # Si falla, devolvemos una lista vacía para que el código no se rompa
        return []

# --- INTERFAZ ---
st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")
st.expander("📜 Ver Reglamento de Desempate").write("1. PTS | 2. DG | 3. GF | 4. Aperturas | 5. Fair Play")

partidos = obtener_datos()

# SI NO HAY DATOS, AVISAMOS PERO MANTENEMOS LA UI
if not partidos:
    st.warning("⚠️ No se pudieron cargar los datos de la nube. Verifique la conexión a Supabase.")
else:
    col1, col2 = st.columns(2)
    for p in partidos:
        target = col1 if p['cancha'] == 'Cancha 1' else col2
        with target:
            with st.container(border=True):
                st.subheader(f"{p['equipo_local']} vs {p['equipo_visitante']}")
                if st.session_state.es_admin:
                    g1 = st.number_input(f"Goles {p['equipo_local']}", value=p['goles_local'], key=f"g1_{p['id_partido']}")
                    g2 = st.number_input(f"Goles {p['equipo_visitante']}", value=p['goles_visitante'], key=f"g2_{p['id_partido']}")
                    if st.button("Guardar", key=f"btn_{p['id_partido']}"):
                        supabase.table('partidos').update({"goles_local": g1, "goles_visitante": g2, "jugado": True}).eq("id_partido", p['id_partido']).execute()
                        st.rerun()
                else:
                    st.metric("Marcador", f"{p['goles_local']} - {p['goles_visitante']}")
                    st.write(f"Estado: {'✅ Finalizado' if p['jugado'] else '⏳ En Juego'}")
