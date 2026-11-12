import json
import os
import sqlite3

DB_NAME = "catalogo.db"
JSON_FILE = "medicamentos.json"


def conectar():
    return sqlite3.connect(DB_NAME)


def inicializar_biblioteca():
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY,
            nombre_generico TEXT NOT NULL,
            nombre_comercial TEXT,
            categoria TEXT,
            descripcion TEXT,
            fuente_referencia TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_farmaco1 INTEGER,
            id_farmaco2 INTEGER,
            nivel_riesgo TEXT,
            horas_separacion INTEGER,
            mecanismo_implicacion TEXT,
            fuente TEXT
        )
    """)

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for med in data.get("medicamentos", []):
            cursor.execute(
                """
                    INSERT OR IGNORE INTO medicamentos (
                        id, nombre_generico, nombre_comercial, categoria, descripcion, fuente_referencia
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    med["id"],
                    med["nombre_generico"],
                    med["nombre_comercial"],
                    med["categoria"],
                    med["descripcion"],
                    med["fuente"],
                ),
            )

        for inter in data.get("interacciones", []):
            cursor.execute(
                """
                    INSERT OR IGNORE INTO interacciones (
                        id_farmaco1, id_farmaco2, nivel_riesgo, horas_separacion,
                        mecanismo_implicacion, fuente
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    inter["id_farmaco1"],
                    inter["id_farmaco2"],
                    inter["nivel_riesgo"],
                    inter.get("horas_separacion"),
                    inter["mecanismo"],
                    inter["fuente"],
                ),
            )

    conexion.commit()
    conexion.close()
    
    def obtener_medicamentos():
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, nombre_generico, nombre_comercial, categoria FROM medicamentos ORDER BY nombre_generico"
    )
    datos = cursor.fetchall()
    conexion.close()
    return datos


def consultar_interaccion(id1, id2):
    conexion = conectar()
    cursor = conexion.cursor()

    query = """
        SELECT nivel_riesgo, mecanismo_implicacion, fuente, horas_separacion
        FROM interacciones
        WHERE (id_farmaco1 = ? AND id_farmaco2 = ?)
           OR (id_farmaco1 = ? AND id_farmaco2 = ?)
    """
    cursor.execute(query, (id1, id2, id2, id1))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado
