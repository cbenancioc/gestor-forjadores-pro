import streamlit as st

st.set_page_config(page_title="Gestor Forjadores PRO", layout="wide")

st.title("⚽ Campeonato Relámpago Forjadores")

# --- PANEL LATERAL ---
with st.sidebar:
    st.title("🔐 Acceso")
    clave = st.text_input("Clave:", type="password")

# --- RENDERIZADO DE EMERGENCIA ---
# Aquí dibujamos algo simple para verificar que el código SÍ está actualizando
st.write("---")
st.subheader("Estado del Sistema")
st.info("El sistema está operativo. Si no ves partidos, es un problema de carga de datos.")

# Simulamos una lista de partidos para forzar el dibujo
partidos = [
    {"equipo_local": "7ma SEC", "equipo_visitante": "3ra SEC", "goles_local": 0, "goles_visitante": 0},
    {"equipo_local": "9na SEC", "equipo_visitante": "1ra SEC", "goles_local": 0, "goles_visitante": 0}
]

for p in partidos:
    with st.container(border=True):
        st.write(f"### {p['equipo_local']} vs {p['equipo_visitante']}")
        st.write(f"Marcador: {p['goles_local']} - {p['goles_visitante']}")
