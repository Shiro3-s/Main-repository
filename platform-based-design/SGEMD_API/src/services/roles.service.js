const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM Roles')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM Roles WHERE idRoles = ?', [id])
    if (rows.length === 0) throw new Error('Roles no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    // Ajusta los campos según la tabla
    const fechaActual = new Date()
    const [result] = await pool.execute(
        'INSERT INTO Roles (Nombre, FechaCreacion, FechaActualizacion) VALUES (?, ?, ?)',
        [data.Nombre,fechaActual,fechaActual]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    // Ajusta los campos según la tabla
    const [result] = await pool.execute(
        'UPDATE Roles SET Nombre = ?, FechaActualizacion = ? WHERE idRoles = ?',
        [data.Nombre, new Date(), id]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM Roles WHERE idRoles = ?', [id]
    )
    return result.affectedRows > 0;
}