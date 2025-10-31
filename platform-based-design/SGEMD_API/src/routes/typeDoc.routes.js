const express = require('express')
const router = express.Router()
const tipoDocController = require('../controllers/typeDoc.controller')

router.get('/', tipoDocController.getAll)
router.get('/:id', tipoDocController.getById)
router.post('/', tipoDocController.create)
router.put('/:id', tipoDocController.update)
router.delete('/:id', tipoDocController.remove)

module.exports = router