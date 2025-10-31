const uniCenter = require('../services/uniCenters.service');

exports.getAll = async (req, res) => {
    try {
        const data = await uniCenter.findAll()
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
}

exports.getById = async (req, res) => {
    try {
        const data = await uniCenter.findById(req.params.id)
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(404).json({ success: false, error: error.message })
    }
}

exports.create = async (req, res) => {
    try {
        const data = await uniCenter.create(req.body)
        res.status(201).json({ success: true, data: data })
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.update = async (req, res) => {
    try {
        const updated = await uniCenter.update(req.params.id, req.body)
        if (updated) {
            res.json({ success: true, message: 'Centro Universitario actualizado' })
        } else {
            res.status(404).json({ success: false, error: 'Centro Universitario no encontrado' })
        }
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.remove = async (req, res) => {
    try {
        const deleted = await uniCenter.remove(req.params.id)
        if (deleted) {
            res.json({ success: true, message: 'Centro Universitario eliminado' })
        } else {
            res.status(404).json({ success: false, error: 'Centro Universitario no encontrado' })
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
};