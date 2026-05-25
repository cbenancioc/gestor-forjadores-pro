import streamlit as st
from supabase import create_client

# --- CONFIGURACIÓN Y CONEXIÓN ---
st.set_page_config(page_title="Gestor Forjadores PRO", page_icon="⚽", layout="wide")

SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNCIONES DE BASE DE DATOS SEGURAS ---
def cargar_partidos():
    try:
        # Ordenamos por rueda y luego por id
        return supabase.table('partidos').select('*').order('rueda').order('id_partido').execute().data
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return []

def guardar_resultado(p_id, datos_actualizados):
    try:
        supabase.table('partidos').update(datos_actualizados).eq('id_partido', p_id).execute()
        st.success("¡Cambios guardados en la nube!")
    except Exception as e:
        st.error(f"Error al guardar: {e}")

# --- PANEL DE ACCESO ADMIN ---
if 'es_admin' not in st.session_state: 
    st.session_state.es_admin = False

with st.sidebar:
    st.title("🔐 Acceso Admin")
    if st.text_input("Clave de Mesa:", type="password") == "230297":
        st.session_state.es_admin = True
        st.success("Mesa de Control Desbloqueada")
    else:
        st.info("Modo Visor: Solo lectura de resultados.")

# --- INTERFAZ PRINCIPAL ---
st.title("⚽ Campeonato Relámpago Forjadores - Casino de Policía")
st.markdown("---")

partidos = cargar_partidos()

if not partidos:
    st.warning("La base de datos está limpia y lista. Aún no hay partidos cargados.")
else:
    # Agrupar partidos por su 'rueda'
    ruedas = sorted(list(set(p.get('rueda', 'Sin Rueda') for p in partidos if p.get('rueda'))))
    
    for rueda in ruedas:
        st.header(f"🏆 {rueda}")
        partidos_rueda = [p for p in partidos if p.get('rueda') == rueda]
        
        for p in partidos_rueda:
            # Usamos .get() para evitar cualquier KeyError futuro
            eq_local = p.get('equipo_local', 'Local')
            eq_visita = p.get('equipo_visitante', 'Visita')
            id_p = p.get('id_partido')
            estado = p.get('estado', 'Pendiente')
            
            with st.expander(f"{eq_local} vs {eq_visita} | Estado: {estado}", expanded=True):
                if st.session_state.es_admin:
                    # MODO EDICIÓN
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**{eq_local}**")
                        gl = st.number_input("Goles L", value=p.get('goles_local', 0), key=f"gl_{id_p}")
                        al = st.number_input("🟨 Amarillas L", value=p.get('amarillas_local', 0), key=f"al_{id_p}")
                        rl = st.number_input("🟥 Rojas L", value=p.get('rojas_local', 0), key=f"rl_{id_p}")
                        
                    with col2:
                        st.markdown(f"**{eq_visita}**")
                        gv = st.number_input("Goles V", value=p.get('goles_visitante', 0), key=f"gv_{id_p}")
                        av = st.number_input("🟨 Amarillas V", value=p.get('amarillas_visitante', 0), key=f"av_{id_p}")
                        rv = st.number_input("🟥 Rojas V", value=p.get('rojas_visitante', 0), key=f"rv_{id_p}")
                    
                    st.markdown("---")
                    col_pg, col_est, col_btn = st.columns([2, 2, 1])
                    pg = col_pg.text_input("⚽ Autor del 1er Gol", value=p.get('primer_gol', 'Ninguno'), key=f"pg_{id_p}")
                    est = col_est.selectbox("Estado del partido", ["Pendiente", "Finalizado"], index=0 if estado=="Pendiente" else 1, key=f"est_{id_p}")
                    
                    if col_btn.button("💾 Guardar", key=f"btn_{id_p}", use_container_width=True):
                        datos = {
                            "goles_local": gl, "goles_visitante": gv,
                            "amarillas_local": al, "rojas_local": rl,
                            "amarillas_visitante": av, "rojas_visitante": rv,
                            "primer_gol": pg, "estado": est
                        }
                        guardar_resultado(id_p, datos)
                        st.rerun()
                else:
                    # MODO VISOR PÚBLICO
                    st.markdown(f"<h2 style='text-align: center;'>{p.get('goles_local', 0)} - {p.get('goles_visitante', 0)}</h2>", unsafe_allow_html=True)
                    st.caption(f"⚽ 1er gol: {p.get('primer_gol', 'Ninguno')} | 🏟️ {p.get('cancha', 'Por definir')}")
