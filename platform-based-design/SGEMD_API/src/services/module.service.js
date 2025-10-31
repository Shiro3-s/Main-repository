const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM modulos')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM modulos WHERE idModulos = ?', [id])
    if (rows.length === 0) throw new Error('Modulo no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    // Ajusta los campos según la tabla
    const fechaActual = new Date()
    const [result] = await pool.execute(
        'INSERT INTO Modulos (Asistencia, Practicas, OpcionGrado, FechaCreacion, FechaActualizacion) VALUES (?, ?, ?,?,?)',
        [data.Asistencia, data.Practicas,data.OpcionGrado,data.Asistencia, fechaActual, fechaActual]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    // Ajusta los campos según la tabla
    const [result] = await pool.execute(
        'UPDATE Modulos SET Asistencia = ?, Practicas = ?, OpcionGrado = ?, FechaActualizacion = ? WHERE idModulos = ?',
        [data.Asistencia, data.Practicas,data.OpcionGrado, new Date(), id]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM Modulos WHERE idModulos = ?', [id]
    )
    return result.affectedRows > 0;
}