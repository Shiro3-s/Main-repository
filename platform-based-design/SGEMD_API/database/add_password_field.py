import mysql.connector as msql
from mysql.connector import Error 

connection = None
cursor = None

try:
    # Establecer conexión con MySQL
    connection = msql.connect(
        host="localhost",
        port="3306",
        user="root",
        password=""
    )

    if connection.is_connected():
        cursor = connection.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS DB_SEGMED")
        cursor.execute("USE DB_SEGMED")
        print("Base de datos seleccionada exitosamente.")
        
        # Verificar si la tabla Usuarios existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'DB_SEGMED' 
            AND table_name = 'Usuarios'
        """)
        table_exists = cursor.fetchone()[0] > 0

        if table_exists:
            # Verificar si la columna Password existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_schema = 'DB_SEGMED'
                AND table_name = 'Usuarios'
                AND column_name = 'Password'
            """)
            password_exists = cursor.fetchone()[0] > 0

            if not password_exists:
                # Agregar la columna Password
                cursor.execute("""
                    ALTER TABLE Usuarios
                    ADD COLUMN Password VARCHAR(255) NOT NULL DEFAULT ''
                """)
                print("Columna Password agregada exitosamente a la tabla Usuarios.")
            else:
                print("La columna Password ya existe en la tabla Usuarios.")
        else:
            print("La tabla Usuarios no existe. Por favor, ejecute primero init_db.py")

except Error as e:
    print("Error al conectarse a MySQL:", e)
    
finally:
    if connection and connection.is_connected():
        if cursor:
            cursor.close()
        connection.close()
        print("Conexión cerrada con la base de datos.")