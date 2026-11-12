import streamlit as st
from database import inicializar_biblioteca, obtener_medicamentos, consultar_interaccion

st.set_page_config(page_title="Medicamentos sin Receta e Interacciones", page_icon="💊", layout="wide")

inicializar_biblioteca()

st.title("Medicamentos sin Receta e Interacciones")
st.write("Consulta rápida de combinaciones fármaco-fármaco basadas en referencias oficiales.")

meds = obtener_medicamentos()
opciones = {f"{m[1]} ({m[2]})": m[0] for m in meds}

if not opciones:
    st.warning("⚠️ No se encontraron medicamentos en la biblioteca.")
else:
    col1, col2 = st.columns(2)
    
    with col1:
        f1_nombre = st.selectbox("Primer Medicamento:", ["Selecciona una opción"] + list(opciones.keys()), key="med1")
        
    with col2:
        f2_nombre = st.selectbox("Segundo Medicamento:", ["Selecciona una opción"] + list(opciones.keys()), key="med2")

    if f1_nombre != "Selecciona una opción" and f2_nombre != "Selecciona una opción":
        id1 = opciones[f1_nombre]
        id2 = opciones[f2_nombre]
        
        if st.button("Verificar Interacción", type="primary"):
            if id1 == id2:
                st.warning("Por favor, selecciona dos medicamentos distintos.")
            else:
                resultado = consultar_interaccion(id1, id2)
                
                st.subheader("Resultado de la Evaluación")
                if resultado:
                    if len(resultado) == 4:
                        riesgo, implicacion, fuente, horas_separacion = resultado
                    else:
                        riesgo, implicacion, fuente = resultado
                        horas_separacion = None
                    
                    if riesgo == "Alto":
                        st.error(f"**Riesgo:** {riesgo}")
                    elif riesgo == "Moderado":
                        st.warning(f"**Riesgo:** {riesgo}")
                    else:
                        st.info(f"**Riesgo:** {riesgo}")
                    
                    st.write(f"**Mecanismo e Implicación:**\n{implicacion}")
                    
                    if riesgo == "Leve" and horas_separacion:
                        st.markdown(f"⏱️ **Recomendación clínica:** Se sugiere separar la administración de ambos medicamentos por un intervalo mínimo de **{horas_separacion} horas**.")
                        
                    st.caption(f"**Fuente:** {fuente}")
                else:
                    st.success("No se encontraron interacciones de riesgo registradas para esta combinación en la biblioteca.")
    else:
        st.info("Selecciona ambos medicamentos para hacer la consulta.")
