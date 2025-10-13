\# **Proyecto SGEMD**



\## Requisitos previos



\- Node js

\- jsonwebtoken 9.0.2

\- bcryptjs 3.0.2



\## Base de datos



\### Descripción



En este proyecto, se ha creado una base de datos utilizando Python, esta base de datos esta construida para ser un sistema de gestión de emprendimiento en la empresa Minuto de Dios.



\### Instrucciones



1\. La tabla usuarios de la base de datos debe contener un parámetro de Password, este parámetro contener una cadena de caracteres.

2\. Todos los errores de escritura deberán ser corregidos.

3\. Se deberá mantener la estructura de la base de datos.



\### Código Base





```Python

\# init\_db.py

import mysql.connector as msql

from mysql.connector import Error 



try:

&nbsp;   connection = msql.connect(

&nbsp;       host="localhost",

&nbsp;       port="3306",

&nbsp;       user="root",

&nbsp;       password=""

&nbsp;   )



&nbsp;   if connection.is\_connected():

&nbsp;       cursor = connection.cursor()

&nbsp;       cursor.execute("CREATE DATABASE IF NOT EXISTS DB\_SEGMED")

&nbsp;       print("Base de datos creada exitosamente o ya existía.")



&nbsp;       cursor.execute("USE DB\_SEGMED")



&nbsp;       # Tabla Modulos

&nbsp;       create\_Modulos = """

&nbsp;       CREATE TABLE IF NOT EXISTS Modulos (

&nbsp;           idModulos INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Asistencia VARCHAR(45) NOT NULL,

&nbsp;           Practicas VARCHAR(45) NOT NULL,

&nbsp;           OpcionGrado VARCHAR(45) NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           PRIMARY KEY (idModulos)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Modulos)



&nbsp;       # Tabla Municipios

&nbsp;       create\_Municipios = """

&nbsp;       CREATE TABLE IF NOT EXISTS Municipios (

&nbsp;           idMunicipio INT NOT NULL,

&nbsp;           Nombre VARCHAR(45) NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           PRIMARY KEY (idMunicipio)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Municipios)



&nbsp;       # Tabla ProgramaAcademico

&nbsp;       create\_ProgramaAcademico = """

&nbsp;       CREATE TABLE IF NOT EXISTS ProgramaAcademico (

&nbsp;           idProgramaAcademico INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Nombre VARCHAR(45) NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           PRIMARY KEY (idProgramaAcademico)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_ProgramaAcademico)



&nbsp;       # Tabla Roles

&nbsp;       create\_Roles = """

&nbsp;       CREATE TABLE IF NOT EXISTS Roles (

&nbsp;           idRoles INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Nombre VARCHAR(45) NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           PRIMARY KEY (idRoles)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Roles)



&nbsp;       # Tabla TipoDocumentos

&nbsp;       create\_TipoDocumentos = """

&nbsp;       CREATE TABLE IF NOT EXISTS TipoDocumentos (

&nbsp;           idTipoDocumento INT NOT NULL AUTO\_INCREMENT,

&nbsp;           TipoDocumento VARCHAR(45) NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           PRIMARY KEY (idTipoDocumento)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_TipoDocumentos)



&nbsp;       # Tabla TipoUsuarios

&nbsp;       create\_TipoUsuarios = """

&nbsp;       CREATE TABLE IF NOT EXISTS TipoUsuarios (

&nbsp;           idTipoUsuarios INT NOT NULL AUTO\_INCREMENT,

&nbsp;           TipodeUsuario VARCHAR(45) NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           PRIMARY KEY (idTipoUsuarios)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_TipoUsuarios)



&nbsp;       # Tabla CentroUniversitarios

&nbsp;       create\_CentroUniversitarios = """

&nbsp;       CREATE TABLE IF NOT EXISTS CentroUniversitarios (

&nbsp;           idCentroUniversitarios INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Nombre VARCHAR(45) NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           PRIMARY KEY (idCentroUniversitarios)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_CentroUniversitarios)



&nbsp;       # Tabla TipoPoblacion

&nbsp;       create\_TipoPoblacion = """

&nbsp;       CREATE TABLE IF NOT EXISTS TipoPoblacion (

&nbsp;           idTipoPoblacion INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Nombre VARCHAR(45) NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           PRIMARY KEY (idTipoPoblacion)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_TipoPoblacion)



&nbsp;       # Tabla Usuarios con relaciones

&nbsp;       create\_Usuarios = """

&nbsp;       CREATE TABLE IF NOT EXISTS Usuarios (

&nbsp;           idUsuarios INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Nombre VARCHAR(45) NOT NULL,

&nbsp;           CorreoInstitucional VARCHAR(45) NOT NULL,

&nbsp;           CorreoPersonal VARCHAR(45) NOT NULL,

&nbsp;           Celular VARCHAR(45) NOT NULL,

&nbsp;           Telefono VARCHAR(45) NOT NULL,

&nbsp;           Direcccion VARCHAR(45) NOT NULL,

&nbsp;           Genero VARCHAR(45) NOT NULL,

&nbsp;           EstadoCivil VARCHAR(45) NOT NULL,

&nbsp;           FechaNacimiento DATE NOT NULL,

&nbsp;           Modulos\_idModulos INT,

&nbsp;           Municipios\_idMunicipio INT,

&nbsp;           ProgramaAcademico\_idProgramaAcademico INT,

&nbsp;           Roles\_idRoles1 INT,

&nbsp;           TipoDocumentos\_idTipoDocumento INT,

&nbsp;           TipoUsuarios\_idTipoUsuarios INT,

&nbsp;           ProgramaAcademico\_idProgramaAcademico1 INT NOT NULL,

&nbsp;           CentroUniversitarios\_idCentroUniversitarios INT NOT NULL,

&nbsp;           Estado TINYINT NOT NULL,

&nbsp;           Semestre VARCHAR(45) NOT NULL,

&nbsp;           Modalidad VARCHAR(45) NOT NULL,

&nbsp;           TipoPoblacion\_idTipoPoblacion INT,

&nbsp;           FechaCreacion DATE,

&nbsp;           FechaActualizacion DATE,

&nbsp;           PRIMARY KEY (idUsuarios),

&nbsp;           INDEX fk\_Usuarios\_Modulos\_idx (Modulos\_idModulos),

&nbsp;           INDEX fk\_Usuarios\_Municipios1\_idx (Municipios\_idMunicipio),

&nbsp;           INDEX fk\_Usuarios\_ProgramaAcademico1\_idx (ProgramaAcademico\_idProgramaAcademico),

&nbsp;           INDEX fk\_Usuarios\_Roles2\_idx (Roles\_idRoles1),

&nbsp;           INDEX fk\_Usuarios\_TipoDocumentos1\_idx (TipoDocumentos\_idTipoDocumento),

&nbsp;           INDEX fk\_Usuarios\_TipoUsuarios1\_idx (TipoUsuarios\_idTipoUsuarios),

&nbsp;           INDEX fk\_Usuarios\_ProgramaAcademico2\_idx (ProgramaAcademico\_idProgramaAcademico1),

&nbsp;           INDEX fk\_Usuarios\_CentroUniversitarios1\_idx (CentroUniversitarios\_idCentroUniversitarios),

&nbsp;           INDEX fk\_Usuarios\_TipoPoblacion1\_idx (TipoPoblacion\_idTipoPoblacion),

&nbsp;           CONSTRAINT fk\_Usuarios\_Modulos

&nbsp;               FOREIGN KEY (Modulos\_idModulos)

&nbsp;               REFERENCES Modulos (idModulos),

&nbsp;           CONSTRAINT fk\_Usuarios\_Municipios1

&nbsp;               FOREIGN KEY (Municipios\_idMunicipio)

&nbsp;               REFERENCES Municipios (idMunicipio),

&nbsp;           CONSTRAINT fk\_Usuarios\_ProgramaAcademico1

&nbsp;               FOREIGN KEY (ProgramaAcademico\_idProgramaAcademico)

&nbsp;               REFERENCES ProgramaAcademico (idProgramaAcademico),

&nbsp;           CONSTRAINT fk\_Usuarios\_Roles2

&nbsp;               FOREIGN KEY (Roles\_idRoles1)

&nbsp;               REFERENCES Roles (idRoles),

&nbsp;           CONSTRAINT fk\_Usuarios\_TipoDocumentos1

&nbsp;               FOREIGN KEY (TipoDocumentos\_idTipoDocumento)

&nbsp;               REFERENCES TipoDocumentos (idTipoDocumento),

&nbsp;           CONSTRAINT fk\_Usuarios\_TipoUsuarios1

&nbsp;               FOREIGN KEY (TipoUsuarios\_idTipoUsuarios)

&nbsp;               REFERENCES TipoUsuarios (idTipoUsuarios),

&nbsp;           CONSTRAINT fk\_Usuarios\_ProgramaAcademico2

&nbsp;               FOREIGN KEY (ProgramaAcademico\_idProgramaAcademico1)

&nbsp;               REFERENCES ProgramaAcademico (idProgramaAcademico),

&nbsp;           CONSTRAINT fk\_Usuarios\_CentroUniversitarios1

&nbsp;               FOREIGN KEY (CentroUniversitarios\_idCentroUniversitarios)

&nbsp;               REFERENCES CentroUniversitarios (idCentroUniversitarios),

&nbsp;           CONSTRAINT fk\_Usuarios\_TipoPoblacion1

&nbsp;               FOREIGN KEY (TipoPoblacion\_idTipoPoblacion)

&nbsp;               REFERENCES TipoPoblacion (idTipoPoblacion)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Usuarios)



&nbsp;       # Tabla EtapadeEmpedimiento

&nbsp;       create\_EtapadeEmpedimiento = """

&nbsp;       CREATE TABLE IF NOT EXISTS EtapadeEmpedimiento (

&nbsp;           idEtapadeEmpedimiento INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Estado TINYINT NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           TipoEtapa VARCHAR(45) NOT NULL,

&nbsp;           PRIMARY KEY (idEtapadeEmpedimiento)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_EtapadeEmpedimiento)



&nbsp;       # Tabla Emprendimiento

&nbsp;       create\_Emprendimiento = """

&nbsp;       CREATE TABLE IF NOT EXISTS Emprendimiento (

&nbsp;           idEmprendimiento INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Nombre VARCHAR(45) NOT NULL,

&nbsp;           Descripcion VARCHAR(45) NOT NULL,

&nbsp;           TipoEmprendimiento VARCHAR(45) NOT NULL,  -- Corregido de TipoEmpreedimiento

&nbsp;           SectorProductivo VARCHAR(45) NOT NULL,    -- Corregido de SectorPruductivo

&nbsp;           RedesSociales TINYINT NOT NULL,

&nbsp;           Acompanamiento TINYINT NOT NULL,          -- Corregido de Acompañamiento (evita la ñ)

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           ActaCompromiso TEXT(150) NOT NULL,

&nbsp;           EtapadeEmpedimiento\_idEtapadeEmpedimiento INT NOT NULL,

&nbsp;           PRIMARY KEY (idEmprendimiento),

&nbsp;           INDEX fk\_Emprendimiento\_EtapadeEmpedimiento1\_idx (EtapadeEmpedimiento\_idEtapadeEmpedimiento),

&nbsp;           CONSTRAINT fk\_Emprendimiento\_EtapadeEmpedimiento1

&nbsp;               FOREIGN KEY (EtapadeEmpedimiento\_idEtapadeEmpedimiento)

&nbsp;               REFERENCES EtapadeEmpedimiento (idEtapadeEmpedimiento)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Emprendimiento)



&nbsp;       # Tabla Seguimientos

&nbsp;       create\_Seguimientos = """

&nbsp;       CREATE TABLE IF NOT EXISTS Seguimientos (

&nbsp;           idSeguimientos INT NOT NULL AUTO\_INCREMENT,

&nbsp;           histproal VARCHAR(45) NOT NULL,

&nbsp;           TipoSeguimiento VARCHAR(45) NOT NULL,

&nbsp;           Descripcion VARCHAR(45) NOT NULL,

&nbsp;           Seguimientoscol VARCHAR(45) NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           PRIMARY KEY (idSeguimientos)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Seguimientos)



&nbsp;       # Tabla Asisitencia

&nbsp;       create\_Asisitencia = """

&nbsp;       CREATE TABLE IF NOT EXISTS Asisitencia (

&nbsp;           idAsisitencia INT NOT NULL AUTO\_INCREMENT,

&nbsp;           FeedBack VARCHAR(45) NOT NULL,

&nbsp;           Emprendimiento\_idEmprendimiento INT NOT NULL,

&nbsp;           FechaCreacion DATE NOT NULL,

&nbsp;           FechaActualizacion DATE NOT NULL,

&nbsp;           Seguimientos\_idSeguimientos INT NOT NULL,

&nbsp;           PRIMARY KEY (idAsisitencia),

&nbsp;           INDEX fk\_Asisitencia\_Emprendimiento1\_idx (Emprendimiento\_idEmprendimiento),

&nbsp;           INDEX fk\_Asisitencia\_Seguimientos1\_idx (Seguimientos\_idSeguimientos),

&nbsp;           CONSTRAINT fk\_Asisitencia\_Emprendimiento1

&nbsp;               FOREIGN KEY (Emprendimiento\_idEmprendimiento)

&nbsp;               REFERENCES Emprendimiento (idEmprendimiento),

&nbsp;           CONSTRAINT fk\_Asisitencia\_Seguimientos1

&nbsp;               FOREIGN KEY (Seguimientos\_idSeguimientos)

&nbsp;               REFERENCES Seguimientos (idSeguimientos)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Asisitencia)



&nbsp;       # Tabla SectoEconomico

&nbsp;       create\_SectoEconomico = """

&nbsp;       CREATE TABLE IF NOT EXISTS SectoEconomico (

&nbsp;           idSectoEconomico INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Nombre VARCHAR(45) NOT NULL,

&nbsp;           PRIMARY KEY (idSectoEconomico)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_SectoEconomico)



&nbsp;       # Tabla Diagnosticos

&nbsp;       create\_Diagnosticos = """

&nbsp;       CREATE TABLE IF NOT EXISTS Diagnosticos (

&nbsp;           idDiagnosticos INT NOT NULL AUTO\_INCREMENT,

&nbsp;           FechaEmprendimiento DATE NOT NULL,                -- Corregido de FechaEmpredimiento

&nbsp;           AreaEstrategia VARCHAR(45) NOT NULL,

&nbsp;           Diferencial TINYINT NOT NULL,

&nbsp;           Planeacion TINYINT NOT NULL,

&nbsp;           MercadoObjetivo VARCHAR(45) NOT NULL,             -- Corregido de Mercadoobjetivo

&nbsp;           Tendencias TINYINT NOT NULL,

&nbsp;           Canales TINYINT NOT NULL,

&nbsp;           DescripcionPromocion TEXT(150) NOT NULL,

&nbsp;           SectoEconomico\_idSectoEconomico INT NOT NULL,

&nbsp;           Emprendimiento\_idEmprendimiento INT NOT NULL,

&nbsp;           Presentacion TINYINT NOT NULL,

&nbsp;           PasosElaboracion TINYINT NOT NULL,

&nbsp;           SituacionFinanciera TINYINT NOT NULL,             -- Corregido de SituacionFinaciera

&nbsp;           FuenteFinanciero TEXT(150) NOT NULL,              -- Corregido de FuenteFinaciero

&nbsp;           EstructuraOrganica TINYINT NOT NULL,              -- Corregido de EstrucuturaOrganica

&nbsp;           ConocimientoLegal TINYINT NOT NULL,               -- Corregido de ConociminetoLegal

&nbsp;           MetodologiaInnovacion TEXT(150) NOT NULL,         -- Corregido de MEtologiaInnovacion

&nbsp;           HerramientaTecnologicas TEXT(150) NOT NULL,       -- Corregido de HerammientoTecnologicas

&nbsp;           Marca TEXT(150) NOT NULL,

&nbsp;           AplicacionMetodologia TINYINT NOT NULL,

&nbsp;           ImpactoAmbiental TINYINT NOT NULL,

&nbsp;           ImpactoSocial TINYINT NOT NULL,

&nbsp;           Viabilidad TINYINT NOT NULL,

&nbsp;           PRIMARY KEY (idDiagnosticos),

&nbsp;           INDEX fk\_Diagnosticos\_SectoEconomico1\_idx (SectoEconomico\_idSectoEconomico),

&nbsp;           INDEX fk\_Diagnosticos\_Emprendimiento1\_idx (Emprendimiento\_idEmprendimiento),

&nbsp;           CONSTRAINT fk\_Diagnosticos\_SectoEconomico1

&nbsp;               FOREIGN KEY (SectoEconomico\_idSectoEconomico)

&nbsp;               REFERENCES SectoEconomico (idSectoEconomico),

&nbsp;           CONSTRAINT fk\_Diagnosticos\_Emprendimiento1

&nbsp;               FOREIGN KEY (Emprendimiento\_idEmprendimiento)

&nbsp;               REFERENCES Emprendimiento (idEmprendimiento)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Diagnosticos)



&nbsp;       # Tabla Modalidad

&nbsp;       create\_Modalidad = """

&nbsp;       CREATE TABLE IF NOT EXISTS Modalidad (

&nbsp;           idModalidad INT NOT NULL,

&nbsp;           Presencial TINYINT NOT NULL,

&nbsp;           Distancia TINYINT NOT NULL,               

&nbsp;           Enlace\_virtual VARCHAR(45) NOT NULL,       

&nbsp;           Lugar VARCHAR(45) NOT NULL,

&nbsp;           PRIMARY KEY (idModalidad)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Modalidad)



&nbsp;       # Tabla Fecha\_y\_Horarios

&nbsp;       create\_Fecha\_y\_Horarios = """

&nbsp;       CREATE TABLE IF NOT EXISTS Fecha\_y\_Horarios (

&nbsp;           idFecha\_y\_Horarios INT NOT NULL,

&nbsp;           Fecha\_inicio DATETIME NOT NULL,

&nbsp;           Hora\_inicio DATETIME NOT NULL,

&nbsp;           Fecha\_fin DATETIME NOT NULL,

&nbsp;           Hora\_fin DATETIME NOT NULL,

&nbsp;           PRIMARY KEY (idFecha\_y\_Horarios)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Fecha\_y\_Horarios)



&nbsp;       # Tabla Asesorias

&nbsp;       create\_Asesorias = """

&nbsp;       CREATE TABLE IF NOT EXISTS Asesorias (

&nbsp;           idAsesorias INT NOT NULL AUTO\_INCREMENT,

&nbsp;           Nombre\_de\_asesoria VARCHAR(45) NOT NULL,

&nbsp;           Descripcion VARCHAR(45) NOT NULL,

&nbsp;           Fecha\_asesoria DATETIME NOT NULL,

&nbsp;           Comentarios VARCHAR(45) NOT NULL,

&nbsp;           Fecha\_creacion DATETIME NOT NULL,

&nbsp;           Fecha\_actualizacion DATETIME NOT NULL,

&nbsp;           confimacion VARCHAR(45) NOT NULL,

&nbsp;           Usuarios\_idUsuarios INT NOT NULL,

&nbsp;           Modalidad\_idModalidad INT NOT NULL,

&nbsp;           Fecha\_y\_Horarios\_idFecha\_y\_Horarios INT NOT NULL,

&nbsp;           PRIMARY KEY (idAsesorias),

&nbsp;           INDEX fk\_Asesorias\_Usuarios1\_idx (Usuarios\_idUsuarios),

&nbsp;           INDEX fk\_Asesorias\_Modalidad1\_idx (Modalidad\_idModalidad),

&nbsp;           INDEX fk\_Asesorias\_Fecha\_y\_Horarios1\_idx (Fecha\_y\_Horarios\_idFecha\_y\_Horarios),

&nbsp;           CONSTRAINT fk\_Asesorias\_Usuarios1

&nbsp;               FOREIGN KEY (Usuarios\_idUsuarios)

&nbsp;               REFERENCES Usuarios (idUsuarios),

&nbsp;           CONSTRAINT fk\_Asesorias\_Modalidad1

&nbsp;               FOREIGN KEY (Modalidad\_idModalidad)

&nbsp;               REFERENCES Modalidad (idModalidad),

&nbsp;           CONSTRAINT fk\_Asesorias\_Fecha\_y\_Horarios1

&nbsp;               FOREIGN KEY (Fecha\_y\_Horarios\_idFecha\_y\_Horarios)

&nbsp;               REFERENCES Fecha\_y\_Horarios (idFecha\_y\_Horarios)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Asesorias)



&nbsp;       # Tabla Tipo\_evento

&nbsp;       create\_Tipo\_evento = """

&nbsp;       CREATE TABLE IF NOT EXISTS Tipo\_evento (

&nbsp;           idTipo\_evento INT NOT NULL,

&nbsp;           Academico VARCHAR(45) NOT NULL,

&nbsp;           Cultura VARCHAR(45) NOT NULL,

&nbsp;           Deportivo VARCHAR(45) NOT NULL,

&nbsp;           Social VARCHAR(45) NOT NULL,

&nbsp;           Conerencia VARCHAR(45) NOT NULL,

&nbsp;           PRIMARY KEY (idTipo\_evento)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Tipo\_evento)



&nbsp;       # Tabla Eventos

&nbsp;       create\_Eventos = """

&nbsp;       CREATE TABLE IF NOT EXISTS Eventos (

&nbsp;           idEventos INT NOT NULL,

&nbsp;           Nombre\_evento VARCHAR(45) NOT NULL,

&nbsp;           Descripcion\_evento VARCHAR(45) NOT NULL,

&nbsp;           Tipo\_evento\_idTipo\_evento INT NOT NULL,

&nbsp;           Modalidad\_idModalidad INT NOT NULL,

&nbsp;           Fecha\_y\_Horarios\_idFecha\_y\_Horarios INT NOT NULL,

&nbsp;           Estado VARCHAR(45) NOT NULL,

&nbsp;           Capacidad\_maxima INT NOT NULL,

&nbsp;           Requiere\_registro TINYINT NOT NULL,

&nbsp;           Fecha\_creacion DATETIME NOT NULL,          -- Corregido de Fecha\_crecion

&nbsp;           Fecha\_actualizacion DATETIME NOT NULL,

&nbsp;           PRIMARY KEY (idEventos),

&nbsp;           INDEX fk\_Eventos\_Tipo\_evento1\_idx (Tipo\_evento\_idTipo\_evento),

&nbsp;           INDEX fk\_Eventos\_Modalidad1\_idx (Modalidad\_idModalidad),

&nbsp;           INDEX fk\_Eventos\_Fecha\_y\_Horarios1\_idx (Fecha\_y\_Horarios\_idFecha\_y\_Horarios),

&nbsp;           CONSTRAINT fk\_Eventos\_Tipo\_evento1

&nbsp;               FOREIGN KEY (Tipo\_evento\_idTipo\_evento)

&nbsp;               REFERENCES Tipo\_evento (idTipo\_evento),

&nbsp;           CONSTRAINT fk\_Eventos\_Modalidad1

&nbsp;               FOREIGN KEY (Modalidad\_idModalidad)

&nbsp;               REFERENCES Modalidad (idModalidad),

&nbsp;           CONSTRAINT fk\_Eventos\_Fecha\_y\_Horarios1

&nbsp;               FOREIGN KEY (Fecha\_y\_Horarios\_idFecha\_y\_Horarios)

&nbsp;               REFERENCES Fecha\_y\_Horarios (idFecha\_y\_Horarios)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Eventos)



&nbsp;       # Tabla Usuarios\_has\_Eventos

&nbsp;       create\_Usuarios\_has\_Eventos = """

&nbsp;       CREATE TABLE IF NOT EXISTS Usuarios\_has\_Eventos (

&nbsp;           Usuarios\_idUsuarios INT NOT NULL,

&nbsp;           Eventos\_idEventos INT NOT NULL,

&nbsp;           PRIMARY KEY (Usuarios\_idUsuarios, Eventos\_idEventos),

&nbsp;           INDEX fk\_Usuarios\_has\_Eventos\_Eventos1\_idx (Eventos\_idEventos),

&nbsp;           INDEX fk\_Usuarios\_has\_Eventos\_Usuarios1\_idx (Usuarios\_idUsuarios),

&nbsp;           CONSTRAINT fk\_Usuarios\_has\_Eventos\_Usuarios1

&nbsp;               FOREIGN KEY (Usuarios\_idUsuarios)

&nbsp;               REFERENCES Usuarios (idUsuarios),

&nbsp;           CONSTRAINT fk\_Usuarios\_has\_Eventos\_Eventos1

&nbsp;               FOREIGN KEY (Eventos\_idEventos)

&nbsp;               REFERENCES Eventos (idEventos)

&nbsp;       ) 

&nbsp;       """

&nbsp;       cursor.execute(create\_Usuarios\_has\_Eventos)



&nbsp;       print("Tablas creadas exitosamente o ya existían.")



except Error as e:

&nbsp;   print("Error al conectarse a MySQL:", e)

&nbsp;   

finally:

&nbsp;   if connection and connection.is\_connected():

&nbsp;       cursor.close()

&nbsp;       connection.close()

&nbsp;       print("Conexión cerrada con la base de datos.")

```



\## Ejercicio: Implementación de Auth



\### Descripción



En este ejercicio, extenderemos el sistema anterior para implementar un modelo de autenticación, y al mismo tiempo la base de datos recibirá un dato cifrado utilizando la librería bcryptjs, la autenticación se realizará en POSTMAN y la visualización deberá mantenerse.



\### Instrucciones



1\. Modifica el código para implementar un modelo de autenticación en POSTMAN.

2\. La base de datos recibirá la contraseña cifrada utilizando la librería bcryptjs.

3\. Para la autenticación se usaran tokens de la librería jsonwebtoken.



\### Código base para el ejercicio



```JavaScript

// app.js

const express = require('express')

const bodyParser = require('body-parser')

const cors = require('cors')

const { testConnection } = require('./config/db.config')



// Importar rutas

const userRoutes = require('./routes/user.routes')

const moduleRoutes = require('./routes/module.routes')

const municipalitiesRoutes = require('./routes/municipalities.routes')

const academicProgramRoutes = require('./routes/academicProgram.routes')

const roles = require('./routes/roles.routes')

const tipoDoc = require('./routes/typeDoc.routes')

const tipoUsuario = require('./routes/typeUsers.routes')

const uniCenters = require('./routes/uniCenters.routes')

const tipoPoblacion = require('./routes/typePop.routes')

const EtapadeEmprendimiento = require('./routes/entrepStage.routes')

const emprendimiento = require('./routes/entrepreneurship.routes')

const tracing = require('./routes/tracing.routes')

const assistance = require('./routes/assistance.routes')

const econoSector = require('./routes/econoSector.routes')

const diagnosis = require('./routes/diagnosis.routes')

const mode = require('./routes/mode.routes')

const advice = require('./routes/advice.routes')

const event = require('./routes/event.routes')

const typeEvent = require('./routes/typeEvent.routes')

const dateTimes = require('./routes/dateTimes.routes')



// Crear la aplicación



const app = express()

const PORT = process.env.PORT || 3005



// Middleware

app.use(cors())

app.use(bodyParser.json())

app.use(bodyParser.urlencoded({ extended: true }))



// Rutas

app.use('/segmed/users', userRoutes)

app.use('/segmed/module', moduleRoutes)

app.use('/segmed/municipalities', municipalitiesRoutes)

app.use('/segmed/academic-programs', academicProgramRoutes)

app.use('/segmed/roles', roles)

app.use('/segmed/type-doc', tipoDoc)

app.use('/segmed/type-users', tipoUsuario)

app.use('/segmed/uni-centers', uniCenters)

app.use('/segmed/type-pop', tipoPoblacion)

app.use('/segmed/entrep-stage', EtapadeEmprendimiento)

app.use('/segmed/entrepreneurship', emprendimiento)

app.use('/segmed/tracing', tracing)

app.use('/segmed/assistance', assistance)

app.use('/segmed/econo-sector', econoSector)

app.use('/segmed/diagnosis', diagnosis)

app.use('/segmed/mode', mode)

app.use('/segmed/advice', advice)

app.use('/segmed/event', event)

app.use('/segmed/type-event', typeEvent)

app.use('/segmed/date-times', dateTimes)



// Ruta de prueba   

app.get('/', (req, res) => {

&nbsp;   res.json({ 

&nbsp;       message: 'Bienvenido al API de SGEMD',

&nbsp;       endpoints: {

&nbsp;           users: '/segmed/users',

&nbsp;           modules: '/segmed/modules',

&nbsp;           municipalities: '/segmed/municipalities',

&nbsp;           academicPrograms: '/segmed/academic-programs',

&nbsp;           roles: '/segmed/roles',

&nbsp;           tipoDoc: '/segmed/tipo-doc',

&nbsp;           tipoUsuario: '/segmed/tipo-usuarios',

&nbsp;           uniCenters: '/segmed/uni-centers',

&nbsp;           tipoPoblacion: '/segmed/tipo-poblacion',

&nbsp;           etapadeEmpedimiento: '/segmed/etapade-empedimiento',

&nbsp;           emprendimiento: '/segmed/emprendimiento',

&nbsp;           tracing: '/segmed/tracing',

&nbsp;           assistance: '/segmed/assistance',

&nbsp;           econoSector: '/segmed/econo-sector',

&nbsp;           diagnosis: '/segmed/diagnosis',

&nbsp;           mode: '/segmed/mode',

&nbsp;           advice: '/segmed/advice',

&nbsp;           event: '/segmed/event',

&nbsp;           typeEvent: '/segmed/typeEvent',

&nbsp;           dateTimes: '/segmed/dateTimes'

&nbsp;       }

&nbsp;   })

})



// Manejo de errores

app.use((err, req, res, next) => {

&nbsp;   console.error(err.stack)

&nbsp;   res.status(500).json({ success: false, error: 'Error interno del servidor' });

})



// Ruta no encontrada

app.use('\*', (req, res) => {

&nbsp;   res.status(404).json({ success: false, error: 'Ruta no encontrada' });

})



// Inicializar la aplicación

async function startServer() {

&nbsp;   const dbConnected = await testConnection();

&nbsp;   if (!dbConnected) {

&nbsp;       console.error('No se pudo conectar a la base de datos. Verifica la configuración.');

&nbsp;       process.exit(1);

&nbsp;   }



&nbsp;   app.listen(PORT, () => {

&nbsp;       console.log(`Servidor ejecutándose en http://localhost:${PORT}`);

&nbsp;       console.log(`API disponible en http://localhost:${PORT}/segmed/`);

&nbsp;   })

}



startServer()



```



```JavaScript

// users.service.js

const { pool } = require('../config/db.config');



// Obtener todos los usuarios

exports.findAll = async () => {

&nbsp;   const \[rows] = await pool.execute(`

&nbsp;       SELECT u.idUsuarios, u.Nombre, u.CorreoInstitucional, u.CorreoPersonal, 

&nbsp;              u.Celular, u.Telefono, u.Estado, u.Semestre, u.Modalidad,

&nbsp;              tu.TipodeUsuario, pa.Nombre as ProgramaAcademico

&nbsp;       FROM Usuarios u

&nbsp;       INNER JOIN TipoUsuarios tu ON u.TipoUsuarios\_idTipoUsuarios = tu.idTipoUsuarios

&nbsp;       LEFT JOIN ProgramaAcademico pa ON u.ProgramaAcademico\_idProgramaAcademico = pa.idProgramaAcademico

&nbsp;       WHERE u.Estado = 1

&nbsp;   `);

&nbsp;   return rows;

}

// Obtener todos los estudiantes

exports.findAllStudents = async () => {

&nbsp;   const \[rows] = await pool.execute(`

&nbsp;       SELECT u.idUsuarios, u.Nombre, u.CorreoInstitucional, u.CorreoPersonal, 

&nbsp;              u.Celular, u.Telefono, u.Estado, u.Semestre, u.Modalidad,

&nbsp;              tu.TipodeUsuario, pa.Nombre as ProgramaAcademico

&nbsp;       FROM Usuarios u

&nbsp;       INNER JOIN TipoUsuarios tu ON u.TipoUsuarios\_idTipoUsuarios = tu.idTipoUsuarios

&nbsp;       LEFT JOIN ProgramaAcademico pa ON u.ProgramaAcademico\_idProgramaAcademico = pa.idProgramaAcademico

&nbsp;       WHERE tu.TipodeUsuario = 'Estudiante' AND u.Estado = 1

&nbsp;       `)

&nbsp;       return rows

}



exports.findAllTeachers = async () => {

&nbsp;   const \[rows] = await pool.execute(`

&nbsp;       SELECT u.idUsuarios, u.Nombre, u.CorreoInstitucional, u.CorreoPersonal, 

&nbsp;              u.Celular, u.Telefono, u.Estado, u.Semestre, u.Modalidad,

&nbsp;              tu.TipodeUsuario, pa.Nombre as ProgramaAcademico

&nbsp;       FROM Usuarios u

&nbsp;       INNER JOIN TipoUsuarios tu ON u.TipoUsuarios\_idTipoUsuarios = tu.idTipoUsuarios

&nbsp;       LEFT JOIN ProgramaAcademico pa ON u.ProgramaAcademico\_idProgramaAcademico = pa.idProgramaAcademico

&nbsp;       WHERE tu.TipodeUsuario = 'Docente' AND u.Estado = 1

&nbsp;       `)

&nbsp;       return rows

}



exports.findAllAdmin = async () => {

&nbsp;   const \[rows] = await pool.execute(`

&nbsp;       SELECT u.idUsuarios, u.Nombre, u.CorreoInstitucional, u.CorreoPersonal, 

&nbsp;              u.Celular, u.Telefono, u.Estado, u.Semestre, u.Modalidad,

&nbsp;              tu.TipodeUsuario, pa.Nombre as ProgramaAcademico

&nbsp;       FROM Usuarios u

&nbsp;       INNER JOIN TipoUsuarios tu ON u.TipoUsuarios\_idTipoUsuarios = tu.idTipoUsuarios

&nbsp;       LEFT JOIN ProgramaAcademico pa ON u.ProgramaAcademico\_idProgramaAcademico = pa.idProgramaAcademico

&nbsp;       WHERE tu.TipodeUsuario = 'Administrativo' AND u.Estado = 1

&nbsp;       `)

&nbsp;       return rows

}





// Obtener usuario por ID

exports.findById = async (id) => {

&nbsp;   const \[rows] = await pool.execute(`

&nbsp;       SELECT u.idUsuarios, u.Nombre, u.CorreoInstitucional, u.CorreoPersonal,

&nbsp;              u.Celular, u.Telefono, u.Direcccion, u.Genero, u.EstadoCivil,

&nbsp;              u.FechaNacimiento, u.Semestre, u.Modalidad, u.Estado,

&nbsp;              tu.TipodeUsuario, pa.Nombre as ProgramaAcademico,

&nbsp;              cu.Nombre as CentroUniversitario, m.Nombre as Municipio,

&nbsp;              td.TipoDocumento, r.Nombre as Rol, tp.Nombre as TipoPoblacion

&nbsp;       FROM Usuarios u

&nbsp;       INNER JOIN TipoUsuarios tu ON u.TipoUsuarios\_idTipoUsuarios = tu.idTipoUsuarios

&nbsp;       LEFT JOIN ProgramaAcademico pa ON u.ProgramaAcademico\_idProgramaAcademico = pa.idProgramaAcademico

&nbsp;       LEFT JOIN CentroUniversitarios cu ON u.CentroUniversitarios\_idCentroUniversitarios = cu.idCentroUniversitarios

&nbsp;       LEFT JOIN Municipios m ON u.Municipios\_idMunicipio = m.idMunicipio

&nbsp;       LEFT JOIN TipoDocumentos td ON u.TipoDocumentos\_idTipoDocumento = td.idTipoDocumento

&nbsp;       LEFT JOIN Roles r ON u.Roles\_idRoles1 = r.idRoles

&nbsp;       LEFT JOIN TipoPoblacion tp ON u.TipoPoblacion\_idTipoPoblacion = tp.idTipoPoblacion

&nbsp;       WHERE u.idUsuarios = ? AND u.Estado = 1

&nbsp;   `, \[id])

&nbsp;   

&nbsp;   if (rows.length === 0) {

&nbsp;       throw new Error('Usuario no encontrado')

&nbsp;   }

&nbsp;   

&nbsp;   return rows\[0];

};



// Verificar si el correo ya existe

exports.emailExists = async (email) => {

&nbsp;   const \[rows] = await pool.execute(

&nbsp;       'SELECT idUsuarios FROM Usuarios WHERE CorreoInstitucional = ? AND Estado = 1',

&nbsp;       \[email]

&nbsp;   );

&nbsp;   return rows.length > 0;

};



// Crear nuevo estudiante

exports.create = async (newUser) => {

&nbsp;   // Verificar si el correo ya existe

&nbsp;   const emailExists = await exports.emailExists(newUser.CorreoInstitucional)

&nbsp;   if (emailExists) {

&nbsp;       throw new Error('El correo institucional ya está registrado')

&nbsp;   }



&nbsp;   // Obtener IDs de las tablas relacionadas

&nbsp;   const \[tipoUsuario] = await pool.execute(

&nbsp;       "SELECT idTipoUsuarios FROM TipoUsuarios WHERE TipodeUsuario = 'Estudiante' LIMIT 1"

&nbsp;   )

&nbsp;   const \[rol] = await pool.execute(

&nbsp;       "SELECT idRoles FROM Roles WHERE Nombre = 'Estudiante' LIMIT 1"

&nbsp;   )

&nbsp;   if (tipoUsuario.length === 0 || rol.length === 0) {

&nbsp;       throw new Error('Configuración de base de datos incompleta');

&nbsp;   }



&nbsp;   const fechaActual = new Date()

&nbsp;   const \[result] = await pool.execute(

&nbsp;       `INSERT INTO Usuarios (

&nbsp;           Nombre, CorreoInstitucional, CorreoPersonal, Celular, Telefono,

&nbsp;           Direcccion, Genero, EstadoCivil, FechaNacimiento, 

&nbsp;           Modulos\_idModulos, Municipios\_idMunicipio, ProgramaAcademico\_idProgramaAcademico, 

&nbsp;           Roles\_idRoles1, TipoDocumentos\_idTipoDocumento, TipoUsuarios\_idTipoUsuarios,

&nbsp;           ProgramaAcademico\_idProgramaAcademico1, CentroUniversitarios\_idCentroUniversitarios,

&nbsp;           Estado, Semestre, Modalidad, TipoPoblacion\_idTipoPoblacion,

&nbsp;           FechaCreacion, FechaActualizacion

&nbsp;       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

&nbsp;       `,

&nbsp;       \[

&nbsp;           newUser.Nombre,

&nbsp;           newUser.CorreoInstitucional,

&nbsp;           newUser.CorreoPersonal || '',

&nbsp;           newUser.Celular || '',

&nbsp;           newUser.Telefono || '',

&nbsp;           newUser.Direcccion || '',

&nbsp;           newUser.Genero || '',

&nbsp;           newUser.EstadoCivil || '',

&nbsp;           newUser.FechaNacimiento || fechaActual,

&nbsp;           newUser.Modulos\_idModulos || 1,

&nbsp;           newUser.Municipios\_idMunicipio || 1,

&nbsp;           newUser.ProgramaAcademico\_idProgramaAcademico || 1,

&nbsp;           rol\[0].idRoles,

&nbsp;           newUser.TipoDocumentos\_idTipoDocumento || 1,

&nbsp;           tipoUsuario\[0].idTipoUsuarios,

&nbsp;           newUser.ProgramaAcademico\_idProgramaAcademico1 || 1,

&nbsp;           newUser.CentroUniversitarios\_idCentroUniversitarios || 1,

&nbsp;           1,

&nbsp;           newUser.Semestre || '1',

&nbsp;           newUser.Modalidad || 'Presencial',

&nbsp;           newUser.TipoPoblacion\_idTipoPoblacion || 1,

&nbsp;           fechaActual,

&nbsp;           fechaActual

&nbsp;       ]

&nbsp;   );

&nbsp;   return { id: result.insertId, ...newUser };

};



// Actualizar usuario

exports.update = async (id, updatedUsers) => {

&nbsp;   await exports.findById(id)



&nbsp;   const \[result] = await pool.execute(

&nbsp;       `UPDATE Usuarios SET 

&nbsp;           Nombre = ?, CorreoPersonal = ?, Celular = ?, Telefono = ?,

&nbsp;           Direcccion = ?, Genero = ?, EstadoCivil = ?, FechaNacimiento = ?,

&nbsp;           Semestre = ?, Modalidad = ?, FechaActualizacion = ?,

&nbsp;           Municipios\_idMunicipio = ?, ProgramaAcademico\_idProgramaAcademico = ?,

&nbsp;           TipoDocumentos\_idTipoDocumento = ?, CentroUniversitarios\_idCentroUniversitarios = ?,

&nbsp;           TipoPoblacion\_idTipoPoblacion = ?

&nbsp;       WHERE idUsuarios = ? AND Estado = 1`,

&nbsp;       \[

&nbsp;           updatedUsers.Nombre,

&nbsp;           updatedUsers.CorreoPersonal,

&nbsp;           updatedUsers.Celular,

&nbsp;           updatedUsers.Telefono,

&nbsp;           updatedUsers.Direcccion,

&nbsp;           updatedUsers.Genero,

&nbsp;           updatedUsers.EstadoCivil,

&nbsp;           updatedUsers.FechaNacimiento,

&nbsp;           updatedUsers.Semestre,

&nbsp;           updatedUsers.Modalidad,

&nbsp;           new Date(),

&nbsp;           updatedUsers.Municipios\_idMunicipio,

&nbsp;           updatedUsers.ProgramaAcademico\_idProgramaAcademico,

&nbsp;           updatedUsers.TipoDocumentos\_idTipoDocumento,

&nbsp;           updatedUsers.CentroUniversitarios\_idCentroUniversitarios,

&nbsp;           updatedUsers.TipoPoblacion\_idTipoPoblacion,

&nbsp;           id

&nbsp;       ]

&nbsp;   )

&nbsp;   return result.affectedRows > 0;

}



// Eliminar usuario (soft delete)

exports.remove = async (id) => {

&nbsp;   const \[result] = await pool.execute(

&nbsp;       'UPDATE Usuarios SET Estado = 0, FechaActualizacion = ? WHERE idUsuarios = ?',

&nbsp;       \[new Date(), id]

&nbsp;   )

&nbsp;   return result.affectedRows > 0;

}



// Login de usuario

exports.login = async (email) => {

&nbsp;   const \[rows] = await pool.execute(`

&nbsp;       SELECT u.idUsuarios, u.Nombre, u.CorreoInstitucional, u.Estado 

&nbsp;       FROM Usuarios u 

&nbsp;       INNER JOIN TipoUsuarios tu ON u.TipoUsuarios\_idTipoUsuarios = tu.idTipoUsuarios 

&nbsp;       WHERE u.CorreoInstitucional = ? 

&nbsp;       AND u.Estado = 1 

&nbsp;   `, \[email])

&nbsp;   if (rows.length === 0) {

&nbsp;       throw new Error('Usuario no encontrado')

&nbsp;   }

&nbsp;   return rows\[0];

}



// Obtener emprendimientos del usuario

exports.getEntrepreneurships = async (userId) => {

&nbsp;   const \[modulo] = await pool.execute(

&nbsp;       'SELECT Modulos\_idModulos FROM Usuarios WHERE idUsuarios = ?', \[userId]

&nbsp;   )

&nbsp;   if (modulo.length === 0) return \[]

&nbsp;   const moduloId = modulo\[0].Modulos\_idModulos



&nbsp;   const \[rows] = await pool.execute(`

&nbsp;       SELECT e.idEmprendimiento, e.Nombre, e.Descripcion, e.TipoEmprendimiento,

&nbsp;              e.SectorProductivo, e.RedesSociales, e.Acompanamiento, e.FechaCreacion, e.FechaActualizacion,

&nbsp;              ee.TipoEtapa

&nbsp;       FROM Emprendimiento e

&nbsp;       INNER JOIN EtapadeEmpedimiento ee ON e.EtapadeEmpedimiento\_idEtapadeEmpedimiento = ee.idEtapadeEmpedimiento

&nbsp;       WHERE e.Modulos\_idModulos = ? 

&nbsp;   `, \[moduloId])

&nbsp;   return rows

};



// Obtener diagnósticos de un emprendimiento

exports.getDiagnostics = async (entrepreneurshipId) => {

&nbsp;   const \[rows] = await pool.execute(`

&nbsp;       SELECT d.idDiagnosticos, d.FechaEmprendimiento, d.AreaEstrategia, d.Diferencial,

&nbsp;              d.Planeacion, d.MercadoObjetivo, d.Tendencias, d.Canales, d.DescripcionPromocion,

&nbsp;              d.Presentacion, d.PasosElaboracion, d.SituacionFinanciera, d.FuenteFinanciero,

&nbsp;              d.EstructuraOrganica, d.ConocimientoLegal, d.MetodologiaInnovacion,

&nbsp;              d.HerramientaTecnologicas, d.Marca, d.AplicacionMetodologia,

&nbsp;              d.ImpactoAmbiental, d.ImpactoSocial, d.Viabilidad,

&nbsp;              se.Nombre as SectorEconomico

&nbsp;       FROM Diagnosticos d

&nbsp;       INNER JOIN SectoEconomico se ON d.SectoEconomico\_idSectoEconomico = se.idSectoEconomico

&nbsp;       WHERE d.Emprendimiento\_idEmprendimiento = ?

&nbsp;   `, \[entrepreneurshipId]);

&nbsp;   return rows;

};



// Obtener consultorías de un usuario

exports.getConsultancies = async (userId) => {

&nbsp;   const \[rows] = await pool.execute(`

&nbsp;       SELECT a.idAsesorias, a.Nombre\_de\_asesoria, a.Descripcion, a.Fecha\_asesoria,

&nbsp;              a.Comentarios, a.confimacion, a.Fecha\_creacion, a.Fecha\_actualizacion,

&nbsp;              m.Presencial, m.Distancia, m.Enlace\_virtual, m.Lugar,

&nbsp;              fyh.Fecha\_inicio, fyh.Hora\_inicio, fyh.Fecha\_fin, fyh.Hora\_fin

&nbsp;       FROM Asesorias a

&nbsp;       INNER JOIN Modalidad m ON a.Modalidad\_idModalidad = m.idModalidad

&nbsp;       INNER JOIN Fecha\_y\_Horarios fyh ON a.Fecha\_y\_Horarios\_idFecha\_y\_Horarios = fyh.idFecha\_y\_Horarios

&nbsp;       WHERE a.Usuarios\_idUsuarios = ?

&nbsp;   `, \[userId]);

&nbsp;   return rows;

};

```



```JavaScript

// user.controller.js



const usersService = require('../services/users.service')



// Obtener todos los estudiantes

exports.getAllUsers = async (req, res) => {

&nbsp;   try {

&nbsp;       const users = await usersService.findAll()

&nbsp;       res.json({ success: true, data: users })

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en getAllUsers:', error)

&nbsp;       res.status(500).json({ success: false, error: error.message })

&nbsp;   }

}



exports.getAllStudents = async (req, res) => {

&nbsp;   try {

&nbsp;       const students = await usersService.findAllStudents()

&nbsp;       res.json({ success: true, data: students })

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en getAllStudents:', error)

&nbsp;       res.status(500).json({ success: false, error: error.message })

&nbsp;   }

}



exports.getAllTeachers = async (req, res) => {

&nbsp;   try {

&nbsp;       const teachers = await usersService.findAllTeachers()

&nbsp;       res.json({ success: true, data: teachers })

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en getAllTeachers:', error)

&nbsp;       res.status(500).json({ success: false, error: error.message })

&nbsp;   }

}



exports.getAllAdmins = async (req, res) => {

&nbsp;   try {

&nbsp;       const admins = await usersService.findAllAdmin()

&nbsp;       res.json({ success: true, data: admins })

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en getAllAdmins:', error)

&nbsp;       res.status(500).json({ success: false, error: error.message })

&nbsp;   }

}



// Obtener usuario por ID

exports.getUsersById = async (req, res) => {

&nbsp;   try {

&nbsp;       const user = await usersService.findById(req.params.id)

&nbsp;       res.json({ success: true, data: user })

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en getStudentById:', error)

&nbsp;       res.status(404).json({ success: false, error: error.message })

&nbsp;   }

}



// Crear nuevo usuario

exports.createUser = async (req, res) => {

&nbsp;   try {

&nbsp;       const newUser = await usersService.create(req.body)

&nbsp;       res.status(201).json({ success: true, data: newUser })

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en createUsers:', error)

&nbsp;       res.status(400).json({ success: false, error: error.message })

&nbsp;   }

}



// Actualizar estudiante

exports.updateUser = async (req, res) => {

&nbsp;   try {

&nbsp;       const updated = await usersService.update(req.params.id, req.body);

&nbsp;       if (updated) {

&nbsp;           res.json({ success: true, message: 'Usuario actualizado correctamente' })

&nbsp;       } else {

&nbsp;           res.status(404).json({ success: false, error: 'Usuario no encontrado' })

&nbsp;       }

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en updateUsuario:', error)

&nbsp;       res.status(400).json({ success: false, error: error.message })

&nbsp;   }

}



// Eliminar usuario

exports.deleteUser = async (req, res) => {

&nbsp;   try {

&nbsp;       const deleted = await usersService.remove(req.params.id)

&nbsp;       if (deleted) {

&nbsp;           res.json({ success: true, message: 'Usuario eliminado correctamente' })

&nbsp;       } else {

&nbsp;           res.status(404).json({ success: false, error: 'Usuario no encontrado' })

&nbsp;       }

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en deleteUsuario:', error)

&nbsp;       res.status(500).json({ success: false, error: error.message })

&nbsp;   }

}



// Login de usuario

exports.loginUser = async (req, res) => {

&nbsp;   try {

&nbsp;       const { email } = req.body;

&nbsp;       if (!email) {

&nbsp;           return res.status(400).json({ success: false, error: 'Email es requerido' })

&nbsp;       }

&nbsp;       

&nbsp;       const user = await usersService.login(email)

&nbsp;       res.json({ success: true, data: user })

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en loginUser:', error)

&nbsp;       res.status(401).json({ success: false, error: error.message })

&nbsp;   }

}



// Obtener emprendimientos de estudiante

exports.getStudentEntrepreneurships = async (req, res) => {

&nbsp;   try {

&nbsp;       const entrepreneurships = await usersService.getEntrepreneurships(req.params.id)

&nbsp;       res.json({ success: true, data: entrepreneurships })

&nbsp;   } catch (error) {

&nbsp;       console.error('Error en getStudentEntrepreneurships:', error)

&nbsp;       res.status(500).json({ success: false, error: error.message })

&nbsp;   }

}



```



```JavaScript

// user.routes.js

const express = require('express')

const router = express.Router()

const userController = require('../controllers/user.controller')



// Rutas para estudiantes

router.get('/', userController.getAllUsers)

router.get('/students', userController.getAllStudents)

router.get('/teachers', userController.getAllTeachers)

router.get('/admins', userController.getAllAdmins)

router.get('/:id', userController.getUsersById)

router.post('/', userController.createUser)

router.put('/:id', userController.updateUser)

router.delete('/:id', userController.deleteUser)

router.post('/login', userController.loginUser)

router.get('/:id/entrepreneurships', userController.getStudentEntrepreneurships)



module.exports = router

```



