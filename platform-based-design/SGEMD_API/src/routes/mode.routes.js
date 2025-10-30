const express = require('express')
const router = express.Router()
const mode = require('../controllers/mode.controller')

router.get('/', mode.getAll)
router.get('/:id', mode.getById)
router.post('/', mode.create)
router.put('/:id', mode.update)
router.delete('/:id', mode.remove)

module.exports = router