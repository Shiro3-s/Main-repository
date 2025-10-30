const userService = require('../services/user.service');

exports.findAll = async (req, res) => {
    try {
        const users = await userService.findAll();
        res.status(200).json(users);
    } catch (error) {
        res.status(500).json({ message: "Error al obtener usuarios", error });
    }
};

exports.findById = async (req, res) => {
    try {
        const user = await userService.findById(req.params.id);
        if (!user) {
            return res.status(404).json({ message: "Usuario no encontrado" });
        }
        res.status(200).json(user);
    } catch (error) {
        res.status(500).json({ message: "Error al obtener el usuario", error });
    }
};

exports.create = async (req, res) => {
    try {
        const newUser = await userService.create(req.body);
        res.status(201).json(newUser);
    } catch (error) {
        res.status(500).json({ message: "Error al crear usuario", error });
    }
};

exports.update = async (req, res) => {
    try {
        const updated = await userService.update(req.params.id, req.body);
        if (!updated) {
            return res.status(404).json({ message: "Usuario no encontrado" });
        }
        res.status(200).json({ message: "Usuario actualizado exitosamente" });
    } catch (error) {
        res.status(500).json({ message: "Error al actualizar usuario", error });
    }
};

exports.remove = async (req, res) => {
    try {
        const removed = await userService.remove(req.params.id);
        if (!removed) {
            return res.status(404).json({ message: "Usuario no encontrado" });
        }
        res.status(200).json({ message: "Usuario eliminado exitosamente" });
    } catch (error) {
        res.status(500).json({ message: "Error al eliminar usuario", error });
    }
};