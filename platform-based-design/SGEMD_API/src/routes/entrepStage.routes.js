const express = require('express')
const router = express.Router()
const etapaEmprendimientoController = require('../controllers/entrepStage.controller')

router.get('/', etapaEmprendimientoController.getAll)
router.get('/:id', etapaEmprendimientoController.getById)
router.post('/', etapaEmprendimientoController.create)
router.put('/:id', etapaEmprendimientoController.update)
router.delete('/:id', etapaEmprendimientoController.remove)

module.exports = router