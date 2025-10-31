const tipoPoblacion = require('../services/typePop.service');

exports.getAll = async (req, res) => {
    try {
        const data = await tipoPoblacion.findAll()
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
}

exports.getById = async (req, res) => {
    try {
        const data = await tipoPoblacion.findById(req.params.id)
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(404).json({ success: false, error: error.message })
    }
}

exports.create = async (req, res) => {
    try {
        const data = await tipoPoblacion.create(req.body)
        res.status(201).json({ success: true, data: data })
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.update = async (req, res) => {
    try {
        const updated = await tipoPoblacion.update(req.params.id, req.body)
        if (updated) {
            res.json({ success: true, message: 'Tipo de poblacion actualizado' })
        } else {
            res.status(404).json({ success: false, error: 'Tipo de poblacion no encontrado' })
        }
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.remove = async (req, res) => {
    try {
        const deleted = await tipoPoblacion.remove(req.params.id)
        if (deleted) {
            res.json({ success: true, message: 'Tipo de poblacion eliminado' })
        } else {
            res.status(404).json({ success: false, error: 'Tipo de poblacion no encontrado' })
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
};