from datetime import datetime
from typing import Optional

class DNPDatabaseCreator:
    """
    Generador de base de datos para el sistema DNP de seguimiento de proyectos
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
        
        # Tabla Tipo_Beneficiario (debe crearse primero por la relación FK)
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Tipo_Beneficiario (
                id_tipo_beneficiario {types['INT']} PRIMARY KEY,
                nombre_tipo {types['VARCHAR']}(50) NOT NULL,
                descripcion {types['VARCHAR']}(255)
            );
        """)
        
        # Tabla Beneficiario
        tables.append(f"""
            CREATE TABLE IF NOT EXISTS Beneficiario (
                id_beneficiario {types['INT']} PRIMARY KEY,
                nombre_beneficiario {types['VARCHAR']}(100) NOT NULL,
                desc_beneficiario {types['VARCHAR']}(255),
                Tipo_Beneficiario_id_tipo_beneficiario {types['INT']},
                FOREIGN KEY (Tipo_Beneficiario_id_tipo_beneficiario) REFERENCES Tipo_Beneficiario(id_tipo_beneficiario)
            );
        """)
        
        for i, table_sql in enumerate(tables, 1):
            try:
                self.cursor.execute(table_sql)
                print(f"✅ Tabla {i} creada exitosamente")
            except Exception as e:
                print(f"❌ Error creando tabla {i}: {e}")
        
        self.conn.commit()
        print("🎉 ¡Base de datos creada exitosamente!")

    def insert_sample_data(self):
        """Inserta datos de muestra en las tablas"""
        try:
            # Insertar tipos de beneficiario
            sample_types = [
                (1, 'Persona Natural', 'Beneficiario individual'),
                (2, 'Empresa', 'Empresa privada beneficiaria'),
                (3, 'ONG', 'Organización no gubernamental'),
                (4, 'Institución Pública', 'Entidad del sector público')
            ]
            
            for tipo in sample_types:
                if self.db_type == "sqlite":
                    self.cursor.execute(
                        "INSERT OR IGNORE INTO Tipo_Beneficiario (id_tipo_beneficiario, nombre_tipo, descripcion) VALUES (?, ?, ?)",
                        tipo
                    )
                elif self.db_type == "postgresql":
                    self.cursor.execute(
                        "INSERT INTO Tipo_Beneficiario (id_tipo_beneficiario, nombre_tipo, descripcion) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                        tipo
                    )
            
            # Insertar beneficiarios de muestra
            sample_beneficiarios = [
                (1, 'Juan Pérez', 'Beneficiario individual del programa social', 1),
                (2, 'María González', 'Emprendedora local', 1),
                (3, 'TechCorp S.A.S', 'Empresa de tecnología', 2),
                (4, 'Fundación Esperanza', 'ONG de ayuda social', 3),
                (5, 'Hospital San José', 'Institución de salud pública', 4)
            ]
            
            for beneficiario in sample_beneficiarios:
                if self.db_type == "sqlite":
                    self.cursor.execute(
                        "INSERT OR IGNORE INTO Beneficiario (id_beneficiario, nombre_beneficiario, desc_beneficiario, Tipo_Beneficiario_id_tipo_beneficiario) VALUES (?, ?, ?, ?)",
                        beneficiario
                    )
                elif self.db_type == "postgresql":
                    self.cursor.execute(
                        "INSERT INTO Beneficiario (id_beneficiario, nombre_beneficiario, desc_beneficiario, Tipo_Beneficiario_id_tipo_beneficiario) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                        beneficiario
                    )
            
            self.conn.commit()
            print("✅ Datos de muestra insertados exitosamente")
            
        except Exception as e:
            print(f"❌ Error insertando datos de muestra: {e}")

    def create_indexes(self):
        """Crea índices para optimizar consultas"""
        try:
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_beneficiario_tipo ON Beneficiario(Tipo_Beneficiario_id_tipo_beneficiario);",
                "CREATE INDEX IF NOT EXISTS idx_beneficiario_nombre ON Beneficiario(nombre_beneficiario);",
                "CREATE INDEX IF NOT EXISTS idx_tipo_beneficiario_nombre ON Tipo_Beneficiario(nombre_tipo);"
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
    """Función principal para ejecutar el creador de base de datos"""
    print("🏗️  GENERADOR DE BASE DE DATOS DNP")
    print("=" * 50)
    
    # Configuración para SQLite (por defecto)
    db_creator = DNPDatabaseCreator(
        db_type="sqlite",
        connection_params={'database': 'dnp_beneficiarios.db'}
    )
    try:
        # Ejecutar proceso completo
        db_creator.connect()
        db_creator.create_tables()
        db_creator.insert_sample_data()
        db_creator.create_indexes()
        
        print("\n🎯 PROCESO COMPLETADO EXITOSAMENTE")
        print("📁 Base de datos creada: dnp_beneficiarios.db")
        print("📊 Tablas creadas: Beneficiario y Tipo_Beneficiario")
        print("🔍 Índices optimizados creados")
        print("📋 Datos de muestra insertados")
        
    except Exception as e:
        print(f"💥 Error durante la ejecución: {e}")
    finally:
        db_creator.close()

if __name__ == "__main__":
    main()