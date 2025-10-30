const dateTimes = require('../services/dateTimes.service');

exports.getAll = async (req, res) => {
    try {
        const data = await dateTimes.findAll()
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
}

exports.getById = async (req, res) => {
    try {
        const data = await dateTimes.findById(req.params.id)
        res.json({ success: true, data: data })
    } catch (error) {
        res.status(404).json({ success: false, error: error.message })
    }
}

exports.create = async (req, res) => {
    try {
        const data = await dateTimes.create(req.body)
        res.status(201).json({ success: true, data: data })
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.update = async (req, res) => {
    try {
        const updated = await dateTimes.update(req.params.id, req.body)
        if (updated) {
            res.json({ success: true, message: 'Fecha y horario actualizado' })
        } else {
            res.status(404).json({ success: false, error: 'Fecha y horario no encontrado' })
        }
    } catch (error) {
        res.status(400).json({ success: false, error: error.message })
    }
}

exports.remove = async (req, res) => {
    try {
        const deleted = await dateTimes.remove(req.params.id)
        if (deleted) {
            res.json({ success: true, message: 'Fecha y horario eliminado' })
        } else {
            res.status(404).json({ success: false, error: 'Fecha y horario no encontrado' })
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message })
    }
};