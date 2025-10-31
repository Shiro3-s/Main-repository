const express = require('express')
const router = express.Router()
const dateTimes = require('../controllers/dateTimes.controller')

router.get('/', dateTimes.getAll)
router.get('/:id', dateTimes.getById)
router.post('/', dateTimes.create)
router.put('/:id', dateTimes.update)
router.delete('/:id', dateTimes.remove)

module.exports = router