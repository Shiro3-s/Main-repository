const express = require('express');
const router = express.Router();
const userController = require('../controllers/user.controllers');

router.get('/', userController.findAll);
router.get('/:id', userController.findById);
router.post('/:id', userController.create);
router.put('/:id', userController.update);
router.delete('/:id', userController.remove);

module.exports = router;