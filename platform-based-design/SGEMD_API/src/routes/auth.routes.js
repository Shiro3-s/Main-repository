// routes/auth.routes.js
const express = require('express');
const router = express.Router();
const { pool } = require('../config/db.config');
const nodemailer = require('nodemailer');

router.post('/login', async (req, res) => {
  const { usuario, clave } = req.body;

  try {

    const [rows] = await pool.query('SELECT * FROM usuarios WHERE CorreoPersonal = ? AND Password = ?',[usuario, clave]);

    if (rows.length === 0) {
      return res.status(401).json({ success: false, message: 'Credenciales inválidas' });
    }

    const user = rows[0];

    // 📧 Enviar correo al usuario
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.EMAIL_USER, // tu correo
        pass: process.env.EMAIL_PASS, // tu contraseña o app password
      },
    });

    await transporter.sendMail({
      from: `"SGEMED" <${process.env.EMAIL_USER}>`,
      to: user.correo,
      subject: 'Inicio de sesión detectado',
      text: `Hola ${user.nombre}, acabas de iniciar sesión en SGEMED.`,
    });

    res.json({ success: true, message: 'Login exitoso, correo enviado', user });
  } catch (error) {
    console.error('Error en login:', error);
    res.status(500).json({ success: false, message: 'Error interno del servidor' });
  }
});

module.exports = router;
