const express = require('express')
const router = express.Router()
const diagnostico = require('../controllers/diagnosis.controller')

router.get('/', diagnostico.getAll)
router.get('/:id', diagnostico.getById)
router.post('/', diagnostico.create)
router.put('/:id', diagnostico.update)
router.delete('/:id', diagnostico.remove)

module.exports = router