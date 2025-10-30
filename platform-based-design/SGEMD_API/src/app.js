//Dependencias principales
require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { testConnection } = require('./config/db.config');
/*
    El endpoint de register esta en el node, si se quiere registrar un nuevo usuario se sigue el siguiente endpoint:
    http://localhost:3005/sgmed/users/register

    realizas la siguiente estructura en el body:

    {
      "Nombre": "Carlos Pérez",
      "CorreoInstitucional": "monocho29@gmail.com",
      "CorreoPersonal": "monocho29@gmail.com",
      "Password": "abcdef123",
      "Celular": "3198765432",
      "Telefono": "6011122233",
      "Direccion": "Carrera 23 #45-67",
      "Genero": "Masculino",
      "EstadoCivil": "Soltero",
      "FechaNacimiento": "1998-07-22",
      "ProgramaAcademico_idProgramaAcademico1": 2,
      "CentroUniversitarios_idCentroUniversitarios": 1,
      "Estado": 1,
      "Semestre": "3",
      "Modalidad": "Virtual",
      "Roles_idRoles1": 2,
      "FechaCreacion": "2025-10-28",
      "FechaActualizacion": "2025-10-28"
    }
*/

//Importar rutas
const userRoutes = require('./routes/user.routes');
const moduleRoutes = require('./routes/module.routes');
const municipalitiesRoutes = require('./routes/municipalities.routes');
const academicProgramRoutes = require('./routes/academicProgram.routes');
const roles = require('./routes/roles.routes');
const tipoDoc = require('./routes/typeDoc.routes');
const tipoUsuario = require('./routes/typeUsers.routes');
const uniCenters = require('./routes/uniCenters.routes');
const tipoPoblacion = require('./routes/typePop.routes');
const EtapadeEmprendimiento = require('./routes/entrepStage.routes');
const emprendimiento = require('./routes/entrepreneurship.routes');
const tracing = require('./routes/tracing.routes');
const assistance = require('./routes/assistance.routes');
const econoSector = require('./routes/econoSector.routes');
const diagnosis = require('./routes/diagnosis.routes');
const mode = require('./routes/mode.routes');
const advice = require('./routes/advice.routes');
const event = require('./routes/event.routes');
const typeEvent = require('./routes/typeEvent.routes');
const dateTimes = require('./routes/dateTimes.routes');
const authRoutes = require('./routes/auth.routes');

// Configuración base de la app
const app = express();
const PORT = process.env.PORT || 3005;

// Middleware global
app.use(cors({
  origin: "http://localhost:3000",
  credentials: true
}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Rutas del sistema
app.use('/sgmed/auth', authRoutes);
app.use('/sgmed/users', userRoutes);
app.use('/sgmed/module', moduleRoutes);
app.use('/sgmed/municipalities', municipalitiesRoutes);
app.use('/sgmed/academic-programs', academicProgramRoutes);
app.use('/sgmed/roles', roles);
app.use('/sgmed/type-doc', tipoDoc);
app.use('/sgmed/type-users', tipoUsuario);
app.use('/sgmed/uni-centers', uniCenters);
app.use('/sgmed/type-pop', tipoPoblacion);
app.use('/sgmed/entrep-stage', EtapadeEmprendimiento);
app.use('/sgmed/entrepreneurship', emprendimiento);
app.use('/sgmed/tracing', tracing);
app.use('/sgmed/assistance', assistance);
app.use('/sgmed/econo-sector', econoSector);
app.use('/sgmed/diagnosis', diagnosis);
app.use('/sgmed/mode', mode);
app.use('/sgmed/advice', advice);
app.use('/sgmed/event', event);
app.use('/sgmed/type-event', typeEvent);
app.use('/sgmed/date-times', dateTimes);

// Ruta base de prueba
app.get('/', (req, res) => {
  res.json({
    message: 'Bienvenido al API de SGEMD 🚀',
    endpoints: {
      auth: '/sgmed/auth/login',
      users: '/sgmed/users',
      modules: '/sgmed/module',
      municipalities: '/sgmed/municipalities',
      academicPrograms: '/sgmed/academic-programs',
      roles: '/sgmed/roles',
      tipoDoc: '/sgmed/type-doc',
      tipoUsuario: '/sgmed/type-users',
      uniCenters: '/sgmed/uni-centers',
      tipoPoblacion: '/sgmed/type-pop',
      etapadeEmpedimiento: '/sgmed/entrep-stage',
      emprendimiento: '/sgmed/entrepreneurship',
      tracing: '/sgmed/tracing',
      assistance: '/sgmed/assistance',
      econoSector: '/sgmed/econo-sector',
      diagnosis: '/sgmed/diagnosis',
      mode: '/sgmed/mode',
      advice: '/sgmed/advice',
      event: '/sgmed/event',
      typeEvent: '/sgmed/type-event',
      dateTimes: '/sgmed/date-times'
    }
  });
});

// Manejo de errores global
app.use((err, req, res, next) => {
  console.error('🔥 Error interno:', err.stack);
  res.status(500).json({ success: false, error: 'Error interno del servidor' });
});

// Rutas no encontradas
app.use('*', (req, res) => {
  res.status(404).json({ success: false, error: 'Ruta no encontrada' });
});

// Inicializar servidor
async function startServer() {
  const dbConnected = await testConnection();
  if (!dbConnected) {
    console.error('No se pudo conectar a la base de datos.');
    process.exit(1);
  }

  app.listen(PORT, () => {
    console.log(`Servidor ejecutándose en: http://localhost:${PORT}`);
    console.log(`API disponible en: http://localhost:${PORT}/sgmed/`);
  });
}
// Iniciar el servidor
startServer();
