const tipoUsuario = require('../services/typeUsers.service');

exports.getAll = async (req, res) => {
    try {
        const data = await tipoUsuario.findAll()
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
}

exports.getById = async (req, res) => {
    try {
        const data = await tipoUsuario.findById(req.params.id)
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(404).json({ success: false, error: error.message })
    }
}

exports.create = async (req, res) => {
    try {
        const data = await tipoUsuario.create(req.body)
        res.status(201).json({ success: true, data: data })
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.update = async (req, res) => {
    try {
        const updated = await tipoUsuario.update(req.params.id, req.body)
        if (updated) {
            res.json({ success: true, message: 'Tipo de Usuario actualizado' })
        } else {
            res.status(404).json({ success: false, error: 'Tipo de Usuario no encontrado' })
        }
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.remove = async (req, res) => {
    try {
        const deleted = await tipoUsuario.remove(req.params.id)
        if (deleted) {
            res.json({ success: true, message: 'Tipo de usuario eliminado' })
        } else {
            res.status(404).json({ success: false, error: 'Tipo de Usuario no encontrado' })
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
};