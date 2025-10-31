const sectorEconomico = require('../services/econoSector.service');

exports.getAll = async (req, res) => {
    try {
        const data = await sectorEconomico.findAll()
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
}

exports.getById = async (req, res) => {
    try {
        const data = await sectorEconomico.findById(req.params.id)
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(404).json({ success: false, error: error.message })
    }
}

exports.create = async (req, res) => {
    try {
        const data = await sectorEconomico.create(req.body)
        res.status(201).json({ success: true, data: data })
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.update = async (req, res) => {
    try {
        const updated = await sectorEconomico.update(req.params.id, req.body)
        if (updated) {
            res.json({ success: true, message: 'Sector Economico actualizado' })
        } else {
            res.status(404).json({ success: false, error: 'Sector Economico no encontrado' })
        }
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.remove = async (req, res) => {
    try {
        const deleted = await sectorEconomico.remove(req.params.id)
        if (deleted) {
            res.json({ success: true, message: 'Sector Economico eliminado' })
        } else {
            res.status(404).json({ success: false, error: 'Sector Economico no encontrado' })
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
};