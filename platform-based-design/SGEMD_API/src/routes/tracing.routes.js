const express = require('express')
const router = express.Router()
const tracing = require('../controllers/tracing.controller')

router.get('/', tracing.getAll)
router.get('/:id', tracing.getById)
router.post('/', tracing.create)
router.put('/:id', tracing.update)
router.delete('/:id', tracing.remove)

module.exports = router