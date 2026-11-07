from database import conectar, crear_tabla

def poblar_datos_ejemplo():
  crear_tabla()
  conexion = conectar()

medicamentos = [
        ("Ibuprofeno", "Advil, Motrin", "Antiinflamatorio (AINE)", "Alivio del dolor y fiebre", "https://go.drugbank.com/drugs/DB01050"),
        ("Paracetamol / Acetaminofén", "Tylenol", "Analgésico / Antipirético", "Control de dolor moderado y fiebre", "https://www.drugs.com/acetaminophen.html"),
        ("Ácido Acetilsalicílico", "Aspirina", "AINE / Antiagregante", "Alivio sintomático del dolor, fiebre e inflamación", "https://www.medicamentosplm.com/"),
        ("Omeprazol", "Losec", "Inhibidor de la bomba de protones", "Gastritis y reflujo gastroesofágico", "https://www.vademecum.es/")
    ]

cursor.executemany("""
INSERT OR IGNORE INTO medicamentos (nombre_generico, nombre_comercial, categoria, indicacion, fuente_referencia)
VALUES (?, ?, ?, ?, ?)
""", medicamentos)

interacciones = [
        (1, 3, "Alto", "El uso concomitante disminuye el efecto antiagregante de la aspirina y aumenta considerablemente el riesgo de úlceras o sangrado gastrointestinal.", "Drugs.com / DailyMed"),
        (1, 2, "Leve", "En dosis habituales no presentan interacción grave, pero el uso prolongado concomitante requiere monitoreo renal/hepático.", "Vademecum / PLM")
    ]

cursor.executemany("""
    INSERT OR IGNORE INTO interacciones (id_farmaco1, id_farmaco2, nivel_riesgo, mecanismo_implicacion, fuente)
    VALUES (?, ?, ?, ?, ?)
    """, interacciones)

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    poblar_datos_ejemplo()
    print("Base de datos configurada con éxito.")
