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

        # Tabla Modulos
        create_Modulos = """
        CREATE TABLE IF NOT EXISTS Modulos (
            idModulos INT NOT NULL AUTO_INCREMENT,
            Asistencia VARCHAR(45) NOT NULL,
            Practicas VARCHAR(45) NOT NULL,
            OpcionGrado VARCHAR(45) NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            PRIMARY KEY (idModulos)
        ) 
        """
        cursor.execute(create_Modulos)

        # Tabla Municipios
        create_Municipios = """
        CREATE TABLE IF NOT EXISTS Municipios (
            idMunicipio INT NOT NULL,
            Nombre VARCHAR(45) NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            PRIMARY KEY (idMunicipio)
        ) 
        """
        cursor.execute(create_Municipios)

        # Tabla ProgramaAcademico
        create_ProgramaAcademico = """
        CREATE TABLE IF NOT EXISTS ProgramaAcademico (
            idProgramaAcademico INT NOT NULL AUTO_INCREMENT,
            Nombre VARCHAR(45) NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            PRIMARY KEY (idProgramaAcademico)
        ) 
        """
        cursor.execute(create_ProgramaAcademico)

        # Tabla Roles
        create_Roles = """
        CREATE TABLE IF NOT EXISTS Roles (
            idRoles INT NOT NULL AUTO_INCREMENT,
            Nombre VARCHAR(45) NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            PRIMARY KEY (idRoles)
        ) 
        """
        cursor.execute(create_Roles)

        # Tabla TipoDocumentos
        create_TipoDocumentos = """
        CREATE TABLE IF NOT EXISTS TipoDocumentos (
            idTipoDocumento INT NOT NULL AUTO_INCREMENT,
            TipoDocumento VARCHAR(45) NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            PRIMARY KEY (idTipoDocumento)
        ) 
        """
        cursor.execute(create_TipoDocumentos)

        # Tabla TipoUsuarios
        create_TipoUsuarios = """
        CREATE TABLE IF NOT EXISTS TipoUsuarios (
            idTipoUsuarios INT NOT NULL AUTO_INCREMENT,
            TipodeUsuario VARCHAR(45) NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            PRIMARY KEY (idTipoUsuarios)
        ) 
        """
        cursor.execute(create_TipoUsuarios)

        # Tabla CentroUniversitarios
        create_CentroUniversitarios = """
        CREATE TABLE IF NOT EXISTS CentroUniversitarios (
            idCentroUniversitarios INT NOT NULL AUTO_INCREMENT,
            Nombre VARCHAR(45) NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            PRIMARY KEY (idCentroUniversitarios)
        ) 
        """
        cursor.execute(create_CentroUniversitarios)

        # Tabla TipoPoblacion
        create_TipoPoblacion = """
        CREATE TABLE IF NOT EXISTS TipoPoblacion (
            idTipoPoblacion INT NOT NULL AUTO_INCREMENT,
            Nombre VARCHAR(45) NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            PRIMARY KEY (idTipoPoblacion)
        ) 
        """
        cursor.execute(create_TipoPoblacion)

        # Tabla Usuarios con relaciones
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

        # Tabla EtapadeEmpedimiento
        create_EtapadeEmpedimiento = """
        CREATE TABLE IF NOT EXISTS EtapadeEmpedimiento (
            idEtapadeEmpedimiento INT NOT NULL AUTO_INCREMENT,
            Estado TINYINT NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            TipoEtapa VARCHAR(45) NOT NULL,
            PRIMARY KEY (idEtapadeEmpedimiento)
        ) 
        """
        cursor.execute(create_EtapadeEmpedimiento)

        # Tabla Emprendimiento
        create_Emprendimiento = """
        CREATE TABLE IF NOT EXISTS Emprendimiento (
            idEmprendimiento INT NOT NULL AUTO_INCREMENT,
            Nombre VARCHAR(45) NOT NULL,
            Descripcion VARCHAR(45) NOT NULL,
            TipoEmprendimiento VARCHAR(45) NOT NULL,  -- Corregido de TipoEmpreedimiento
            SectorProductivo VARCHAR(45) NOT NULL,    -- Corregido de SectorPruductivo
            RedesSociales TINYINT NOT NULL,
            Acompanamiento TINYINT NOT NULL,          -- Corregido de Acompañamiento (evita la ñ)
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            ActaCompromiso TEXT(150) NOT NULL,
            EtapadeEmpedimiento_idEtapadeEmpedimiento INT NOT NULL,
            PRIMARY KEY (idEmprendimiento),
            INDEX fk_Emprendimiento_EtapadeEmpedimiento1_idx (EtapadeEmpedimiento_idEtapadeEmpedimiento),
            CONSTRAINT fk_Emprendimiento_EtapadeEmpedimiento1
                FOREIGN KEY (EtapadeEmpedimiento_idEtapadeEmpedimiento)
                REFERENCES EtapadeEmpedimiento (idEtapadeEmpedimiento)
        ) 
        """
        cursor.execute(create_Emprendimiento)

        # Tabla Seguimientos
        create_Seguimientos = """
        CREATE TABLE IF NOT EXISTS Seguimientos (
            idSeguimientos INT NOT NULL AUTO_INCREMENT,
            histproal VARCHAR(45) NOT NULL,
            TipoSeguimiento VARCHAR(45) NOT NULL,
            Descripcion VARCHAR(45) NOT NULL,
            Seguimientoscol VARCHAR(45) NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            PRIMARY KEY (idSeguimientos)
        ) 
        """
        cursor.execute(create_Seguimientos)

        # Tabla Asisitencia
        create_Asisitencia = """
        CREATE TABLE IF NOT EXISTS Asisitencia (
            idAsisitencia INT NOT NULL AUTO_INCREMENT,
            FeedBack VARCHAR(45) NOT NULL,
            Emprendimiento_idEmprendimiento INT NOT NULL,
            FechaCreacion DATE NOT NULL,
            FechaActualizacion DATE NOT NULL,
            Seguimientos_idSeguimientos INT NOT NULL,
            PRIMARY KEY (idAsisitencia),
            INDEX fk_Asisitencia_Emprendimiento1_idx (Emprendimiento_idEmprendimiento),
            INDEX fk_Asisitencia_Seguimientos1_idx (Seguimientos_idSeguimientos),
            CONSTRAINT fk_Asisitencia_Emprendimiento1
                FOREIGN KEY (Emprendimiento_idEmprendimiento)
                REFERENCES Emprendimiento (idEmprendimiento),
            CONSTRAINT fk_Asisitencia_Seguimientos1
                FOREIGN KEY (Seguimientos_idSeguimientos)
                REFERENCES Seguimientos (idSeguimientos)
        ) 
        """
        cursor.execute(create_Asisitencia)

        # Tabla SectoEconomico
        create_SectoEconomico = """
        CREATE TABLE IF NOT EXISTS SectoEconomico (
            idSectoEconomico INT NOT NULL AUTO_INCREMENT,
            Nombre VARCHAR(45) NOT NULL,
            PRIMARY KEY (idSectoEconomico)
        ) 
        """
        cursor.execute(create_SectoEconomico)

        # Tabla Diagnosticos
        create_Diagnosticos = """
        CREATE TABLE IF NOT EXISTS Diagnosticos (
            idDiagnosticos INT NOT NULL AUTO_INCREMENT,
            FechaEmprendimiento DATE NOT NULL,                -- Corregido de FechaEmpredimiento
            AreaEstrategia VARCHAR(45) NOT NULL,
            Diferencial TINYINT NOT NULL,
            Planeacion TINYINT NOT NULL,
            MercadoObjetivo VARCHAR(45) NOT NULL,             -- Corregido de Mercadoobjetivo
            Tendencias TINYINT NOT NULL,
            Canales TINYINT NOT NULL,
            DescripcionPromocion TEXT(150) NOT NULL,
            SectoEconomico_idSectoEconomico INT NOT NULL,
            Emprendimiento_idEmprendimiento INT NOT NULL,
            Presentacion TINYINT NOT NULL,
            PasosElaboracion TINYINT NOT NULL,
            SituacionFinanciera TINYINT NOT NULL,             -- Corregido de SituacionFinaciera
            FuenteFinanciero TEXT(150) NOT NULL,              -- Corregido de FuenteFinaciero
            EstructuraOrganica TINYINT NOT NULL,              -- Corregido de EstrucuturaOrganica
            ConocimientoLegal TINYINT NOT NULL,               -- Corregido de ConociminetoLegal
            MetodologiaInnovacion TEXT(150) NOT NULL,         -- Corregido de MEtologiaInnovacion
            HerramientaTecnologicas TEXT(150) NOT NULL,       -- Corregido de HerammientoTecnologicas
            Marca TEXT(150) NOT NULL,
            AplicacionMetodologia TINYINT NOT NULL,
            ImpactoAmbiental TINYINT NOT NULL,
            ImpactoSocial TINYINT NOT NULL,
            Viabilidad TINYINT NOT NULL,
            PRIMARY KEY (idDiagnosticos),
            INDEX fk_Diagnosticos_SectoEconomico1_idx (SectoEconomico_idSectoEconomico),
            INDEX fk_Diagnosticos_Emprendimiento1_idx (Emprendimiento_idEmprendimiento),
            CONSTRAINT fk_Diagnosticos_SectoEconomico1
                FOREIGN KEY (SectoEconomico_idSectoEconomico)
                REFERENCES SectoEconomico (idSectoEconomico),
            CONSTRAINT fk_Diagnosticos_Emprendimiento1
                FOREIGN KEY (Emprendimiento_idEmprendimiento)
                REFERENCES Emprendimiento (idEmprendimiento)
        ) 
        """
        cursor.execute(create_Diagnosticos)

        # Tabla Modalidad
        create_Modalidad = """
        CREATE TABLE IF NOT EXISTS Modalidad (
            idModalidad INT NOT NULL,
            Presencial TINYINT NOT NULL,
            Distancia TINYINT NOT NULL,               
            Enlace_virtual VARCHAR(45) NOT NULL,       
            Lugar VARCHAR(45) NOT NULL,
            PRIMARY KEY (idModalidad)
        ) 
        """
        cursor.execute(create_Modalidad)

        # Tabla Fecha_y_Horarios
        create_Fecha_y_Horarios = """
        CREATE TABLE IF NOT EXISTS Fecha_y_Horarios (
            idFecha_y_Horarios INT NOT NULL,
            Fecha_inicio DATETIME NOT NULL,
            Hora_inicio DATETIME NOT NULL,
            Fecha_fin DATETIME NOT NULL,
            Hora_fin DATETIME NOT NULL,
            PRIMARY KEY (idFecha_y_Horarios)
        ) 
        """
        cursor.execute(create_Fecha_y_Horarios)

        # Tabla Asesorias
        create_Asesorias = """
        CREATE TABLE IF NOT EXISTS Asesorias (
            idAsesorias INT NOT NULL AUTO_INCREMENT,
            Nombre_de_asesoria VARCHAR(45) NOT NULL,
            Descripcion VARCHAR(45) NOT NULL,
            Fecha_asesoria DATETIME NOT NULL,
            Comentarios VARCHAR(45) NOT NULL,
            Fecha_creacion DATETIME NOT NULL,
            Fecha_actualizacion DATETIME NOT NULL,
            confimacion VARCHAR(45) NOT NULL,
            Usuarios_idUsuarios INT NOT NULL,
            Modalidad_idModalidad INT NOT NULL,
            Fecha_y_Horarios_idFecha_y_Horarios INT NOT NULL,
            PRIMARY KEY (idAsesorias),
            INDEX fk_Asesorias_Usuarios1_idx (Usuarios_idUsuarios),
            INDEX fk_Asesorias_Modalidad1_idx (Modalidad_idModalidad),
            INDEX fk_Asesorias_Fecha_y_Horarios1_idx (Fecha_y_Horarios_idFecha_y_Horarios),
            CONSTRAINT fk_Asesorias_Usuarios1
                FOREIGN KEY (Usuarios_idUsuarios)
                REFERENCES Usuarios (idUsuarios),
            CONSTRAINT fk_Asesorias_Modalidad1
                FOREIGN KEY (Modalidad_idModalidad)
                REFERENCES Modalidad (idModalidad),
            CONSTRAINT fk_Asesorias_Fecha_y_Horarios1
                FOREIGN KEY (Fecha_y_Horarios_idFecha_y_Horarios)
                REFERENCES Fecha_y_Horarios (idFecha_y_Horarios)
        ) 
        """
        cursor.execute(create_Asesorias)

        # Tabla Tipo_evento
        create_Tipo_evento = """
        CREATE TABLE IF NOT EXISTS Tipo_evento (
            idTipo_evento INT NOT NULL,
            Academico VARCHAR(45) NOT NULL,
            Cultura VARCHAR(45) NOT NULL,
            Deportivo VARCHAR(45) NOT NULL,
            Social VARCHAR(45) NOT NULL,
            Conerencia VARCHAR(45) NOT NULL,
            PRIMARY KEY (idTipo_evento)
        ) 
        """
        cursor.execute(create_Tipo_evento)

        # Tabla Eventos
        create_Eventos = """
        CREATE TABLE IF NOT EXISTS Eventos (
            idEventos INT NOT NULL,
            Nombre_evento VARCHAR(45) NOT NULL,
            Descripcion_evento VARCHAR(45) NOT NULL,
            Tipo_evento_idTipo_evento INT NOT NULL,
            Modalidad_idModalidad INT NOT NULL,
            Fecha_y_Horarios_idFecha_y_Horarios INT NOT NULL,
            Estado VARCHAR(45) NOT NULL,
            Capacidad_maxima INT NOT NULL,
            Requiere_registro TINYINT NOT NULL,
            Fecha_creacion DATETIME NOT NULL,          -- Corregido de Fecha_crecion
            Fecha_actualizacion DATETIME NOT NULL,
            PRIMARY KEY (idEventos),
            INDEX fk_Eventos_Tipo_evento1_idx (Tipo_evento_idTipo_evento),
            INDEX fk_Eventos_Modalidad1_idx (Modalidad_idModalidad),
            INDEX fk_Eventos_Fecha_y_Horarios1_idx (Fecha_y_Horarios_idFecha_y_Horarios),
            CONSTRAINT fk_Eventos_Tipo_evento1
                FOREIGN KEY (Tipo_evento_idTipo_evento)
                REFERENCES Tipo_evento (idTipo_evento),
            CONSTRAINT fk_Eventos_Modalidad1
                FOREIGN KEY (Modalidad_idModalidad)
                REFERENCES Modalidad (idModalidad),
            CONSTRAINT fk_Eventos_Fecha_y_Horarios1
                FOREIGN KEY (Fecha_y_Horarios_idFecha_y_Horarios)
                REFERENCES Fecha_y_Horarios (idFecha_y_Horarios)
        ) 
        """
        cursor.execute(create_Eventos)

        # Tabla Usuarios_has_Eventos
        create_Usuarios_has_Eventos = """
        CREATE TABLE IF NOT EXISTS Usuarios_has_Eventos (
            Usuarios_idUsuarios INT NOT NULL,
            Eventos_idEventos INT NOT NULL,
            PRIMARY KEY (Usuarios_idUsuarios, Eventos_idEventos),
            INDEX fk_Usuarios_has_Eventos_Eventos1_idx (Eventos_idEventos),
            INDEX fk_Usuarios_has_Eventos_Usuarios1_idx (Usuarios_idUsuarios),
            CONSTRAINT fk_Usuarios_has_Eventos_Usuarios1
                FOREIGN KEY (Usuarios_idUsuarios)
                REFERENCES Usuarios (idUsuarios),
            CONSTRAINT fk_Usuarios_has_Eventos_Eventos1
                FOREIGN KEY (Eventos_idEventos)
                REFERENCES Eventos (idEventos)
        ) 
        """
        cursor.execute(create_Usuarios_has_Eventos)

        print("Tablas creadas exitosamente o ya existían.")

except Error as e:
    print("Error al conectarse a MySQL:", e)
    
finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada con la base de datos.")