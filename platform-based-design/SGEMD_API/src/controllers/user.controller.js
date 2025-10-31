// Controlador para la gestión de usuarios
const usersService = require('../services/users.service');
const { enviarCorreoLogin } = require('../config/mailer.js');

//  Obtener todos los usuarios
exports.getAllUsers = async (req, res) => {
    try {
        const users = await usersService.findAll();
        res.json({ success: true, data: users });
    } catch (error) {
        console.error('Error en getAllUsers:', error);
        res.status(500).json({ success: false, error: error.message });
    }
};

// Obtener todos los estudiantes
exports.getAllStudents = async (req, res) => {
    try {
        const students = await usersService.findAllStudents();
        res.json({ success: true, data: students });
    } catch (error) {
        console.error('Error en getAllStudents:', error);
        res.status(500).json({ success: false, error: error.message });
    }
};

// Obtener todos los profesores
exports.getAllTeachers = async (req, res) => {
    try {
        const teachers = await usersService.findAllTeachers();
        res.json({ success: true, data: teachers });
    } catch (error) {
        console.error('Error en getAllTeachers:', error);
        res.status(500).json({ success: false, error: error.message });
    }
};

// Obtener todos los administradores
exports.getAllAdmins = async (req, res) => {
    try {
        const admins = await usersService.findAllAdmin();
        res.json({ success: true, data: admins });
    } catch (error) {
        console.error('Error en getAllAdmins:', error);
        res.status(500).json({ success: false, error: error.message });
    }
};

// Obtener usuario por ID
exports.getUsersById = async (req, res) => {
    try {
        const user = await usersService.findById(req.params.id);
        res.json({ success: true, data: user });
    } catch (error) {
        console.error('Error en getUsersById:', error);
        res.status(404).json({ success: false, error: error.message });
    }
};

// Crear nuevo usuario (registro)
exports.createUser = async (req, res) => {
    try {
        console.log('Body recibido en createUser:', req.body);
        const newUser = await usersService.create(req.body);
        res.status(201).json({ success: true, data: newUser });
    } catch (error) {
        console.error('Error en createUser:', error);
        res.status(400).json({ success: false, error: error.message });
    }
};

// Actualizar usuario
exports.updateUser = async (req, res) => {
    try {
        const updated = await usersService.update(req.params.id, req.body);
        if (updated) {
            res.json({ success: true, message: 'Usuario actualizado correctamente' });
        } else {
            res.status(404).json({ success: false, error: 'Usuario no encontrado' });
        }
    } catch (error) {
        console.error('Error en updateUser:', error);
        res.status(400).json({ success: false, error: error.message });
    }
};

// Eliminar usuario
exports.deleteUser = async (req, res) => {
    try {
        const deleted = await usersService.remove(req.params.id);
        if (deleted) {
            res.json({ success: true, message: 'Usuario eliminado correctamente' });
        } else {
            res.status(404).json({ success: false, error: 'Usuario no encontrado' });
        }
    } catch (error) {
        console.error('Error en deleteUser:', error);
        res.status(500).json({ success: false, error: error.message });
    }
};

// Login de usuario
exports.loginUser = async (req, res) => {
  const { CorreoInstitucional, Password } = req.body;
  console.log('Login attempt:', { CorreoInstitucional });

  if (!CorreoInstitucional || !Password) {
    return res.status(400).json({ success: false, error: 'El correo y la contraseña son requeridos' });
  }

  try {
    const result = await usersService.login(CorreoInstitucional, Password);

    if (!result.user) {
      return res.status(401).json({ success: false, error: 'Credenciales inválidas' });
    }

    console.log('Login exitoso:', { userId: result.user.idUsuarios });

    const contenido = `
      <h3>Inicio de sesión en sgemd</h3>
      <p>Hola ${result.user.Nombre},</p>
      <p>Se detectó un inicio de sesión en tu cuenta.</p>
      <p><strong>Correo:</strong> ${result.user.CorreoInstitucional}</p>
      <p>Si no fuiste tú, cambia tu contraseña inmediatamente.</p>
    `;
    enviarCorreoLogin(result.user.CorreoInstitucional, 'Inicio de sesión en sgemd', contenido)
      .then(() => console.log('Correo de login enviado correctamente'))
      .catch(err => console.error('Error enviando correo de login:', err));
    res.json({ success: true, message: 'Login exitoso', data: result });

  } catch (error) {
    console.error('Error en loginUser:', error);

    if (error.message === 'Usuario no encontrado' || error.message === 'Contraseña incorrecta') {
      return res.status(401).json({ success: false, error: 'Credenciales inválidas' });
    }

    res.status(500).json({ success: false, error: 'Error interno del servidor' });
  }
};

// Obtener emprendimientos del estudiante
exports.getStudentEntrepreneurships = async (req, res) => {
    try {
        const entrepreneurships = await usersService.getEntrepreneurships(req.params.id);
        res.json({ success: true, data: entrepreneurships });
    } catch (error) {
        console.error('Error en getStudentEntrepreneurships:', error);
        res.status(500).json({ success: false, error: error.message });
    }
};
