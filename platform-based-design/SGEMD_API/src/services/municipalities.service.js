const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM Municipios')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM Municipios WHERE idMunicipio = ?', [id])
    if (rows.length === 0) throw new Error('Municipio no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    // Ajusta los campos según la tabla
    const fechaActual = new Date()
    const [result] = await pool.execute(
        'INSERT INTO Municipios (idMunicipio, Nombre, FechaCreacion, FechaActualizacion) VALUES (?, ?, ?,?)',
        [data.idMunicipio, data.Nombre,fechaActual,fechaActual]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    // Ajusta los campos según la tabla
    const [result] = await pool.execute(
        'UPDATE Municipios SET idMunicipio = ?, Nombre = ?, FechaActualizacion = ? WHERE idMunicipio = ?',
        [data.idMunicipio, data.Nombre, new Date(), id]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM Municipios WHERE idMunicipio = ?', [id]
    )
    return result.affectedRows > 0;
}