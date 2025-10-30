from typing import Optional

class EntidadesDatabaseCreator:
    """
    Generador de base de datos para el microservicio ms-entidades
    Soporta SQLite y PostgreSQL
    """

    def __init__(self, db_type: str = "sqlite", connection_params: Optional[dict] = None):
        self.db_type = db_type
        self.connection_params = connection_params or {}
        self.conn = None
        self.cursor = None

    def connect(self):
        if self.db_type == "sqlite":
            import sqlite3
            self.conn = sqlite3.connect(self.connection_params.get("database", ":memory:"))
            self.cursor = self.conn.cursor()
        elif self.db_type == "postgresql":
            import psycopg2
            self.conn = psycopg2.connect(**self.connection_params)
            self.cursor = self.conn.cursor()
        else:
            raise ValueError("Tipo de base de datos no soportado")

    def get_data_types(self):
        if self.db_type == "sqlite":
            return {
                "INT": "INTEGER",
                "VARCHAR": "TEXT"
            }
        elif self.db_type == "postgresql":
            return {
                "INT": "INTEGER",
                "VARCHAR": "VARCHAR"
            }

    def create_tables(self):
        types = self.get_data_types()
        tables = [
            f"""
            CREATE TABLE IF NOT EXISTS Region (
                id_region {types['INT']} PRIMARY KEY,
                nombre_region {types['VARCHAR']}(100) NOT NULL
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Departamento (
                id_departamento {types['INT']} PRIMARY KEY,
                cod_dane_departamento {types['VARCHAR']}(10) UNIQUE NOT NULL,
                nombre_departamento {types['VARCHAR']}(100) NOT NULL,
                id_region {types['INT']}
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Municipio (
                id_municipio {types['INT']} PRIMARY KEY,
                cod_dane_municipio {types['VARCHAR']}(10) UNIQUE NOT NULL,
                nombre_municipio {types['VARCHAR']}(100) NOT NULL,
                coordenadas_lat {types['VARCHAR']}(50),
                coordenadas_long {types['VARCHAR']}(50),
                id_departamento {types['INT']}
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Nivel_Gobierno (
                id_nivel_gob {types['INT']} PRIMARY KEY,
                nombre_nivel_gob {types['VARCHAR']}(100) NOT NULL,
                desc_nivel_gob {types['VARCHAR']}(300)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Entidad_Ejecutora (
                id_entidad_ejecutora {types['INT']} PRIMARY KEY,
                nombre_entidad {types['VARCHAR']}(300) NOT NULL,
                nit_entidad {types['VARCHAR']}(50),
                email_contacto {types['VARCHAR']}(200),
                telefono_contacto {types['VARCHAR']}(50),
                representante_legal {types['VARCHAR']}(200),
                estado_entidad {types['INT']},
                id_tipo_entidad {types['INT']},
                id_nivel_gob {types['INT']}
            );
            """
        ]
        for i, table_sql in enumerate(tables, 1):
            self.cursor.execute(table_sql)
        self.conn.commit()
        print("🎉 ¡Base de datos de entidades creada exitosamente!")

    def insert_sample_data(self):
        self.cursor.execute("INSERT OR IGNORE INTO Region VALUES (1, 'Caribe')")
        self.cursor.execute("INSERT OR IGNORE INTO Departamento VALUES (1, '08', 'Atlántico', 1)")
        self.cursor.execute("INSERT OR IGNORE INTO Municipio VALUES (1, '08001', 'Barranquilla', '10.9639', '-74.7964', 1)")
        self.cursor.execute("INSERT OR IGNORE INTO Nivel_Gobierno VALUES (1, 'Nacional', 'Gobierno central')")
        self.cursor.execute("INSERT OR IGNORE INTO Entidad_Ejecutora VALUES (1, 'Ministerio de Educación', '800123456', 'contacto@minedu.gov.co', '1234567', 'Juan Pérez', 1, 1, 1)")
        self.conn.commit()
        print("✅ Datos de muestra insertados exitosamente")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✅ Conexión cerrada exitosamente")

def main():
    print("🏗️  GENERADOR DE BASE DE DATOS MS-ENTIDADES")
    db_creator = EntidadesDatabaseCreator(
        db_type="sqlite",
        connection_params={'database': 'dnp_entidades.db'}
    )
    try:
        db_creator.connect()
        db_creator.create_tables()
        db_creator.insert_sample_data()
        print("\n🎯 PROCESO COMPLETADO EXITOSAMENTE")
    except Exception as e:
        print(f"💥 Error durante la ejecución: {e}")
    finally:
        db_creator.close()

if __name__ == "__main__":
    main()