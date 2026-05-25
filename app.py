import streamlit as st
import pandas as pd
from supabase import create_client

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Gestor Oficial - Promoción Forjadores", page_icon="🏆", layout="wide")

# --- CONEXIÓN A SUPABASE ---
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = init_connection()
    db_conectada = True
except:
    db_conectada = False

# --- SEGURIDAD: MODO VISOR VS MODO MESA DE CONTROL ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Escudo_de_la_Polic%C3%ADa_Nacional_del_Per%C3%BA.png/200px-Escudo_de_la_Polic%C3%ADa_Nacional_del_Per%C3%BA.png", width=100)
    st.title("🔐 Acceso Administrativo")
    st.markdown("El público general ingresa en **Modo Visor** (Solo Lectura).")
    clave_admin = st.text_input("Clave de la Mesa de Control:", type="password")
    es_admin = (clave_admin == "230297")
    
    if es_admin:
        st.success("✅ MODO ADMINISTRADOR ACTIVADO")
    else:
        st.info("👁️ MODO VISOR ACTIVADO")

# --- FUNCIONES DE BASE DE DATOS (LECTURA Y ESCRITURA) ---
def cargar_partidos_nube():
    if not db_conectada: return []
    try:
        res = supabase.table('partidos').select('*').execute()
        return res.data
    except:
        return []

def guardar_partido_nube(datos_partido):
    if not db_conectada: return False
    try:
        supabase.table('partidos').upsert(datos_partido).execute()
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

# --- INICIALIZACIÓN DE DATOS (MEMORIA) ---
equipos_a = ["1ra", "2da", "3ra", "6ta", "7ma", "9na"]
equipos_b = ["4ta", "5ta", "8va", "10ma", "11va", "12va"]
columnas_tabla = ['PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DG', 'Aperturas', 'TA', 'TR', 'Castigo', 'PTS']

# Estructura base de los partidos
partidos_base = [
    {"id_partido": "P1_C1", "fase": "Fase 1", "cancha": "Cancha 1", "equipo_local": "7ma", "equipo_visitante": "3ra", "goles_local": 0, "goles_visitante": 0, "primer_gol": "Ninguno", "amarillas_local": 0, "rojas_local": 0, "amarillas_visitante": 0, "rojas_visitante": 0, "jugado": False},
    {"id_partido": "P2_C1", "fase": "Fase 1", "cancha": "Cancha 1", "equipo_local": "9na", "equipo_visitante": "1ra", "goles_local": 0, "goles_visitante": 0, "primer_gol": "Ninguno", "amarillas_local": 0, "rojas_local": 0, "amarillas_visitante": 0, "rojas_visitante": 0, "jugado": False},
    {"id_partido": "P3_C1", "fase": "Fase 1", "cancha": "Cancha 1", "equipo_local": "2da", "equipo_visitante": "6ta", "goles_local": 0, "goles_visitante": 0, "primer_gol": "Ninguno", "amarillas_local": 0, "rojas_local": 0, "amarillas_visitante": 0, "rojas_visitante": 0, "jugado": False},
    {"id_partido": "P1_C2", "fase": "Fase 1", "cancha": "Cancha 2", "equipo_local": "5ta", "equipo_visitante": "8va", "goles_local": 0, "goles_visitante": 0, "primer_gol": "Ninguno", "amarillas_local": 0, "rojas_local": 0, "amarillas_visitante": 0, "rojas_visitante": 0, "jugado": False},
    {"id_partido": "P2_C2", "fase": "Fase 1", "cancha": "Cancha 2", "equipo_local": "10ma", "equipo_visitante": "11va", "goles_local": 0, "goles_visitante": 0, "primer_gol": "Ninguno", "amarillas_local": 0, "rojas_local": 0, "amarillas_visitante": 0, "rojas_visitante": 0, "jugado": False},
    {"id_partido": "P3_C2", "fase": "Fase 1", "cancha": "Cancha 2", "equipo_local": "4ta", "equipo_visitante": "12va", "goles_local": 0, "goles_visitante": 0, "primer_gol": "Ninguno", "amarillas_local": 0, "rojas_local": 0, "amarillas_visitante": 0, "rojas_visitante": 0, "jugado": False},
]

# Sincronizar memoria con Nube
partidos_nube = cargar_partidos_nube()
dict_nube = {p['id_partido']: p for p in partidos_nube}

for p in partidos_base:
    if p['id_partido'] in dict_nube:
        p.update(dict_nube[p['id_partido']])

st.session_state.partidos_fase1 = partidos_base

# --- LÓGICA DE TABLA Y DESEMPATE OFICIAL ---
def recalcular_tablas():
    df_a = pd.DataFrame(0, index=equipos_a, columns=columnas_tabla)
    df_b = pd.DataFrame(0, index=equipos_b, columns=columnas_tabla)
    
    for p in st.session_state.partidos_fase1:
        if p["jugado"]:
            serie = 'A' if p["equipo_local"] in equipos_a else 'B'
            df = df_a if serie == 'A' else df_b
            
            eq1, eq2 = p["equipo_local"], p["equipo_visitante"]
            g1, g2 = p["goles_local"], p["goles_visitante"]
            
            df.loc[eq1, 'PJ'] += 1; df.loc[eq2, 'PJ'] += 1
            df.loc[eq1, 'GF'] += g1; df.loc[eq1, 'GC'] += g2
            df.loc[eq2, 'GF'] += g2; df.loc[eq2, 'GC'] += g1
            
            if g1 > g2:
                df.loc[eq1, 'PG'] += 1; df.loc[eq1, 'PTS'] += 3; df.loc[eq2, 'PP'] += 1
            elif g1 < g2:
                df.loc[eq2, 'PG'] += 1; df.loc[eq2, 'PTS'] += 3; df.loc[eq1, 'PP'] += 1
            else:
                df.loc[eq1, 'PE'] += 1; df.loc[eq2, 'PE'] += 1; df.loc[eq1, 'PTS'] += 1; df.loc[eq2, 'PTS'] += 1
            
            if p["primer_gol"] == "Local": df.loc[eq1, 'Aperturas'] += 1
            elif p["primer_gol"] == "Visitante": df.loc[eq2, 'Aperturas'] += 1
            
            df.loc[eq1, 'TA'] += p['amarillas_local']; df.loc[eq1, 'TR'] += p['rojas_local']
            df.loc[eq2, 'TA'] += p['amarillas_visitante']; df.loc[eq2, 'TR'] += p['rojas_visitante']
            
    for df in [df_a, df_b]:
        df['DG'] = df['GF'] - df['GC']
        df['Castigo'] = (df['TA'] * 1) + (df['TR'] * 3)
    
    df_a = df_a.sort_values(by=['PTS', 'DG', 'GF', 'Aperturas', 'Castigo'], ascending=[False, False, False, False, True])
    df_b = df_b.sort_values(by=['PTS', 'DG', 'GF', 'Aperturas', 'Castigo'], ascending=[False, False, False, False, True])
    return df_a, df_b

# --- INTERFAZ VISUAL ---
st.title("🏆 Campeonato Relámpago - Promoción Forjadores")
st.markdown("Sede: **Casino de Policía** | Algoritmo ajustado al **Manual Oficial de Reglas**.")
st.markdown("---")

t_fase1, t_fase2, t_fase3 = st.tabs(["1️⃣ FASE 1: Grupos", "2️⃣ FASE 2: Repechaje", "3️⃣ FASE 3: Eliminatorias"])

# ========================================================
# PESTAÑA 1: FASE 1
# ========================================================
with t_fase1:
    col_c1, col_c2 = st.columns(2)
    
    def render_partido(i, p):
        with st.expander(f"[{p['cancha']}] {p['equipo_local']} vs {p['equipo_visitante']}", expanded=not p['jugado']):
            if es_admin:
                c1, c2, c3 = st.columns([2,1,2])
                with c1:
                    g1 = st.number_input(f"Goles {p['equipo_local']}", 0, 20, p['goles_local'], key=f"g1_{p['id_partido']}")
                    ta1 = st.number_input("T. Amarillas", 0, 10, p['amarillas_local'], key=f"ta1_{p['id_partido']}")
                    tr1 = st.number_input("T. Rojas", 0, 5, p['rojas_local'], key=f"tr1_{p['id_partido']}")
                with c2:
                    st.markdown("<h3 style='text-align:center;'>VS</h3>", unsafe_allow_html=True)
                with c3:
                    g2 = st.number_input(f"Goles {p['equipo_visitante']}", 0, 20, p['goles_visitante'], key=f"g2_{p['id_partido']}")
                    ta2 = st.number_input("T. Amarillas", 0, 10, p['amarillas_visitante'], key=f"ta2_{p['id_partido']}")
                    tr2 = st.number_input("T. Rojas", 0, 5, p['rojas_visitante'], key=f"tr2_{p['id_partido']}")
                
                primer_gol = st.selectbox("¿Quién anotó el 1er gol? (Apertura)", ["Ninguno", "Local", "Visitante"], 
                                          index=["Ninguno", "Local", "Visitante"].index(p['primer_gol']), key=f"pg_{p['id_partido']}")
                jugado = st.checkbox("Sellar Partido", value=p['jugado'], key=f"chk_{p['id_partido']}")
                
                # Botón de Guardado en Nube
                if st.button("💾 Guardar Resultado en Nube", key=f"btn_{p['id_partido']}", use_container_width=True):
                    datos_actualizados = {
                        "id_partido": p['id_partido'], "fase": p['fase'], "cancha": p['cancha'],
                        "equipo_local": p['equipo_local'], "equipo_visitante": p['equipo_visitante'],
                        "goles_local": g1, "goles_visitante": g2, "primer_gol": primer_gol,
                        "amarillas_local": ta1, "rojas_local": tr1, "amarillas_visitante": ta2, "rojas_visitante": tr2,
                        "jugado": jugado
                    }
                    if guardar_partido_nube(datos_actualizados):
                        st.success("¡Guardado en la base de datos oficial!")
                        st.rerun()

            else:
                st.markdown(f"<h2 style='text-align:center;'>{p['goles_local']} - {p['goles_visitante']}</h2>", unsafe_allow_html=True)
                if p['jugado']:
                    st.success("✅ Partido Finalizado Oficialmente")
                    st.write(f"**Apertura:** {p['primer_gol']} | **Tarjetas {p['equipo_local']}:** {p['amarillas_local']}A {p['rojas_local']}R | **Tarjetas {p['equipo_visitante']}:** {p['amarillas_visitante']}A {p['rojas_visitante']}R")
                else:
                    st.warning("⏳ Pendiente o En Juego")

    with col_c1:
        st.subheader("Serie A (Cancha 1)")
        for i, p in enumerate(st.session_state.partidos_fase1[:3]): render_partido(i, p)

    with col_c2:
        st.subheader("Serie B (Cancha 2)")
        for i, p in enumerate(st.session_state.partidos_fase1[3:]): render_partido(i+3, p)

    st.markdown("---")
    st.header("📊 Tabla de Posiciones Oficial")
    df_a, df_b = recalcular_tablas()
    
    col_ta, col_tb = st.columns(2)
    with col_ta:
        st.subheader("🟢 SERIE A")
        st.dataframe(df_a, use_container_width=True)
        top_a = list(df_a.index)
        st.success(f"🎟️ Cuartos de Final (Directo): **{top_a[0]}**")
        st.error(f"❌ Eliminado: **{top_a[5]}**")
        
    with col_tb:
        st.subheader("🔵 SERIE B")
        st.dataframe(df_b, use_container_width=True)
        top_b = list(df_b.index)
        st.success(f"🎟️ Cuartos de Final (Directo): **{top_b[0]}**")
        st.error(f"❌ Eliminado: **{top_b[5]}**")

# ========================================================
# PESTAÑA 2 y 3: ESTRUCTURA LISTA PARA AUTOMATIZAR
# ========================================================
with t_fase2:
    st.header("⚔️ FASE 2: Segunda Rueda (Repechaje Cruzado)")
    cruzado_a = [f"2°A ({top_a[1]}) vs 5°B ({top_b[4]})", f"4°A ({top_a[3]}) vs 3°B ({top_b[2]})"]
    cruzado_b = [f"2°B ({top_b[1]}) vs 5°A ({top_a[4]})", f"4°B ({top_b[3]}) vs 3°A ({top_a[2]})"]
    
    col_ra, col_rb = st.columns(2)
    with col_ra:
        st.info("Llaves hacia Serie A")
        for match in cruzado_a: st.markdown(f"- **{match}**")
    with col_rb:
        st.info("Llaves hacia Serie B")
        for match in cruzado_b: st.markdown(f"- **{match}**")

with t_fase3:
    st.header("🔥 FASE 3: Cuartos, Semis y Final")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Tournament_Bracket_8.svg/1024px-Tournament_Bracket_8.svg.png", width=500)
