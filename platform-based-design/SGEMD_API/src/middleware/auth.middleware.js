// Middleware para autenticación y autorización
const jwt = require('jsonwebtoken');
const JWT_SECRET = 'segmed_jwt_secret_2025'; 

// Verificar que el token sea válido y no haya expirado
exports.authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    console.log('Auth header:', authHeader); // Debug log

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        console.log('No token provided or invalid format');
        return res.status(401).json({ 
            success: false, 
            error: 'Se requiere token de autenticación válido' 
        });
    }

    const token = authHeader.split(' ')[1];
    console.log('Token received:', token.substring(0, 20) + '...'); 

    try {
        const decodedToken = jwt.verify(token, JWT_SECRET);
        console.log('Token decoded successfully:', { 
            userId: decodedToken.id,
            role: decodedToken.role,
            exp: new Date(decodedToken.exp * 1000) 
        }); 

        req.user = decodedToken;
        next();
    } catch (err) {
        console.error('Token verification failed:', err.message);
        return res.status(403).json({ 
            success: false, 
            error: 'Token inválido o expirado' 
        });
    }
};

exports.isAdmin = (req, res, next) => {
    if (!req.user || req.user.role !== 'Administrativo') {
        return res.status(403).json({ 
            success: false, 
            error: 'Se requieren permisos de administrador' 
        });
    }
    next();
};

exports.isTeacher = (req, res, next) => {
    if (!req.user || req.user.role !== 'Docente') {
        return res.status(403).json({ 
            success: false, 
            error: 'Se requieren permisos de docente' 
        });
    }
    next();
};

exports.isStudent = (req, res, next) => {
    if (!req.user || req.user.role !== 'Estudiante') {
        return res.status(403).json({ 
            success: false, 
            error: 'Se requieren permisos de estudiante' 
        });
    }
    next();
};