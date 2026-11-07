import streamlit as st
from database import crear_tabla, obtener_medicamentos, consultar_interaccion

st.set_page_config(
    page_title="Interacciones fármaco-fármaco",
    page_icon="💊",
    layout="wide"
)

crear_tabla()

st.title("Consulta de Interacciones fármaco-fármaco sin receta")
st.caption("Plataforma informativa sobre el uso seguro y combinaciones no recomendadas de fármacos de venta libre.")

meds = obtener_medicamentos()
opciones = {f"{m[1]} ({m[2]})": m[0] for m in meds}

st.sidebar.header("Fuentes y Referencias")
st.sidebar.markdown("""
- [DailyMed (NLM)](https://dailymed.nlm.nih.gov/dailymed/index.cfm)
- [DrugBank](https://go.drugbank.com/)
- [Medicamentos PLM](https://www.medicamentosplm.com/)
- [Vademecum](https://www.vademecum.es/)
- [Drugs.com](https://www.drugs.com/)
- [Stabilis](https://www.stabilis.org/)
""")

col1, col2 = st.columns(2)

with col1:
    f1_nombre = st.selectbox("Seleccione medicamento", list(opciones.keys()), key="med1")

with col2:
    f2_nombre = st.selectbox("Seleccione medicamento", list(opciones.keys()), key="med2")

id1 = opciones[f1_nombre]
id2 = opciones[f2_nombre]

if st.button("Verificar Interacción", type="primary"):
    if id1 == id2:
        st.warning("Por favor, seleccione dos medicamentos distintos.")
    else:
        resultado = consultar_interaccion(id1, id2)
        
        st.subheader("Resultado de la Evaluación")
        if resultado:
            riesgo, implicacion, fuente = resultado
            
            if riesgo == "Alto":
                st.error(f"**Riesgo:** {riesgo}")
            elif riesgo == "Moderado":
                st.warning(f"**Riesgo:** {riesgo}")
            else:
                st.info(f"**Riesgo:** {riesgo}")

            st.write(f"**Mecanismo e Implicación Clínica:**\n{implicacion}")
            st.caption(f"**Fuente de Referencia:** {fuente}")
        else:
            st.success("No se encontraron interacciones de alto riesgo documentadas en esta base de datos local para la combinación seleccionada.")
