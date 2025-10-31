const asesoria = require('../services/advice.service');

exports.getAll = async (req, res) => {
    try {
        const data = await asesoria.findAll()
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
}

exports.getById = async (req, res) => {
    try {
        const data = await asesoria.findById(req.params.id)
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(404).json({ success: false, error: error.message })
    }
}

exports.create = async (req, res) => {
    try {
        const data = await asesoria.create(req.body)
        res.status(201).json({ success: true, data: data })
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.update = async (req, res) => {
    try {
        const updated = await asesoria.update(req.params.id, req.body)
        if (updated) {
            res.json({ success: true, message: 'Asesoria actualizado' })
        } else {
            res.status(404).json({ success: false, error: 'Asesoria no encontrado' })
        }
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.remove = async (req, res) => {
    try {
        const deleted = await asesoria.remove(req.params.id)
        if (deleted) {
            res.json({ success: true, message: 'Asesoria eliminado' })
        } else {
            res.status(404).json({ success: false, error: 'Asesoria no encontrado' })
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
};