const db = require('../config/db.config');

exports.findAll = async () => {
    const [rows] = await db.query('SELECT * FROM users');
    return rows;
}

exports.findById = async (id) => {
    const [rows] = await db.query('SELECT * FROM users WHERE id = ?', [id]);
    return rows[0];
}

exports.create = async (user) => {
    const [result] = await db.execute(
        'INSERT INTO users (name, email) VALUES (?, ?)',
        [user.newName, user.newEmail]
    );
    return { id: result.insertId, ...user };
}

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