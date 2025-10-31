// Configuración del servicio de correo utilizando nodemailer y Gmail
const nodemailer = require("nodemailer");
require("dotenv").config();

const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS,
  },
});

async function enviarCorreoLogin(destinatario, asunto, contenidoHTML) {
  try {
    const info = await transporter.sendMail({
      from: `"Soporte sgemd" <${process.env.EMAIL_USER}>`,
      to: destinatario,
      subject: asunto,
      html: contenidoHTML,
    });
    console.log("Correo enviado:", info.messageId);
  } catch (error) {
    console.error("Error enviando correo:", error);
  }
}


module.exports = { enviarCorreoLogin };

