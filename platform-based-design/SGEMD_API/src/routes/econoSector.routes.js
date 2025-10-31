const express = require('express')
const router = express.Router()
const sectorEconomico = require('../controllers/econoSector.controller')

router.get('/', sectorEconomico.getAll)
router.get('/:id', sectorEconomico.getById)
router.post('/', sectorEconomico.create)
router.put('/:id', sectorEconomico.update)
router.delete('/:id', sectorEconomico.remove)

module.exports = router