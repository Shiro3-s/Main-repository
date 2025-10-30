const express = require('express')
const router = express.Router()
const tipoPoblacionController = require('../controllers/typePop.controller')

router.get('/', tipoPoblacionController.getAll)
router.get('/:id', tipoPoblacionController.getById)
router.post('/', tipoPoblacionController.create)
router.put('/:id', tipoPoblacionController.update)
router.delete('/:id', tipoPoblacionController.remove)

module.exports = router