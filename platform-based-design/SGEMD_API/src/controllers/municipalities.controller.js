const entidadMunicipio = require('../services/municipalities.service');

exports.getAll = async (req, res) => {
    try {
        const data = await entidadMunicipio.findAll();
        res.json({ success: true, data: data });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

exports.getById = async (req, res) => {
    try {
        const data = await entidadMunicipio.findById(req.params.id);
        res.json({ success: true, data: data });
    } catch (error) {
        res.status(404).json({ success: false, error: error.message });
    }
};

exports.create = async (req, res) => {
    try {
        const data = await entidadMunicipio.create(req.body);
        res.status(201).json({ success: true, data: data });
    } catch (error) {
        res.status(400).json({ success: false, error: error.message });
    }
};

exports.update = async (req, res) => {
    try {
        const updated = await entidadMunicipio.update(req.params.id, req.body);
        if (updated) {
            res.json({ success: true, message: 'Municipios actualizado' });
        } else {
            res.status(404).json({ success: false, error: 'Municipios no encontrado' });
        }
    } catch (error) {
        res.status(400).json({ success: false, error: error.message });
    }
};

exports.remove = async (req, res) => {
    try {
        const deleted = await entidadMunicipio.remove(req.params.id);
        if (deleted) {
            res.json({ success: true, message: 'Municipios eliminado' });
        } else {
            res.status(404).json({ success: false, error: 'Municipios no encontrado' });
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};