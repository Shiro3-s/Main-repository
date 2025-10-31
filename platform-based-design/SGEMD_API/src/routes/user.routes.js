// Rutas para la gestión de usuarios
const express = require('express')
const router = express.Router()
const usersController = require('../controllers/user.controller') 
const { authenticateToken, isAdmin } = require('../middleware/auth.middleware')

//RUTAS PÚBLICAS
router.post('/login', usersController.loginUser)
router.post('/register', usersController.createUser)

//RUTAS PROTEGIDAS 
router.get('/', authenticateToken, usersController.getAllUsers)
router.get('/students', authenticateToken, usersController.getAllStudents)
router.get('/teachers', authenticateToken, usersController.getAllTeachers)
router.get('/admins', authenticateToken, isAdmin, usersController.getAllAdmins)

// RUTAS DINÁMICAS (por ID) 
router.get('/:id', authenticateToken, usersController.getUsersById)
router.put('/:id', authenticateToken, usersController.updateUser)
router.delete('/:id', authenticateToken, isAdmin, usersController.deleteUser)

//EMPRENDIMIENTOS DE ESTUDIANTE
router.get('/:id/entrepreneurships', authenticateToken, usersController.getStudentEntrepreneurships)

module.exports = router
