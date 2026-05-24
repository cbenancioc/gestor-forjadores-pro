import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Configuración de la página
st.set_page_config(
    page_title="Gestor de Fulbito - Promoción Forjadores", 
    page_icon="⚽", 
    layout="wide"
)

# --- CONFIGURACIÓN DE SUPABASE ---
SUPABASE_URL = "https://jevlhjtviawzripepfoh.supabase.co"
SUPABASE_KEY = "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

@st.cache_data(ttl=60) # Refresca los datos cada 60 segundos
def cargar_jugadores():
    try:
        response = supabase.table('jugadores').select('*').execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error conectando a Supabase: {e}")
        return pd.DataFrame(columns=['id', 'nombres', 'equipo', 'condicion'])

df_jugadores = cargar_jugadores()

# Diccionario para traducir los nombres de Streamlit al formato de Supabase
MAPEO_EQUIPOS = {
    "1RA SEC": "1ra", "2DA. SEC": "2da", "3RA SEC": "3ra",
    "4TA  SEC": "4ta", "5TA SEC": "5ta", "6TA SEC": "6ta",
    "7MA SEC": "7ma", "8VA SEC": "8va", "9NA SEC": "9na",
    "10MA SEC": "10ma", "11AVA SEC": "11va", "12AVA SEC": "12va"
}

# --- INICIALIZACIÓN DE DATOS (ESTADO DE LA APP) ---
if 'equipos_a' not in st.session_state:
    st.session_state.equipos_a = ["1RA SEC", "2DA. SEC", "3RA SEC", "6TA SEC", "7MA SEC", "9NA SEC"]
if 'equipos_b' not in st.session_state:
    st.session_state.equipos_b = ["4TA  SEC", "5TA SEC", "8VA SEC", "10MA SEC", "11AVA SEC", "12AVA SEC"]

columnas = ['PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DG', 'PTS']

if 'tabla_a' not in st.session_state:
    st.session_state.tabla_a = pd.DataFrame(0, index=st.session_state.equipos_a, columns=columnas)
if 'tabla_b' not in st.session_state:
    st.session_state.tabla_b = pd.DataFrame(0, index=st.session_state.equipos_b, columns=columnas)

if 'partidos_rueda1' not in st.session_state:
    st.session_state.partidos_rueda1 = [
        {"cancha": "Cancha 1", "id": "P1_C1", "eq1": "7MA SEC", "eq2": "3RA SEC", "g1": 0, "g2": 0, "jugado": False, "goleadores_eq1": [], "goleadores_eq2": [], "mvp": None},
        {"cancha": "Cancha 1", "id": "P2_C1", "eq1": "9NA SEC", "eq2": "1RA SEC", "g1": 0, "g2": 0, "jugado": False, "goleadores_eq1": [], "goleadores_eq2": [], "mvp": None},
        {"cancha": "Cancha 1", "id": "P3_C1", "eq1": "2DA. SEC", "eq2": "6TA SEC", "g1": 0, "g2": 0, "jugado": False, "goleadores_eq1": [], "goleadores_eq2": [], "mvp": None},
        {"cancha": "Cancha 2", "id": "P1_C2", "eq1": "5TA SEC", "eq2": "8VA SEC", "g1": 0, "g2": 0, "jugado": False, "goleadores_eq1": [], "goleadores_eq2": [], "mvp": None},
        {"cancha": "Cancha 2", "id": "P2_C2", "eq1": "10MA SEC", "eq2": "11AVA SEC", "g1": 0, "g2": 0, "jugado": False, "goleadores_eq1": [], "goleadores_eq2": [], "mvp": None},
        {"cancha": "Cancha 2", "id": "P3_C2", "eq1": "4TA  SEC", "eq2": "12AVA SEC", "g1": 0, "g2": 0, "jugado": False, "goleadores_eq1": [], "goleadores_eq2": [], "mvp": None},
    ]

# --- FUNCIONES DE LÓGICA ---
def obtener_jugadores(equipo_streamlit):
    equipo_supa = MAPEO_EQUIPOS.get(equipo_streamlit, "")
    if not df_jugadores.empty:
        df_filtrado = df_jugadores[df_jugadores['equipo'] == equipo_supa]
        return df_filtrado['nombres'].tolist()
    return []

def recalcular_tablas():
    st.session_state.tabla_a = pd.DataFrame(0, index=st.session_state.equipos_a, columns=columnas)
    st.session_state.tabla_b = pd.DataFrame(0, index=st.session_state.equipos_b, columns=columnas)
    
    for p in st.session_state.partidos_rueda1:
        if p["jugado"]:
            serie = 'A' if p["eq1"] in st.session_state.equipos_a else 'B'
            df = st.session_state.tabla_a if serie == 'A' else st.session_state.tabla_b
            
            eq1, eq2 = p["eq1"], p["eq2"]
            g1, g2 = p["g1"], p["g2"]
            
            df.loc[eq1, 'PJ'] += 1
            df.loc[eq2, 'PJ'] += 1
            df.loc[eq1, 'GF'] += g1
            df.loc[eq1, 'GC'] += g2
            df.loc[eq2, 'GF'] += g2
            df.loc[eq2, 'GC'] += g1
            
            if g1 > g2:
                df.loc[eq1, 'PG'] += 1
                df.loc[eq1, 'PTS'] += 3
                df.loc[eq2, 'PP'] += 1
            elif g1 < g2:
                df.loc[eq2, 'PG'] += 1
                df.loc[eq2, 'PTS'] += 3
                df.loc[eq1, 'PP'] += 1
            else:
                df.loc[eq1, 'PE'] += 1
                df.loc[eq2, 'PE'] += 1
                df.loc[eq1, 'PTS'] += 1
                df.loc[eq2, 'PTS'] += 1
                
    st.session_state.tabla_a['DG'] = st.session_state.tabla_a['GF'] - st.session_state.tabla_a['GC']
    st.session_state.tabla_b['DG'] = st.session_state.tabla_b['GF'] - st.session_state.tabla_b['GC']
    
    st.session_state.tabla_a = st.session_state.tabla_a.sort_values(by=['PTS', 'DG', 'GF'], ascending=False)
    st.session_state.tabla_b = st.session_state.tabla_b.sort_values(by=['PTS', 'DG', 'GF'], ascending=False)


# --- INTERFAZ VISUAL ---
st.title("⚽ Campeonato Relámpago - Promoción Forjadores")
st.subheader("Sistema Central de Tiempos, Resultados y Estadísticas")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Primera Rueda", "📊 Tabla de Posiciones", "🔄 Segunda Rueda", "⭐ Estadísticas y Premios"])

# ========================================================
# PESTAÑA 1: GESTIÓN DE PARTIDOS
# ========================================================
with tab1:
    st.header("🎯 Registro de Marcadores y Sucesos")
    col_c1, col_c2 = st.columns(2)
    
    def render_partido(i, p):
        with st.expander(f"Partido {i+1}: {p['eq1']} vs {p['eq2']}", expanded=not p['jugado']):
            c_g1, c_vs, c_g2 = st.columns([2, 1, 2])
            with c_g1:
                g1 = st.number_input(f"Goles {p['eq1']}", min_value=0, step=1, key=f"g1_{p['id']}", value=p['g1'])
            with c_vs:
                st.markdown("<h3 style='text-align: center; margin-top: 25px;'>VS</h3>", unsafe_allow_html=True)
            with c_g2:
                g2 = st.number_input(f"Goles {p['eq2']}", min_value=0, step=1, key=f"g2_{p['id']}", value=p['g2'])
            
            # --- SECCIÓN DE ESTADÍSTICAS DEL PARTIDO ---
            if g1 > 0 or g2 > 0:
                st.markdown("**⚽ Asignación de Goles:**")
                jugadores_eq1 = obtener_jugadores(p['eq1'])
                jugadores_eq2 = obtener_jugadores(p['eq2'])
                
                col_goles1, col_goles2 = st.columns(2)
                p["goleadores_eq1"] = []
                p["goleadores_eq2"] = []
                
                with col_goles1:
                    for num in range(g1):
                        goleador = st.selectbox(f"Gol {num+1} ({p['eq1']})", ["Desconocido/Autogol"] + jugadores_eq1, key=f"sel_g1_{p['id']}_{num}")
                        if goleador != "Desconocido/Autogol":
                            p["goleadores_eq1"].append(goleador)
                
                with col_goles2:
                    for num in range(g2):
                        goleador = st.selectbox(f"Gol {num+1} ({p['eq2']})", ["Desconocido/Autogol"] + jugadores_eq2, key=f"sel_g2_{p['id']}_{num}")
                        if goleador != "Desconocido/Autogol":
                            p["goleadores_eq2"].append(goleador)
            
            st.markdown("**🌟 MVP del Partido:**")
            todos_jugadores = obtener_jugadores(p['eq1']) + obtener_jugadores(p['eq2'])
            mvp_seleccionado = st.selectbox("Seleccione al jugador destacado", ["Ninguno aún"] + todos_jugadores, key=f"mvp_{p['id']}")
            p["mvp"] = mvp_seleccionado if mvp_seleccionado != "Ninguno aún" else None

            jugado = st.checkbox("Finalizar Partido (Afecta Tabla)", key=f"chk_{p['id']}", value=p['jugado'])
            p["g1"], p["g2"], p["jugado"] = g1, g2, jugado

    with col_c1:
        st.subheader("🏟️ CANCHA 1")
        for i, p in enumerate(st.session_state.partidos_rueda1):
            if p["cancha"] == "Cancha 1": render_partido(i, p)

    with col_c2:
        st.subheader("🏟️ CANCHA 2")
        for i, p in enumerate(st.session_state.partidos_rueda1):
            if p["cancha"] == "Cancha 2": render_partido(i, p)

    recalcular_tablas()

# ========================================================
# PESTAÑA 2: TABLAS DE POSICIONES
# ========================================================
with tab2:
    st.header("📊 Tablas de Posiciones en Tiempo Real")
    col_ta, col_tb = st.columns(2)
    with col_ta:
        st.subheader("🟢 SERIE A")
        st.dataframe(st.session_state.tabla_a, use_container_width=True)
    with col_tb:
        st.subheader("🔵 SERIE B")
        st.dataframe(st.session_state.tabla_b, use_container_width=True)

# ========================================================
# PESTAÑA 3: SEGUNDA RUEDA
# ========================================================
with tab3:
    st.header("🔄 Configuración Automática - SEGUNDA RUEDA")
    top_a = list(st.session_state.tabla_a.index)
    top_b = list(st.session_state.tabla_b.index)
    
    try:
        nueva_serie_a = [f"1°B ({top_b[0]})", f"2°A ({top_a[1]})", f"3°B ({top_b[2]})", f"4°A ({top_a[3]})", f"5°B ({top_b[4]})"]
        nueva_serie_b = [f"1°A ({top_a[0]})", f"2°B ({top_b[1]})", f"3°A ({top_a[2]})", f"4°B ({top_b[3]})", f"5°A ({top_a[4]})"]
    except IndexError:
        nueva_serie_a = ["Esperando resultados..."] * 5
        nueva_serie_b = ["Esperando resultados..."] * 5

    st.info("💡 El sistema redistribuye las series intercaladamente para garantizar equilibrio deportivo.")
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.success("🔥 NUEVA SERIE A")
        for idx, team in enumerate(nueva_serie_a): st.markdown(f"**Posición {idx+1}:** {team}")
    with col_n2:
        st.info("🔥 NUEVA SERIE B")
        for idx, team in enumerate(nueva_serie_b): st.markdown(f"**Posición {idx+1}:** {team}")

# ========================================================
# PESTAÑA 4: ESTADÍSTICAS Y PREMIOS
# ========================================================
with tab4:
    st.header("🏆 Reconocimientos del Campeonato")
    col_stat1, col_stat2, col_stat3 = st.columns(3)

    # 1. Procesar Goleadores
    todos_los_goles = []
    lista_mvps = []
    for p in st.session_state.partidos_rueda1:
        if p['jugado']:
            todos_los_goles.extend(p['goleadores_eq1'])
            todos_los_goles.extend(p['goleadores_eq2'])
            if p['mvp']: lista_mvps.append(p['mvp'])

    with col_stat1:
        st.subheader("⚽ Máximos Artilleros")
        if todos_los_goles:
            df_goles = pd.Series(todos_los_goles).value_counts().reset_index()
            df_goles.columns = ['Jugador', 'Goles']
            st.dataframe(df_goles, hide_index=True, use_container_width=True)
        else:
            st.caption("Aún no hay goles registrados asignados a jugadores.")

    # 2. Valla Menos Batida
    with col_stat2:
        st.subheader("🧤 El Guante de Oro")
        if not df_jugadores.empty:
            df_arqueros = df_jugadores[df_jugadores['condicion'] == 'Arquero'].copy()
            if not df_arqueros.empty:
                # Unir tabla global para buscar PJ y GC
                tabla_global = pd.concat([st.session_state.tabla_a, st.session_state.tabla_b])
                
                # Traducir los nombres de equipo de Supabase al formato de Streamlit
                inv_mapeo = {v: k for k, v in MAPEO_EQUIPOS.items()}
                
                stats_arqueros = []
                for _, row in df_arqueros.iterrows():
                    equipo_st = inv_mapeo.get(row['equipo'])
                    if equipo_st in tabla_global.index:
                        pj = tabla_global.loc[equipo_st, 'PJ']
                        gc = tabla_global.loc[equipo_st, 'GC']
                        if pj > 0:
                            coef = round(gc / pj, 2)
                            stats_arqueros.append({'Arquero': row['nombres'], 'Equipo': row['equipo'].upper(), 'PJ': pj, 'GC': gc, 'Coef.': coef})
                
                if stats_arqueros:
                    df_stats_arq = pd.DataFrame(stats_arqueros).sort_values(by=['Coef.', 'PJ'], ascending=[True, False])
                    st.dataframe(df_stats_arq, hide_index=True, use_container_width=True)
                    st.caption("Fórmula: Coeficiente = Goles en Contra (GC) / Partidos Jugados (PJ).")
                else:
                    st.caption("Los arqueros aún no han jugado partidos.")
            else:
                st.caption("No hay arqueros inscritos en el padrón oficial.")
        else:
            st.caption("Esperando conexión con el padrón general.")

    # 3. MVP
    with col_stat3:
        st.subheader("🌟 Mejor Jugador (MVP)")
        if lista_mvps:
            df_mvp = pd.Series(lista_mvps).value_counts().reset_index()
            df_mvp.columns = ['Jugador', 'Estrellas']
            st.dataframe(df_mvp, hide_index=True, use_container_width=True)
        else:
            st.caption("No se han asignado estrellas MVP.")