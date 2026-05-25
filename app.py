import streamlit as st
from supabase import create_client

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Forjadores PRO", page_icon="⚽", layout="wide")

SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- SEGURIDAD ADMIN ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Escudo_de_la_Polic%C3%ADa_Nacional_del_Per%C3%BA.png/200px-Escudo_de_la_Polic%C3%ADa_Nacional_del_Per%C3%BA.png", width=100)
    st.title("🔐 Acceso Admin")
    if st.text_input("Clave de Mesa:", type="password") == "230297":
        st.session_state.es_admin = True
        st.success("Mesa de Control Desbloqueada")
    else:
        st.info("Modo Visor: Solo lectura.")
    
    st.markdown("---")
    # --- MENÚ DE NAVEGACIÓN ---
    st.subheader("📍 Navegación")
    menu = st.radio("Ir a:", [
        "⚽ Fixture y Partidos", 
        "📊 Tabla de Posiciones", 
        "📋 Padrón de Jugadores"
    ])

# ==========================================
# MÓDULO 1: FIXTURE Y PARTIDOS
# ==========================================
if menu == "⚽ Fixture y Partidos":
    st.title("⚽ Campeonato Relámpago - Gestión de Partidos")
    partidos = supabase.table('partidos').select('*').order('rueda').order('id_partido').execute().data
    
    if not partidos:
        st.info("No hay partidos programados.")
    else:
        ruedas = sorted(list(set(p.get('rueda', 'Fase de Grupos') for p in partidos if p.get('rueda'))))
        for rueda in ruedas:
            st.header(f"🏆 {rueda}")
            partidos_rueda = [p for p in partidos if p.get('rueda') == rueda]
            
            # Replicando el diseño de Cancha 1 y Cancha 2 de tu manual
            col_c1, col_c2 = st.columns(2)
            
            for p in partidos_rueda:
                cancha_destino = col_c1 if p.get('cancha') == 'Cancha 1' else col_c2
                with cancha_destino:
                    with st.expander(f"{p.get('equipo_local')} vs {p.get('equipo_visitante')} | {p.get('estado', 'Pendiente')}", expanded=True):
                        if st.session_state.es_admin:
                            st.write("*(Modo Edición - Próximamente integrando los campos aquí)*")
                        else:
                            st.markdown(f"<h2 style='text-align: center;'>{p.get('goles_local', 0)} - {p.get('goles_visitante', 0)}</h2>", unsafe_allow_html=True)

# ==========================================
# MÓDULO 2: TABLAS DE POSICIONES
# ==========================================
elif menu == "📊 Tabla de Posiciones":
    st.title("📊 Estadísticas y Clasificación")
    st.write("Aquí irá el motor de cálculo automático de PTS, DG y Fair Play.")
    if st.session_state.es_admin:
        st.button("Generar Tablas Oficiales")

# ==========================================
# MÓDULO 3: PADRÓN OFICIAL DE JUGADORES
# ==========================================
elif menu == "📋 Padrón de Jugadores":
    st.title("📋 Registro Oficial de la Promoción")
    
    if st.session_state.es_admin:
        with st.form("registro_jugador"):
            st.subheader("Añadir Nuevo Integrante")
            col1, col2 = st.columns(2)
            dni = col1.text_input("DNI / CIP")
            nombre = col2.text_input("Nombres y Apellidos")
            seccion = col1.selectbox("Sección / Equipo", ["1ra SEC", "2da SEC", "3ra SEC", "7ma SEC", "9na SEC"])
            sangre = col2.selectbox("Grupo Sanguíneo", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
            
            if st.form_submit_button("Registrar en el Padrón"):
                st.success(f"Registrando a {nombre} en la base de datos...")
                # Próximamente enlazaremos esto a Supabase
    else:
        st.write("El listado de jugadores es de acceso público. (Se mostrará aquí)")
