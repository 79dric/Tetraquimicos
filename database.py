import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "catalogo.db"
JSON_FILE = BASE_DIR / "medicamentos.json"


def conectar():
    return sqlite3.connect(DB_NAME)


def inicializar_biblioteca():
    conexion = conectar()
    try:
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

        if JSON_FILE.exists():
            with JSON_FILE.open("r", encoding="utf-8") as archivo:
                data = json.load(archivo)

            for med in data.get("medicamentos", []):
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO medicamentos (
                        id, nombre_generico, nombre_comercial, categoria,
                        descripcion, fuente_referencia
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        med["id"],
                        med["nombre_generico"],
                        med.get("nombre_comercial"),
                        med.get("categoria"),
                        med.get("descripcion"),
                        med.get("fuente"),
                    ),
                )

            for inter in data.get("interacciones", []):
                cursor.execute(
                    """
                    INSERT INTO interacciones (
                        id_farmaco1, id_farmaco2, nivel_riesgo,
                        horas_separacion, mecanismo_implicacion, fuente
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        inter["id_farmaco1"],
                        inter["id_farmaco2"],
                        inter["nivel_riesgo"],
                        inter.get("horas_separacion"),
                        inter["mecanismo"],
                        inter.get("fuente"),
                    ),
                )

        conexion.commit()
    finally:
        conexion.close()


def obtener_medicamentos():
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT id, nombre_generico, nombre_comercial, categoria
            FROM medicamentos
            ORDER BY nombre_generico
            """
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def consultar_interaccion(id1, id2):
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT nivel_riesgo, mecanismo_implicacion, fuente, horas_separacion
            FROM interacciones
            WHERE (id_farmaco1 = ? AND id_farmaco2 = ?)
               OR (id_farmaco1 = ? AND id_farmaco2 = ?)
            """,
            (id1, id2, id2, id1),
        )
        return cursor.fetchone()
    finally:
        conexion.close()
