const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM Seguimientos')
    return rows;
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM Seguimientos WHERE idSeguimientos = ?', [id])
    if (rows.length === 0) throw new Error('Seguimiento no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    const fechaActual = new Date();
    const [result] = await pool.execute(
        `INSERT INTO Seguimientos (
            histproal, TipoSeguimiento, Descripcion, Seguimientoscol,
            FechaCreacion, FechaActualizacion
        ) VALUES (?, ?, ?, ?, ?, ?)`,
        [
            data.histproal,
            data.TipoSeguimiento,
            data.Descripcion,
            data.Seguimientoscol,
            fechaActual,
            fechaActual
        ]
    )
    return { id: result.insertId, ...data };
}

exports.update = async (id, data) => {
    const [result] = await pool.execute(
        `UPDATE Seguimientos SET
            histproal = ?, TipoSeguimiento = ?, Descripcion = ?, Seguimientoscol = ?,
            FechaActualizacion = ?
        WHERE idSeguimientos = ?`,
        [
            data.histproal,
            data.TipoSeguimiento,
            data.Descripcion,
            data.Seguimientoscol,
            new Date(),
            id
        ]
    )
    return result.affectedRows > 0;
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM Seguimientos WHERE idSeguimientos = ?', [id]
    )
    return result.affectedRows > 0;
}