const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM TipoUsuarios')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM TipoUsuarios WHERE idTipoUsuarios = ?', [id])
    if (rows.length === 0) throw new Error('Tipo de usuario no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    // Ajusta los campos según la tabla
    const fechaActual = new Date()
    const [result] = await pool.execute(
        'INSERT INTO TipoUsuarios (TipodeUsuario, FechaCreacion, FechaActualizacion) VALUES (?, ?, ?)',
        [data.TipodeUsuario,fechaActual,fechaActual]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    // Ajusta los campos según la tabla
    const [result] = await pool.execute(
        'UPDATE TipoUsuarios SET TipodeUsuario = ?, FechaActualizacion = ? WHERE idTipoUsuarios = ?',
        [data.TipodeUsuario, new Date(), id]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM TipoUsuarios WHERE idTipoUsuarios = ?', [id]
    )
    return result.affectedRows > 0;
}