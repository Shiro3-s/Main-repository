const db = require('../config/db.config');

exports.findAll = async () => {
    const [rows] = await db.execute('SELECT * FROM user');
    return rows;
};

exports.findById = async (id) => {
    const [rows] = await db.execute('SELECT * FROM user WHERE id = ?', [id]);
    return rows[0];
};

exports.create = async (newUser) => {
    const [result] = await db.execute(
        'INSERT INTO user (nombre, correo) VALUES (?, ?)',
        [newUser.nombre, newUser.correo]
    );
    return { id: result.insertId, ...newUser };
};

exports.update = async (id, updatedUser) => {
    const [result] = await db.execute(
        'UPDATE user SET nombre = ?, correo = ? WHERE id = ?',
        [updatedUser.nombre, updatedUser.correo, id]
    );
    return result.affectedRows > 0;
};

exports.remove = async (id) => {
    const [result] = await db.execute('DELETE FROM user WHERE id = ?', [id]);
    return result.affectedRows > 0;
};