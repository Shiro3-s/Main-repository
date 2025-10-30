const express = require('express')
const router = express.Router()
const emprendimiento = require('../controllers/entrepreneurship.controller')

router.get('/', emprendimiento.getAll)
router.get('/:id', emprendimiento.getById)
router.post('/', emprendimiento.create)
router.put('/:id', emprendimiento.update)
router.delete('/:id', emprendimiento.remove)

module.exports = router