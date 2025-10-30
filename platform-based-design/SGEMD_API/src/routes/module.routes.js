const express = require('express')
const router = express.Router()
const modulosController = require('../controllers/modules.controller')

router.get('/', modulosController.getAll)
router.get('/:id', modulosController.getById)
router.post('/', modulosController.create)
router.put('/:id', modulosController.update)
router.delete('/:id', modulosController.remove)

module.exports = router