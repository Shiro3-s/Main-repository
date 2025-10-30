from typing import Optional

class ProyectosDatabaseCreator:
    """
    Generador de base de datos para el microservicio ms-proyectos
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
            CREATE TABLE IF NOT EXISTS Proyecto (
                codigo_bpin {types['VARCHAR']}(50) PRIMARY KEY,
                nombre_proyecto {types['VARCHAR']}(500) NOT NULL,
                desc_proyecto {types['VARCHAR']}(2000),
                objetivo_general {types['VARCHAR']}(1000),
                objetivos_especificos {types['VARCHAR']}(2000),
                justificacion {types['VARCHAR']}(2000),
                fecha_inicio_proyecto {types['VARCHAR']}(20),
                fecha_fin_prevista {types['VARCHAR']}(20),
                fecha_fin_registrada {types['VARCHAR']}(20),
                id_estado_proyecto {types['INT']},
                id_fase_proyecto {types['INT']},
                poblacion_beneficiaria {types['INT']},
                id_tipo_poblacion {types['INT']},
                valor_total_proyecto {types['DOUBLE']},
                id_programa {types['INT']},
                id_sector {types['INT']},
                id_ods {types['INT']},
                id_region {types['INT']},
                id_entidad_ejecutora {types['INT']},
                id_tipo_entidad {types['INT']},
                id_nivel_gobierno {types['INT']},
                id_estado {types['INT']},
                id_tipo_estado {types['INT']}
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Hito (
                id_hito {types['INT']} PRIMARY KEY,
                nombre_hito {types['VARCHAR']}(200),
                desc_hito {types['VARCHAR']}(500),
                fecha_programada {types['VARCHAR']}(20),
                fecha_real {types['VARCHAR']}(20),
                porcentaje_completado {types['DOUBLE']},
                responsable_hito {types['VARCHAR']}(200),
                id_estado {types['INT']},
                id_tipo_estado {types['INT']},
                codigo_bpin {types['VARCHAR']}(50)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Contrato (
                id_contrato {types['INT']} PRIMARY KEY,
                numero_contrato {types['VARCHAR']}(50),
                objeto_contrato {types['VARCHAR']}(500),
                contratista {types['VARCHAR']}(200),
                valor_contrato {types['DOUBLE']},
                fecha_inicio_contrato {types['VARCHAR']}(20),
                fecha_fin_contrato {types['VARCHAR']}(20),
                id_estado {types['INT']},
                id_tipo_estado {types['INT']},
                id_tipo_contratacion {types['INT']},
                codigo_bpin {types['VARCHAR']}(50)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Riesgo (
                id_riesgo {types['INT']} PRIMARY KEY,
                codigo_bpin {types['VARCHAR']}(50),
                probabilidad {types['DOUBLE']},
                estrategia_mitigacion {types['VARCHAR']}(500),
                responsable_seguimiento {types['VARCHAR']}(200),
                fecha_identificacion {types['VARCHAR']}(20),
                id_impacto {types['INT']}
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Impacto (
                id_impacto {types['INT']} PRIMARY KEY,
                nombre_impacto {types['VARCHAR']}(100) NOT NULL,
                desc_impacto {types['VARCHAR']}(255)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Nivel_Riesgo (
                id_nivel_riesgo {types['INT']} PRIMARY KEY,
                nombre_nivel {types['VARCHAR']}(100) NOT NULL,
                desc_nivel {types['VARCHAR']}(255)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Avance_Fisico (
                id_avance_fisico {types['INT']} PRIMARY KEY,
                fecha_reporte {types['VARCHAR']}(20),
                periodo_reporte {types['VARCHAR']}(20),
                porcentaje_avance_acumulado {types['DOUBLE']},
                porcentaje_avance_periodo {types['DOUBLE']},
                desc_actividades {types['VARCHAR']}(2000),
                productos_entregados {types['VARCHAR']}(1000),
                metas_cumplidas {types['INT']},
                dificultades_presentadas {types['VARCHAR']}(1000),
                acciones_correctivas {types['VARCHAR']}(1000),
                responsable_reporte {types['VARCHAR']}(200),
                codigo_bpin {types['VARCHAR']}(50)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Fase_Proyecto (
                id_fase_proyecto {types['INT']} PRIMARY KEY,
                nombre_fase_proyecto {types['VARCHAR']}(100) NOT NULL,
                desc_fase_proyecto {types['VARCHAR']}(255)
            );
            """
        ]
        for i, table_sql in enumerate(tables, 1):
            self.cursor.execute(table_sql)
        self.conn.commit()
        print("🎉 ¡Base de datos de proyectos creada exitosamente!")

    def insert_sample_data(self):
        self.cursor.execute("INSERT OR IGNORE INTO Proyecto VALUES ('BPIN001', 'Escuela Rural', 'Construcción de escuela', 'Mejorar educación', 'Aumentar cobertura', 'Falta de infraestructura', '2025-01-01', '2025-12-31', NULL, 1, 1, 100, 1, 50000000, 1, 1, 1, 1, 1, 1, 1, 1, 1)")
        self.cursor.execute("INSERT OR IGNORE INTO Hito VALUES (1, 'Inicio obra', 'Primer ladrillo', '2025-02-01', NULL, 0, 'Ingeniero', 1, 1, 'BPIN001')")
        self.cursor.execute("INSERT OR IGNORE INTO Contrato VALUES (1, 'C-001', 'Construcción', 'Constructora XYZ', 40000000, '2025-01-15', '2025-12-15', 1, 1, 1, 'BPIN001')")
        self.cursor.execute("INSERT OR IGNORE INTO Impacto VALUES (1, 'Educativo', 'Mejora en educación')")
        self.cursor.execute("INSERT OR IGNORE INTO Nivel_Riesgo VALUES (1, 'Alto', 'Riesgo alto')")
        self.cursor.execute("INSERT OR IGNORE INTO Avance_Fisico VALUES (1, '2025-03-01', '2025Q1', 10, 10, 'Excavación', 'Terreno listo', 1, 'Lluvias', 'Reprogramar', 'Supervisor', 'BPIN001')")
        self.cursor.execute("INSERT OR IGNORE INTO Fase_Proyecto VALUES (1, 'Planeación', 'Fase inicial')")
        self.conn.commit()
        print("✅ Datos de muestra insertados exitosamente")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✅ Conexión cerrada exitosamente")

def main():
    print("🏗️  GENERADOR DE BASE DE DATOS MS-PROYECTOS")
    db_creator = ProyectosDatabaseCreator(
        db_type="sqlite",
        connection_params={'database': 'dnp_proyectos.db'}
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