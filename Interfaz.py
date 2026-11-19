import streamlit as st
from database import inicializar_biblioteca, obtener_medicamentos, consultar_interaccion

st.set_page_config(page_title="Medicamentos sin Receta e Interacciones", page_icon="💊", layout="wide")

inicializar_biblioteca()

st.title("Medicamentos sin Receta e Interacciones")
st.write("Consulta rápida de combinaciones fármaco-fármaco basadas en referencias oficiales. Para usos informativos, no sustituye atención médica.")
st.sidebar.write("Facultad de Ciencias Químicas - Universidad Autónoma de Chihuahua - Programación 3°L Tetraquímicos")

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
"glosario": {
    "INR (Índice Internacional Normalizado)": "Prueba de laboratorio que mide qué tan rápido coagula la sangre; se usa sobre todo para controlar anticoagulantes como la warfarina o el acenocumarol. Un INR más alto significa que la sangre tarda más en coagular y hay mayor riesgo de sangrado.",
    "tiempo de protrombina": "Tiempo que tarda el plasma sanguíneo en formar un coágulo en una prueba de laboratorio; ayuda a evaluar la actividad de ciertos factores de coagulación.",
    "factores de coagulación": "Proteínas de la sangre que actúan en cadena para detener el sangrado y formar un coágulo; varios (como II, VII, IX y X) dependen de la vitamina K para activarse.",
    "anticoagulante": "Medicamento que dificulta o retrasa la formación de coágulos de sangre para prevenir trombosis o embolias.",
    "cumarínico": "Tipo de anticoagulante oral (como warfarina o acenocumarol) que actúa interfiriendo con el reciclaje de la vitamina K en el hígado.",
    "anticoagulante oral directo": "Anticoagulante que bloquea directamente un factor específico de la coagulación (como el factor Xa en el caso del rivaroxabán) sin depender de la vitamina K.",
    "antiagregante plaquetario": "Fármaco que evita que las plaquetas se agrupen y formen coágulos (por ejemplo, aspirina o clopidogrel).",
    "antifúngico triazólico": "Medicamento que combate infecciones por hongos bloqueando la síntesis de ergosterol en la membrana celular del hongo.",
    "inhibidor selectivo de la recaptación de serotonina (ISRS)": "Tipo de antidepresivo (como la sertralina) que aumenta la disponibilidad de serotonina en el espacio entre neuronas para regular el estado de ánimo.",
    "benzodiacepina": "Grupo de fármacos (como clonazepam, alprazolam o diazepam) que calman el sistema nervioso central y tienen efectos ansiolíticos, sedantes, relajantes musculares o anticonvulsivos.",
    "receptores GABA-A": "Sitios de unión en las neuronas del cerebro donde actúa el neurotransmisor GABA para frenar la actividad eléctrica excesiva, produciendo calma, relajación o sedación.",
    "hiperpolarización": "Cambio en el voltaje eléctrico de una neurona que la vuelve menos propensa a disparar impulsos nerviosos, reduciendo la excitabilidad neuronal.",
    "inhibición enzimática": "Reducción o bloqueo de la actividad de una enzima (como las del citocromo P450 o CYP2C9), lo que puede hacer que otro fármaco se elimine más lento y suba su nivel en la sangre.",
    "inducción enzimática": "Aumento en la producción o actividad de enzimas metabólicas (principalmente en el hígado), lo que suele acelerar la eliminación de un fármaco y bajar su efecto.",
    "hepatotoxicidad": "Daño o lesión en las células del hígado causada por sustancias, medicamentos o alcohol.",
    "hemorragia gastrointestinal": "Sangrado en alguna parte del tubo digestivo (esófago, estómago o intestinos), que puede verse favorecido por irritación de la mucosa o alteraciones de la coagulación."
  }
