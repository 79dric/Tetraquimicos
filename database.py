import sqlite3
import os

DB_NAME = "catalogo.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            mecanismo_implicacion TEXT,
            fuente TEXT,
            FOREIGN KEY (id_farmaco1) REFERENCES medicamentos (id),
            FOREIGN KEY (id_farmaco2) REFERENCES medicamentos (id)
        )
    """)
    
    conexion.commit()
    conexion.close()

def obtener_medicamentos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_generico, nombre_comercial, categoria FROM medicamentos ORDER BY nombre_generico")
    datos = cursor.fetchall()
    conexion.close()
    return datos

def consultar_interaccion(id1, id2):
    conexion = conectar()
    cursor = conexion.cursor()
    query = """
    SELECT nivel_riesgo, mecanismo_implicacion, fuente
    FROM interacciones
    WHERE (id_farmaco1 = ? AND id_farmaco2 = ?)
       OR (id_farmaco1 = ? AND id_farmaco2 = ?)
    """
    cursor.execute(query, (id1, id2, id2, id1))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado
