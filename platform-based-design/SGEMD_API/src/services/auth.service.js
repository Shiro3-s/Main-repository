const { pool } = require('../config/db.config');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const JWT_SECRET = 'segmed_jwt_secret_2025'; // Cambiar en producción

exports.login = async (email, password) => {
    console.log('Auth attempt:', { email });

    try {
        // 1. Buscar usuario
        const [rows] = await pool.execute(`
            SELECT u.idUsuarios, u.Nombre, u.CorreoInstitucional, u.Password, u.Estado,
                   r.Nombre as Rol, tu.TipodeUsuario
            FROM Usuarios u
            INNER JOIN TipoUsuarios tu ON u.TipoUsuarios_idTipoUsuarios = tu.idTipoUsuarios
            INNER JOIN Roles r ON u.Roles_idRoles1 = r.idRoles
            WHERE u.CorreoInstitucional = ? AND u.Estado = 1
        `, [email]);

        if (rows.length === 0) {
            throw new Error('Usuario no encontrado');
        }

        const user = rows[0];

        // 2. Verificar contraseña
        const isPasswordValid = await bcrypt.compare(password, user.Password);
        if (!isPasswordValid) {
            throw new Error('Contraseña incorrecta');
        }

        // 3. Generar token
        const token = jwt.sign(
            { 
                id: user.idUsuarios,
                email: user.CorreoInstitucional,
                role: user.Rol,
                userType: user.TipodeUsuario
            },
            JWT_SECRET,
            { expiresIn: '24h' }
        );

        // 4. Retornar respuesta
        const { Password, ...userWithoutPassword } = user;
        return {
            user: userWithoutPassword,
            token
        };
    } catch (error) {
        console.error('Auth service error:', error);
        throw error;
    }
};

exports.register = async (userData) => {
    console.log('Register attempt:', { email: userData.CorreoInstitucional });

    try {
        // 1. Verificar si el usuario ya existe
        const [existing] = await pool.execute(
            'SELECT idUsuarios FROM Usuarios WHERE CorreoInstitucional = ?',
            [userData.CorreoInstitucional]
        );

        if (existing.length > 0) {
            throw new Error('El correo ya está registrado');
        }

        // 2. Hashear contraseña
        const hashedPassword = await bcrypt.hash(userData.Password, 10);

        // 3. Obtener IDs necesarios
        const [[tipoUsuario]] = await pool.execute(
            "SELECT idTipoUsuarios FROM TipoUsuarios WHERE TipodeUsuario = 'Estudiante' LIMIT 1"
        );
        const [[rol]] = await pool.execute(
            "SELECT idRoles FROM Roles WHERE Nombre = 'Estudiante' LIMIT 1"
        );

        // 4. Insertar usuario
        const [result] = await pool.execute(
            `INSERT INTO Usuarios (
                Nombre, CorreoInstitucional, Password, CorreoPersonal,
                Celular, Telefono, Direccion, Genero, EstadoCivil,
                FechaNacimiento, TipoUsuarios_idTipoUsuarios, Roles_idRoles1,
                Estado, Semestre, Modalidad, FechaCreacion, FechaActualizacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), NOW())`,
            [
                userData.Nombre,
                userData.CorreoInstitucional,
                hashedPassword,
                userData.CorreoPersonal || '',
                userData.Celular || '',
                userData.Telefono || '',
                userData.Direccion || '',
                userData.Genero || '',
                userData.EstadoCivil || '',
                userData.FechaNacimiento || new Date(),
                tipoUsuario.idTipoUsuarios,
                rol.idRoles,
                1,
                userData.Semestre || '1',
                userData.Modalidad || 'Presencial'
            ]
        );

        return {
            id: result.insertId,
            ...userData,
            Password: undefined
        };
    } catch (error) {
        console.error('Register service error:', error);
        throw error;
    }
};