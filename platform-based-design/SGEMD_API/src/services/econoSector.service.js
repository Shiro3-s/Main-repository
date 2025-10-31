const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM SectoEconomico')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM SectoEconomico WHERE idSectoEconomico = ?', [id])
    if (rows.length === 0) throw new Error('Sector Economico no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    // Ajusta los campos según la tabla
    const [result] = await pool.execute(
        'INSERT INTO SectoEconomico (Nombre) VALUES (?)',
        [data.Nombre]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    // Ajusta los campos según la tabla
    const [result] = await pool.execute(
        'UPDATE SectoEconomico SET Nombre = ? WHERE idSectoEconomico = ?',
        [data.Nombre, id]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM SectoEconomico WHERE idSectoEconomico = ?', [id]
    )
    return result.affectedRows > 0;
}