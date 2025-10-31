const express = require('express')
const router = express.Router()
const advice = require('../controllers/advice.controller')

router.get('/', advice.getAll)
router.get('/:id', advice.getById)
router.post('/', advice.create)
router.put('/:id', advice.update)
router.delete('/:id', advice.remove)

module.exports = router