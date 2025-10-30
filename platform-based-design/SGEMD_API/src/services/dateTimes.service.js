const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM Fecha_y_Horarios')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM Fecha_y_Horarios WHERE idFecha_y_Horarios = ?', [id])
    if (rows.length === 0) throw new Error('Fecha y horario no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    const [result] = await pool.execute(
        `INSERT INTO Fecha_y_Horarios (
            idFecha_y_Horarios, Fecha_inicio, Hora_inicio, Fecha_fin, Hora_fin
        ) VALUES (?, ?, ?, ?, ?)`,
        [
            data.idFecha_y_Horarios,
            data.Fecha_inicio,
            data.Hora_inicio,
            data.Fecha_fin,
            data.Hora_fin
        ]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    const [result] = await pool.execute(
        `UPDATE Fecha_y_Horarios SET
            Fecha_inicio = ?, Hora_inicio = ?, Fecha_fin = ?, Hora_fin = ?
        WHERE idFecha_y_Horarios = ?`,
        [
            data.Fecha_inicio,
            data.Hora_inicio,
            data.Fecha_fin,
            data.Hora_fin,
            id
        ]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM Fecha_y_Horarios WHERE idFecha_y_Horarios = ?', [id]
    )
    return result.affectedRows > 0
}