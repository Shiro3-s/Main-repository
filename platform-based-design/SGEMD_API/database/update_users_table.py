import mysql.connector as msql
from mysql.connector import Error 

try:
    connection = msql.connect(
        host="localhost",
        port="3306",
        user="root",
        password=""
    )

    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS DB_SEGMED")
        print("Base de datos creada exitosamente o ya existía.")

        cursor.execute("USE DB_SEGMED")

        # Tabla Usuarios con relaciones y campo Password
        create_Usuarios = """
        CREATE TABLE IF NOT EXISTS Usuarios (
            idUsuarios INT NOT NULL AUTO_INCREMENT,
            Nombre VARCHAR(45) NOT NULL,
            CorreoInstitucional VARCHAR(45) NOT NULL,
            CorreoPersonal VARCHAR(45) NOT NULL,
            Password VARCHAR(255) NOT NULL,  -- Nuevo campo para la contraseña
            Celular VARCHAR(45) NOT NULL,
            Telefono VARCHAR(45) NOT NULL,
            Direccion VARCHAR(45) NOT NULL,  -- Corregido de Direcccion
            Genero VARCHAR(45) NOT NULL,
            EstadoCivil VARCHAR(45) NOT NULL,
            FechaNacimiento DATE NOT NULL,
            Modulos_idModulos INT,
            Municipios_idMunicipio INT,
            ProgramaAcademico_idProgramaAcademico INT,
            Roles_idRoles1 INT,
            TipoDocumentos_idTipoDocumento INT,
            TipoUsuarios_idTipoUsuarios INT,
            ProgramaAcademico_idProgramaAcademico1 INT NOT NULL,
            CentroUniversitarios_idCentroUniversitarios INT NOT NULL,
            Estado TINYINT NOT NULL,
            Semestre VARCHAR(45) NOT NULL,
            Modalidad VARCHAR(45) NOT NULL,
            TipoPoblacion_idTipoPoblacion INT,
            FechaCreacion DATE,
            FechaActualizacion DATE,
            PRIMARY KEY (idUsuarios),
            INDEX fk_Usuarios_Modulos_idx (Modulos_idModulos),
            INDEX fk_Usuarios_Municipios1_idx (Municipios_idMunicipio),
            INDEX fk_Usuarios_ProgramaAcademico1_idx (ProgramaAcademico_idProgramaAcademico),
            INDEX fk_Usuarios_Roles2_idx (Roles_idRoles1),
            INDEX fk_Usuarios_TipoDocumentos1_idx (TipoDocumentos_idTipoDocumento),
            INDEX fk_Usuarios_TipoUsuarios1_idx (TipoUsuarios_idTipoUsuarios),
            INDEX fk_Usuarios_ProgramaAcademico2_idx (ProgramaAcademico_idProgramaAcademico1),
            INDEX fk_Usuarios_CentroUniversitarios1_idx (CentroUniversitarios_idCentroUniversitarios),
            INDEX fk_Usuarios_TipoPoblacion1_idx (TipoPoblacion_idTipoPoblacion),
            CONSTRAINT fk_Usuarios_Modulos
                FOREIGN KEY (Modulos_idModulos)
                REFERENCES Modulos (idModulos),
            CONSTRAINT fk_Usuarios_Municipios1
                FOREIGN KEY (Municipios_idMunicipio)
                REFERENCES Municipios (idMunicipio),
            CONSTRAINT fk_Usuarios_ProgramaAcademico1
                FOREIGN KEY (ProgramaAcademico_idProgramaAcademico)
                REFERENCES ProgramaAcademico (idProgramaAcademico),
            CONSTRAINT fk_Usuarios_Roles2
                FOREIGN KEY (Roles_idRoles1)
                REFERENCES Roles (idRoles),
            CONSTRAINT fk_Usuarios_TipoDocumentos1
                FOREIGN KEY (TipoDocumentos_idTipoDocumento)
                REFERENCES TipoDocumentos (idTipoDocumento),
            CONSTRAINT fk_Usuarios_TipoUsuarios1
                FOREIGN KEY (TipoUsuarios_idTipoUsuarios)
                REFERENCES TipoUsuarios (idTipoUsuarios),
            CONSTRAINT fk_Usuarios_ProgramaAcademico2
                FOREIGN KEY (ProgramaAcademico_idProgramaAcademico1)
                REFERENCES ProgramaAcademico (idProgramaAcademico),
            CONSTRAINT fk_Usuarios_CentroUniversitarios1
                FOREIGN KEY (CentroUniversitarios_idCentroUniversitarios)
                REFERENCES CentroUniversitarios (idCentroUniversitarios),
            CONSTRAINT fk_Usuarios_TipoPoblacion1
                FOREIGN KEY (TipoPoblacion_idTipoPoblacion)
                REFERENCES TipoPoblacion (idTipoPoblacion)
        ) 
        """
        cursor.execute(create_Usuarios)

        # Si existe la tabla, agregar el campo Password
        alter_usuarios = """
        ALTER TABLE Usuarios
        ADD COLUMN IF NOT EXISTS Password VARCHAR(255) NOT NULL DEFAULT '';
        """
        cursor.execute(alter_usuarios)

        print("Tabla Usuarios actualizada exitosamente.")

except Error as e:
    print("Error al conectarse a MySQL:", e)
    
finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada con la base de datos.")