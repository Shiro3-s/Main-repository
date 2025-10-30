from typing import Optional

class FinanciacionDatabaseCreator:
    """
    Generador de base de datos para el microservicio ms-financiacion
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
            CREATE TABLE IF NOT EXISTS Fuente_Financiacion (
                id_fuente {types['INT']} PRIMARY KEY,
                codigo_fuente {types['VARCHAR']}(50) UNIQUE NOT NULL,
                nombre_fuente {types['VARCHAR']}(200) NOT NULL,
                desc_fuente {types['VARCHAR']}(500),
                entidad_financiadora {types['VARCHAR']}(300)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Financiacion_Proyecto (
                id_financiacion {types['INT']} PRIMARY KEY,
                valor_asignado {types['DOUBLE']},
                porcentaje_participacion {types['DOUBLE']},
                vigencia_presupuestal {types['VARCHAR']}(20),
                id_fuente_financiacion {types['INT']},
                codigo_bpin {types['VARCHAR']}(50)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Avance_Financiero (
                id_avance_financiero {types['INT']} PRIMARY KEY,
                fecha_reporte {types['VARCHAR']}(20),
                periodo_reporte {types['VARCHAR']}(20),
                valor_comprometido {types['DOUBLE']},
                valor_obligado {types['DOUBLE']},
                valor_pagado {types['DOUBLE']},
                porcentaje_ejecucion {types['DOUBLE']},
                saldo_disponible {types['DOUBLE']},
                modificaciones_presupuestales {types['DOUBLE']},
                id_fuente {types['INT']},
                codigo_bpin {types['VARCHAR']}(50)
            );
            """
        ]
        for i, table_sql in enumerate(tables, 1):
            self.cursor.execute(table_sql)
        self.conn.commit()
        print("🎉 ¡Base de datos de financiación creada exitosamente!")

    def insert_sample_data(self):
        self.cursor.execute("INSERT OR IGNORE INTO Fuente_Financiacion VALUES (1, 'F001', 'Presupuesto Nacional', 'Recursos del estado', 'Ministerio de Hacienda')")
        self.cursor.execute("INSERT OR IGNORE INTO Financiacion_Proyecto VALUES (1, 50000000, 100, '2025', 1, 'BPIN001')")
        self.cursor.execute("INSERT OR IGNORE INTO Avance_Financiero VALUES (1, '2025-03-01', '2025Q1', 10000000, 8000000, 5000000, 20, 40000000, 0, 1, 'BPIN001')")
        self.conn.commit()
        print("✅ Datos de muestra insertados exitosamente")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✅ Conexión cerrada exitosamente")

def main():
    print("🏗️  GENERADOR DE BASE DE DATOS MS-FINANCIACION")
    db_creator = FinanciacionDatabaseCreator(
        db_type="sqlite",
        connection_params={'database': 'dnp_financiacion.db'}
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