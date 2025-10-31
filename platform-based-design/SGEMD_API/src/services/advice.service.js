const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM Asesorias')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM Asesorias WHERE idAsesorias = ?', [id])
    if (rows.length === 0) throw new Error('Asesoría no encontrada')
    return rows[0]
}

exports.create = async (data) => {
    const [result] = await pool.execute(
        `INSERT INTO Asesorias (
            Nombre_de_asesoria, Descripcion, Fecha_asesoria, Comentarios,
            Fecha_creacion, Fecha_actualizacion, confimacion,
            Usuarios_idUsuarios, Modalidad_idModalidad, Fecha_y_Horarios_idFecha_y_Horarios
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [
            data.Nombre_de_asesoria,
            data.Descripcion,
            data.Fecha_asesoria,
            data.Comentarios,
            data.Fecha_creacion,
            data.Fecha_actualizacion,
            data.confimacion,
            data.Usuarios_idUsuarios,
            data.Modalidad_idModalidad,
            data.Fecha_y_Horarios_idFecha_y_Horarios
        ]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    const [result] = await pool.execute(
        `UPDATE Asesorias SET
            Nombre_de_asesoria = ?, Descripcion = ?, Fecha_asesoria = ?, Comentarios = ?,
            Fecha_creacion = ?, Fecha_actualizacion = ?, confimacion = ?,
            Usuarios_idUsuarios = ?, Modalidad_idModalidad = ?, Fecha_y_Horarios_idFecha_y_Horarios = ?
        WHERE idAsesorias = ?`,
        [
            data.Nombre_de_asesoria,
            data.Descripcion,
            data.Fecha_asesoria,
            data.Comentarios,
            data.Fecha_creacion,
            data.Fecha_actualizacion,
            data.confimacion,
            data.Usuarios_idUsuarios,
            data.Modalidad_idModalidad,
            data.Fecha_y_Horarios_idFecha_y_Horarios,
            id
        ]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM Asesorias WHERE idAsesorias = ?', [id]
    )
    return result.affectedRows > 0
}