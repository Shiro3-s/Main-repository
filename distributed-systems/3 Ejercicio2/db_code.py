import mysql.connector as msql
from mysql.connector import Error
# ... (importaciones existentes)

try:
    connection = msql.connect(
        host="localhost",   # Servidor
        port=3306,          # Puerto (cambiado a entero)
        user="root",        # Usuario de MySQL
        password=""         # Contraseña MySQL
    )

    
    if connection.is_connected():
        cursor = connection.cursor()
        # Crear la base de datos (si no existe)
        cursor.execute("CREATE DATABASE IF NOT EXISTS usuarios")
        print("Base de datos creada exitosamente o ya existia.")
        
        cursor.execute("USE usuarios")
    
        create_table_users = """
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) NOT NULL UNIQUE
        )
        """

        create_table_generos = """
        CREATE TABLE IF NOT EXISTS generos(
            i_id_genero VARCHAR(50) PRIMARY KEY,
            v_descripcion VARCHAR(100) NOT NULL
        )
        """
        
        create_table_tiposid = """
        CREATE TABLE IF NOT EXISTS tiposid(
            i_id_tipoid VARCHAR(50) PRIMARY KEY,
            v_descripcion VARCHAR(100) NOT NULL
        )
        """

        create_table_personas = """
        CREATE TABLE IF NOT EXISTS personas(
            v_id_docente VARCHAR(50) PRIMARY KEY,
            v_nombre VARCHAR(50) NOT NULL,
            v_apellido VARCHAR(50) NOT NULL,
            i_id_genero VARCHAR(50),
            i_id_tipoid VARCHAR(50),
            FOREIGN KEY (i_id_tipoid) REFERENCES tiposid(i_id_tipoid),
            FOREIGN KEY (i_id_genero) REFERENCES generos(i_id_genero)
        )
        """

        cursor.execute(create_table_users)
        print("SE HA CREADO O YA EXISTIA LA TABLA DE USUARIOS")

        cursor.execute(create_table_generos)
        print("SE HA CREADO O YA EXISTIA LA TABLA DE GENEROS")
        
        cursor.execute(create_table_tiposid)
        print("SE HA CREADO O YA EXISTIA LA TABLA DE TIPOSID")

        cursor.execute(create_table_personas)
        print("SE HA CREADO O YA EXISTIA LA TABLA DE PERSONAS")
        
        # Confirmar los cambios
        connection.commit()
except Error as e:
    print("Error al conectarse a MySQL:", e)
    
# Cerrar la conexión
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada con la base de datos.")