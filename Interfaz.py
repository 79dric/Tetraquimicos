import streamlit as st
from database import crear_tabla

st.set_page_config(
    page_title="Catálogo médico",
    page_icon="📚",
    layout="wide"
)

crear_tabla()

with st.sidebar.container(border=True):
    st.markdown("### **Universidad Autónoma de Chihuahua**")
    st.markdown("**Facultad de Ciencias Químicas**")
    st.write("**Integrantes:**")
    st.markdown(
        """
        * Brissa Carrasco
        * Audric Gomez
        * Leonardo Martinez
        * Isadora Armendariz
        """)
        
st.title("Catálogo médico")

st.write(
    "Plataforma académica de consulta "
    "de información sanitaria."
)

busqueda = st.text_input(
    "Buscar en el catálogo"
)

categoria = st.selectbox(
    "Seleccionar categoría",
    ["Todas", "Información general", "Prevención", "Salud pública"]
)

if busqueda:
    st.write("Búsqueda:", busqueda)

if categoria != "Todas":
    st.write("Categoría seleccionada:", categoria)
