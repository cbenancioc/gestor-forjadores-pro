import streamlit as st
import pandas as pd
from supabase import create_client

# --- CONEXIÓN ---
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Torneo Forjadores PRO", page_icon="⚽", layout="wide")

# --- LÓGICA DE PERSISTENCIA ---
def cargar_datos_nube():
    return supabase.table('partidos').select('*').execute().data

def guardar_datos_nube(p):
    supabase.table('partidos').update({
        "g1": p["g1"], "g2": p["g2"], "ta1": p["ta1"], "tr1": p["tr1"],
        "ta2": p["ta2"], "tr2": p["tr2"], "primer_gol": p["primer_gol"], "fin": p["fin"]
    }).eq("id", p["id"]).execute()

# --- SEGURIDAD ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    if st.text_input("Clave Admin:", type="password") == "230297":
        st.session_state.es_admin = True

# --- MOTOR DE PROCESAMIENTO (Tu lógica original) ---
# Aquí iría tu función procesar_fase() y actualizar_todo_el_torneo()
# (He mantenido la estructura para que los botones de 'Guardar' ahora llamen a guardar_datos_nube)

st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")

# --- CARGA DEL FIXTURE COMPLETO ---
partidos = cargar_datos_nube()

if not partidos:
    st.error("Tabla 'partidos' vacía. Importa tu CSV desde el Table Editor.")
else:
    # --- RENDERIZADO DEL FIXTURE ---
    # Aquí puedes usar tu lógica original de 'for p in partidos' 
    # o la estructura de pestañas/ruedas que ya tenías diseñada.
    
    for p in partidos:
        with st.expander(f"Fecha {p.get('fecha_nro', 'N/A')} - {p.get('eq1')} vs {p.get('eq2')}"):
            if st.session_state.es_admin:
                p["g1"] = st.number_input(f"Goles {p['eq1']}", value=p["g1"], key=f"g1_{p['id']}")
                if st.button("Guardar cambios", key=f"btn_{p['id']}"):
                    guardar_datos_nube(p)
                    st.rerun()
            else:
                st.write(f"Marcador: {p['g1']} - {p['g2']}")
