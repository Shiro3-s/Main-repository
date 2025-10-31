const express = require('express')
const router = express.Router()
const academicProgram = require('../controllers/academicProgram.controller')

router.get('/', academicProgram.getAll)
router.get('/:id', academicProgram.getById)
router.post('/', academicProgram.create)
router.put('/:id', academicProgram.update)
router.delete('/:id', academicProgram.remove)

module.exports = router