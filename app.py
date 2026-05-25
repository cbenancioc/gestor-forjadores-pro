import streamlit as st
import pandas as pd
from supabase import create_client

# Configuración y Conexión
st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")
supabase = create_client("https://jevlhjtviawzripepfoh.supabase.co", "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS")

# --- 1. SEGURIDAD Y ESTADO ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False

# --- 2. LÓGICA DE PERSISTENCIA (Sincronización Supabase) ---
def sincronizar_partidos():
    # Lee todos los partidos de la base de datos
    data = supabase.table('partidos').select('*').execute().data
    return data

# --- 3. INTERFAZ GRÁFICA (Integrando tu diseño) ---
st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")

# Menú lateral para admin
with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297": st.session_state.es_admin = True
    else: st.session_state.es_admin = False
    
    if st.session_state.es_admin: st.success("✅ MESA DE CONTROL ACTIVA")
    else: st.info("👀 MODO VISOR: Solo lectura")

# Carga de datos
partidos = sincronizar_partidos()

# Renderizado amigable (basado en tu diseño original)
with st.expander("📜 Ver Reglamento de Desempate"):
    st.write("1. PTS | 2. DG | 3. GF | 4. Aperturas | 5. Fair Play")

col1, col2 = st.columns(2)

for p in partidos:
    # Determinamos en qué columna va según la cancha
    target = col1 if p['cancha'] == 'Cancha 1' else col2
    
    with target:
        with st.expander(f"{p['equipo_local']} vs {p['equipo_visitante']}", expanded=True):
            if st.session_state.es_admin:
                # Interfaz de Edición para Administrador
                g1 = st.number_input(f"Goles {p['equipo_local']}", value=p['goles_local'], key=f"g1_{p['id_partido']}")
                g2 = st.number_input(f"Goles {p['equipo_visitante']}", value=p['goles_visitante'], key=f"g2_{p['id_partido']}")
                
                if st.button("💾 Guardar en Nube", key=f"btn_{p['id_partido']}"):
                    supabase.table('partidos').update({
                        "goles_local": g1, 
                        "goles_visitante": g2,
                        "jugado": True
                    }).eq("id_partido", p['id_partido']).execute()
                    st.rerun() # Esto refresca toda la app tras guardar
            else:
                # Interfaz amigable para Visores
                st.markdown(f"<h2 style='text-align:center;'>{p['goles_local']} - {p['goles_visitante']}</h2>", unsafe_allow_html=True)
                st.write(f"Estado: {'✅ Finalizado' if p['jugado'] else '⏳ En Juego'}")
