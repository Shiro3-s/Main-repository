from typing import Optional

class IndicadoresDatabaseCreator:
    """
    Generador de base de datos para el microservicio ms-indicadores
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
                "VARCHAR": "TEXT",
                "DOUBLE": "REAL"
            }
        elif self.db_type == "postgresql":
            return {
                "INT": "INTEGER",
                "VARCHAR": "VARCHAR",
                "DOUBLE": "DOUBLE PRECISION"
            }

    def create_tables(self):
        types = self.get_data_types()
        tables = [
            f"""
            CREATE TABLE IF NOT EXISTS Indicador (
                id_indicador {types['INT']} PRIMARY KEY,
                nombre_indicador {types['VARCHAR']}(300) NOT NULL,
                desc_indicador {types['VARCHAR']}(1000),
                id_tipo_indicador {types['INT']}
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Seguimiento_Indicador (
                id_seguimiento {types['INT']} PRIMARY KEY,
                id_indicador {types['INT']},
                fecha_medicion {types['VARCHAR']}(20),
                valor_programado {types['DOUBLE']},
                valor_ejecutado {types['DOUBLE']},
                valor_acumulado {types['DOUBLE']},
                observaciones {types['VARCHAR']}(500),
                codigo_bpin {types['VARCHAR']}(50)
            );
            """
        ]
        for i, table_sql in enumerate(tables, 1):
            self.cursor.execute(table_sql)
        self.conn.commit()
        print("🎉 ¡Base de datos de indicadores creada exitosamente!")

    def insert_sample_data(self):
        self.cursor.execute("INSERT OR IGNORE INTO Indicador VALUES (1, 'Cobertura', 'Porcentaje de niños beneficiados', 1)")
        self.cursor.execute("INSERT OR IGNORE INTO Seguimiento_Indicador VALUES (1, 1, '2025-03-01', 100, 80, 80, 'Avance inicial', 'BPIN001')")
        self.conn.commit()
        print("✅ Datos de muestra insertados exitosamente")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✅ Conexión cerrada exitosamente")

def main():
    print("🏗️  GENERADOR DE BASE DE DATOS MS-INDICADORES")
    db_creator = IndicadoresDatabaseCreator(
        db_type="sqlite",
        connection_params={'database': 'dnp_indicadores.db'}
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