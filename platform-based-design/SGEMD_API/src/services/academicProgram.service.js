const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM ProgramaAcademico')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM ProgramaAcademico WHERE idProgramaAcademico = ?', [id])
    if (rows.length === 0) throw new Error('Programa Academico no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    // Ajusta los campos según la tabla
    const fechaActual = new Date()
    const [result] = await pool.execute(
        'INSERT INTO ProgramaAcademico (Nombre, FechaCreacion, FechaActualizacion) VALUES (?, ?, ?,?,?,?)',
        [data.Nombre,fechaActual,fechaActual]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    // Ajusta los campos según la tabla
    const [result] = await pool.execute(
        'UPDATE ProgramaAcademico SET Nombre = ?, FechaActualizacion = ? WHERE idProgramaAcademico = ?',
        [data.Nombre, new Date(), id]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM ProgramaAcademico WHERE idProgramaAcademico = ?', [id]
    )
    return result.affectedRows > 0;
}