import streamlit as st
input_container = st.container()
with input_container:
    user_input =st.chat_input("¿Qué medicamento desea utilizar?")
st.write("**Consulte a su medico*")
st.sidebar.button("Inicio")
st.sidebar.button("Receta")
st.sidebar.text("Brissa Aracely Carrasco Iglesias 395007")
st.sidebar.text("Alejandra G. Rivera Chávez 358006")
st.sidebar.text("Isadora Armendariz")
st.sidebar.text("Leonardo Eusebio Martinez")
st.sidebar.text("Audric Lorenzo Gómez Carrera 394911")
opcion_menu = st.radio(
        label="Menu",
        options=["🏠 Inicio", "💬 Sala de Chat", "⚙️ Configuración"],
        label_visibility="collapsed"
