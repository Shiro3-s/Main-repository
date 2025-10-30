const express = require('express')
const router = express.Router()
const asistencia = require('../controllers/assistance.controller')

router.get('/', asistencia.getAll)
router.get('/:id', asistencia.getById)
router.post('/', asistencia.create)
router.put('/:id', asistencia.update)
router.delete('/:id', asistencia.remove)

module.exports = router