// Controlador de autenticación
const bcrypt = require('bcryptjs');
const conexion = require('../config/db.config');
const transporter = require('../config/email'); 

// Función para enviar el correo al iniciar sesión
async function enviarCorreoInicioSesion(email, nombre) {
  try {
    await transporter.sendMail({
      from: `"Sistema SGEMD" <${process.env.EMAIL_USER}>`,
      to: email,
      subject: 'Inicio de sesión detectado',
      text: `Hola ${nombre}, acabas de ingresar a tu cuenta en SGEMD.`,
    });
    console.log(`Correo de inicio de sesión enviado a ${email}`);
  } catch (error) {
    console.error('Error al enviar correo:', error);
  }
}

// Controlador del login
exports.login = (req, res) => {
  const { usuario, clave } = req.body;

  if (!usuario || !clave) {
    return res.status(400).send('Por favor ingrese usuario y contraseña');
  }

  const sql = 'SELECT * FROM usuarios WHERE usuario = ?';
  conexion.query(sql, [usuario], async (err, results) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Error interno del servidor');
    }

    if (results.length === 0) {
      return res.status(401).send('Usuario no encontrado');
    }

    const usuarioData = results[0];
    const esValido = await bcrypt.compare(clave, usuarioData.clave);

    if (!esValido) {
      return res.status(401).send('Contraseña incorrecta');
    }

    enviarCorreoInicioSesion(usuarioData.correo, usuarioData.nombre);

    res.status(200).json({
      success: true,
      message: `Bienvenido, ${usuarioData.nombre}`,
      usuario: {
        id: usuarioData.id_usuario,
        nombre: usuarioData.nombre,
        rol: usuarioData.rol,
        correo: usuarioData.correo
      }
    });
  });
};
