import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

# Conexión
supabase = create_client("https://jevlhjtviawzripepfoh.supabase.co", "sb_publishable_bmj25yLy8yE7cuYJc-N-kA_g_IvM2iS")

st.title("⚽ Campeonato Relámpago Forjadores")

# --- CARGAR TODO EL FIXTURE ---
# Eliminamos filtros para traer toda la tabla
try:
    partidos = supabase.table('partidos').select('*').order('rueda,fecha_nro,id').execute().data
except Exception as e:
    st.error(f"Error cargando el fixture: {e}")
    partidos = []

# --- LÓGICA DE VISUALIZACIÓN JERÁRQUICA ---
if not partidos:
    st.warning("El fixture está vacío. ¡Carga tus partidos en el Table Editor!")
else:
    # Obtener todas las ruedas únicas existentes en tu tabla
    ruedas = sorted(list(set(p['rueda'] for p in partidos if p.get('rueda'))))
    
    for rueda in ruedas:
        st.header(f"🏆 {rueda}")
        # Filtrar fechas dentro de esta rueda
        partidos_rueda = [p for p in partidos if p['rueda'] == rueda]
        fechas = sorted(list(set(p['fecha_nro'] for p in partidos_rueda if p.get('fecha_nro'))))
        
        for fecha in fechas:
            with st.expander(f"📅 Fecha {fecha}", expanded=True):
                partidos_fecha = [p for p in partidos_rueda if p['fecha_nro'] == fecha]
                for p in partidos_fecha:
                    # Dibujar cada partido
                    with st.container(border=True):
                        st.write(f"**{p.get('eq1')}** vs **{p.get('eq2')}** | 🏟️ {p.get('cancha', 'N/A')}")
                        st.metric("Marcador", f"{p.get('g1', 0)} - {p.get('g2', 0)}")
