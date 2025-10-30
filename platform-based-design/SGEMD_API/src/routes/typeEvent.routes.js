const express = require('express')
const router = express.Router()
const tipoEvento = require('../controllers/typeEvent.controller')

router.get('/', tipoEvento.getAll)
router.get('/:id', tipoEvento.getById)
router.post('/', tipoEvento.create)
router.put('/:id', tipoEvento.update)
router.delete('/:id', tipoEvento.remove)

module.exports = router