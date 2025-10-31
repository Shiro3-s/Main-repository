const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM Modalidad')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM Modalidad WHERE idModalidad = ?', [id])
    if (rows.length === 0) throw new Error('Modalidad no encontrada')
    return rows[0]
}

exports.create = async (data) => {
    const [result] = await pool.execute(
        `INSERT INTO Modalidad (
            idModalidad, Presencial, Distancia, Enlace_virtual, Lugar
        ) VALUES (?, ?, ?, ?, ?)`,
        [
            data.idModalidad,
            data.Presencial,
            data.Distancia,
            data.Enlace_virtual,
            data.Lugar
        ]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    const [result] = await pool.execute(
        `UPDATE Modalidad SET
            Presencial = ?, Distancia = ?, Enlace_virtual = ?, Lugar = ?
        WHERE idModalidad = ?`,
        [
            data.Presencial,
            data.Distancia,
            data.Enlace_virtual,
            data.Lugar,
            id
        ]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM Modalidad WHERE idModalidad = ?', [id]
    )
    return result.affectedRows > 0
}