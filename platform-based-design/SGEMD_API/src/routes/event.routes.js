const express = require('express')
const router = express.Router()
const event = require('../controllers/event.controller')

router.get('/', event.getAll)
router.get('/:id', event.getById)
router.post('/', event.create)
router.put('/:id', event.update)
router.delete('/:id', event.remove)

module.exports = router