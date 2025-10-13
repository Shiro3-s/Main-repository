from datetime import datetime
from typing import Optional

class CatalogosDatabaseCreator:
    """
    Generador de base de datos para el microservicio ms-catalogos
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
                "DOUBLE": "REAL",
                "DECIMAL": "REAL",
                "NUMERIC": "REAL",
                "DATE": "TEXT",
                "DATETIME": "TEXT",
                "BOOLEAN": "INTEGER"
            }
        elif self.db_type == "postgresql":
            return {
                "INT": "INTEGER",
                "VARCHAR": "VARCHAR",
                "DOUBLE": "DOUBLE PRECISION",
                "DECIMAL": "DECIMAL",
                "NUMERIC": "NUMERIC",
                "DATE": "DATE",
                "DATETIME": "TIMESTAMP",
                "BOOLEAN": "BOOLEAN"
            }

    def create_tables(self):
        types = self.get_data_types()
        tables = []

        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Ods (
                id_ods {types['INT']} PRIMARY KEY,
                nombre_ods {types['VARCHAR']}(200) NOT NULL,
                desc_ods {types['VARCHAR']}(500)
            );
        """)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Sector (
                id_sector {types['INT']} PRIMARY KEY,
                codigo_sector {types['VARCHAR']}(20) UNIQUE NOT NULL,
                nombre_sector {types['VARCHAR']}(200) NOT NULL,
                descripcion_sector {types['VARCHAR']}(500),
                id_ods {types['INT']}
            );
        """)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Tipo_Estado (
                id_tipo_estado {types['INT']} PRIMARY KEY,
                nombre_estado {types['VARCHAR']}(100) NOT NULL,
                desc_estado {types['VARCHAR']}(300)
            );
        """)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Estado (
                id_estado {types['INT']} PRIMARY KEY,
                nombre_estado {types['VARCHAR']}(100) NOT NULL,
                desc_estado {types['VARCHAR']}(300),
                id_tipo_estado {types['INT']}
            );
        """)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Tipo_Indicador (
                id_tipo_indicador {types['INT']} PRIMARY KEY,
                nombre_tipo_indicador {types['VARCHAR']}(100) NOT NULL,
                desc_tipo_indicador {types['VARCHAR']}(255),
                unidad_medida {types['VARCHAR']}(100),
                formula_calculo {types['VARCHAR']}(200),
                frecuencia_medicion {types['VARCHAR']}(45),
                responsable_medicion {types['VARCHAR']}(45)
            );
        """)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Tipo_Beneficiario (
                id_tipo_beneficiario {types['INT']} PRIMARY KEY,
                nombre_tipo_beneficiario {types['VARCHAR']}(100) NOT NULL,
                desc_tipo_beneficiario {types['VARCHAR']}(255)
            );
        """)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Tipo_Contratacion (
                id_tipo_contratacion {types['INT']} PRIMARY KEY,
                nombre_tipo_contratacion {types['VARCHAR']}(100) NOT NULL,
                desc_tipo_contratacion {types['VARCHAR']}(255)
            );
        """)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Tipo_Poblacion (
                id_tipo_poblacion {types['INT']} PRIMARY KEY,
                nombre_tipo_poblacion {types['VARCHAR']}(100) NOT NULL,
                desc_tipo_poblacion {types['VARCHAR']}(255)
            );
        """)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Tipo_Riesgo (
                id_tipo_riesgo {types['INT']} PRIMARY KEY,
                nombre_tipo_riesgo {types['VARCHAR']}(100) NOT NULL,
                desc_tipo_riesgo {types['VARCHAR']}(255)
            );
        """)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Programa (
                id_programa {types['INT']} PRIMARY KEY,
                codigo_programa {types['VARCHAR']}(50) UNIQUE NOT NULL,
                nombre_programa {types['VARCHAR']}(300) NOT NULL,
                desc_programa {types['VARCHAR']}(1000),
                objetivo_general {types['VARCHAR']}(1000),
                fecha_inicio_programa {types['DATE']},
                fecha_fin_programa {types['DATE']},
                responsable_programa {types['VARCHAR']}(200)
            );
        """)

        for i, table_sql in enumerate(tables, 1):
            try:
                self.cursor.execute(table_sql)
                print(f"✅ Tabla {i} creada exitosamente")
            except Exception as e:
                print(f"❌ Error creando tabla {i}: {e}")

        self.conn.commit()
        print("🎉 ¡Base de datos de catálogos creada exitosamente!")

    def insert_sample_data(self):
        """Inserta datos de muestra en las tablas de catálogos"""
        try:
            # ODS
            self.cursor.execute("INSERT OR IGNORE INTO Ods VALUES (1, 'Educación de calidad', 'Garantizar educación inclusiva')")
            self.cursor.execute("INSERT OR IGNORE INTO Ods VALUES (2, 'Salud y bienestar', 'Garantizar vidas saludables')")
            # Sector
            self.cursor.execute("INSERT OR IGNORE INTO Sector VALUES (1, 'EDU', 'Educación', 'Proyectos educativos', 1)")
            self.cursor.execute("INSERT OR IGNORE INTO Sector VALUES (2, 'SAL', 'Salud', 'Proyectos de salud pública', 2)")
            # Tipo_Estado
            self.cursor.execute("INSERT OR IGNORE INTO Tipo_Estado VALUES (1, 'En ejecución', 'Proyecto activo')")
            # Estado
            self.cursor.execute("INSERT OR IGNORE INTO Estado VALUES (1, 'Activo', 'Proyecto en curso', 1)")
            # Tipo_Indicador
            self.cursor.execute("INSERT OR IGNORE INTO Tipo_Indicador VALUES (1, 'Cobertura', 'Porcentaje de cobertura', 'Porcentaje', 'Beneficiarios/Meta', 'Mensual', 'DNP')")
            # Tipo_Beneficiario
            self.cursor.execute("INSERT OR IGNORE INTO Tipo_Beneficiario VALUES (1, 'Niños', 'Menores de edad')")
            # Tipo_Contratacion
            self.cursor.execute("INSERT OR IGNORE INTO Tipo_Contratacion VALUES (1, 'Obra', 'Contratación de obra')")
            # Tipo_Poblacion
            self.cursor.execute("INSERT OR IGNORE INTO Tipo_Poblacion VALUES (1, 'Infantil', 'Menores de edad')")
            # Tipo_Riesgo
            self.cursor.execute("INSERT OR IGNORE INTO Tipo_Riesgo VALUES (1, 'Climático', 'Riesgo por clima')")
            # Programa
            self.cursor.execute("INSERT OR IGNORE INTO Programa VALUES (1, 'PRG001', 'Educación Rural', 'Programa de escuelas rurales', 'Mejorar acceso', '2025-01-01', '2025-12-31', 'Ministerio')")

            self.conn.commit()
            print("✅ Datos de muestra insertados exitosamente")

        except Exception as e:
            print(f"❌ Error insertando datos de muestra: {e}")

    def create_indexes(self):
        """Crea índices para optimizar consultas"""
        try:
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_sector_ods ON Sector(id_ods);",
                "CREATE INDEX IF NOT EXISTS idx_estado_tipo ON Estado(id_tipo_estado);",
                "CREATE INDEX IF NOT EXISTS idx_programa_codigo ON Programa(codigo_programa);"
            ]
            for index_sql in indexes:
                self.cursor.execute(index_sql)
            self.conn.commit()
            print("✅ Índices creados exitosamente")
        except Exception as e:
            print(f"❌ Error creando índices: {e}")

    def close(self):
        """Cierra la conexión a la base de datos"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("✅ Conexión cerrada exitosamente")
        except Exception as e:
            print(f"❌ Error cerrando conexión: {e}")

def main():
    """Función principal para ejecutar el creador de base de datos de catálogos"""
    print("🏗️  GENERADOR DE BASE DE DATOS MS-CATALOGOS")
    print("=" * 50)

    db_creator = CatalogosDatabaseCreator(
        db_type="sqlite",
        connection_params={'database': 'dnp_catalogos.db'}
    )
    try:
        db_creator.connect()
        db_creator.create_tables()
        db_creator.insert_sample_data()
        db_creator.create_indexes()

        print("\n🎯 PROCESO COMPLETADO EXITOSAMENTE")
        print("📁 Base de datos creada: dnp_catalogos.db")
        print("📊 Tablas creadas: Ods, Sector, Tipo_Estado, Estado, Tipo_Indicador, Tipo_Beneficiario, Tipo_Contratacion, Tipo_Poblacion, Tipo_Riesgo, Programa")
        print("🔍 Índices optimizados creados")
        print("📋 Datos de muestra insertados")

    except Exception as e:
        print(f"💥 Error durante la ejecución: {e}")
    finally:
        db_creator.close()

if __name__ == "__main__":
    main()