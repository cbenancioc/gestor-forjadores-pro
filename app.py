import streamlit as st
import pandas as pd
from supabase import create_client

# Configuración
st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")
supabase = create_client("https://jevlhjtviawzripepfoh.supabase.co", "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS")

# --- CONTROL DE ACCESO ---
if 'admin' not in st.session_state: st.session_state.admin = False

with st.sidebar:
    st.title("🔐 Acceso")
    if st.text_input("Clave:", type="password") == "230297":
        st.session_state.admin = True
    elif st.button("Cerrar Sesión"):
        st.session_state.admin = False

# --- CARGA DE DATOS ---
try:
    partidos = supabase.table('partidos').select('*').execute().data
    df_partidos = pd.DataFrame(partidos)
except:
    st.error("Error al conectar con la base de datos.")
    df_partidos = pd.DataFrame()

# --- INTERFAZ PRINCIPAL ---
st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")

# Esta parte siempre se muestra
with st.expander("📜 Ver Reglamento de Desempate"):
    st.write("1. Puntos | 2. Diferencia de Goles | 3. Goles a Favor | 4. Aperturas | 5. Fair Play")

# Renderizado dinámico de partidos
if not df_partidos.empty:
    col1, col2 = st.columns(2)
    for index, p in df_partidos.iterrows():
        cancha_target = col1 if p['cancha'] == 'Cancha 1' else col2
        with cancha_target:
            with st.container(border=True):
                st.subheader(f"{p['equipo_local']} vs {p['equipo_visitante']}")
                
                if st.session_state.admin:
                    # Modo Edición (Administrador)
                    g1 = st.number_input(f"Goles {p['equipo_local']}", value=p['goles_local'], key=f"g1_{p['id_partido']}")
                    g2 = st.number_input(f"Goles {p['equipo_visitante']}", value=p['goles_visitante'], key=f"g2_{p['id_partido']}")
                    if st.button("Guardar en Nube", key=f"btn_{p['id_partido']}"):
                        supabase.table('partidos').update({"goles_local": g1, "goles_visitante": g2, "jugado": True}).eq("id_partido", p['id_partido']).execute()
                        st.rerun()
                else:
                    # Modo Visor
                    st.metric("Marcador", f"{p['goles_local']} - {p['goles_visitante']}")
                    st.write(f"Estado: {'✅ Finalizado' if p['jugado'] else '⏳ En Juego'}")
else:
    st.warning("No hay partidos cargados en la base de datos.")
