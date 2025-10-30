const express = require('express')
const router = express.Router()
const uniCenterController = require('../controllers/uniCenters.controller')

router.get('/', uniCenterController.getAll)
router.get('/:id', uniCenterController.getById)
router.post('/', uniCenterController.create)
router.put('/:id', uniCenterController.update)
router.delete('/:id', uniCenterController.remove)

module.exports = router