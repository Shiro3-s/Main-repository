const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    host: process.env.EMAIL_HOST,
    port: parseInt(process.env.EMAIL_PORT),
    secure: process.env.EMAIL_SECURE === 'true', // false para 587
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
    }
});

exports.sendLoginEmail = async (toEmail, userName) => {
    await transporter.sendMail({
        from: `"SGEMD" <${process.env.EMAIL_USER}>`,
        to: toEmail,
        subject: 'Inicio de sesión exitoso',
        text: `Hola ${userName},\n\nHas iniciado sesión correctamente en SGEMD.`
    });
};
