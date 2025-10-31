const etapaEmprendimiento = require('../services/mode.service');

exports.getAll = async (req, res) => {
    try {
        const data = await etapaEmprendimiento.findAll()
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
}

exports.getById = async (req, res) => {
    try {
        const data = await etapaEmprendimiento.findById(req.params.id)
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(404).json({ success: false, error: error.message })
    }
}

exports.create = async (req, res) => {
    try {
        const data = await etapaEmprendimiento.create(req.body)
        res.status(201).json({ success: true, data: data })
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.update = async (req, res) => {
    try {
        const updated = await etapaEmprendimiento.update(req.params.id, req.body)
        if (updated) {
            res.json({ success: true, message: 'Modalidad actualizado' })
        } else {
            res.status(404).json({ success: false, error: 'Modalidad no encontrado' })
        }
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.remove = async (req, res) => {
    try {
        const deleted = await etapaEmprendimiento.remove(req.params.id)
        if (deleted) {
            res.json({ success: true, message: 'Modalidad eliminado' })
        } else {
            res.status(404).json({ success: false, error: 'Modalidad no encontrado' })
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
};