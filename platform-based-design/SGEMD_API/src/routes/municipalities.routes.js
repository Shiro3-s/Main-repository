const express = require('express')
const router = express.Router()
const municipiosController = require('../controllers/municipalities.controller')

router.get('/', municipiosController.getAll)
router.get('/:id', municipiosController.getById)
router.post('/', municipiosController.create)
router.put('/:id', municipiosController.update)
router.delete('/:id', municipiosController.remove)

module.exports = router