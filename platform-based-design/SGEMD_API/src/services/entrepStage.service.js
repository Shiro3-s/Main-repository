const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM EtapadeEmpedimiento')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM EtapadeEmpedimiento WHERE idEtapadeEmpedimiento = ?', [id])
    if (rows.length === 0) throw new Error('Etapa de emprendimiento no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    // Ajusta los campos según la tabla
    const fechaActual = new Date()
    const [result] = await pool.execute(
        'INSERT INTO EtapadeEmpedimiento (Estado, FechaCreacion, FechaActualizacion, TipoEtapa) VALUES (?, ?, ?, ?)',
        [data.Estado,fechaActual,fechaActual,data.TipoEtapa]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    // Ajusta los campos según la tabla
    const [result] = await pool.execute(
        'UPDATE EtapadeEmpedimiento SET Estado = ?, FechaActualizacion = ?, TipoEtapa = ? WHERE idEtapadeEmpedimiento = ?',
        [data.Estado, new Date(), data.TipoEtapa,id]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM EtapadeEmpedimiento WHERE idEtapadeEmpedimiento = ?', [id]
    )
    return result.affectedRows > 0;
}