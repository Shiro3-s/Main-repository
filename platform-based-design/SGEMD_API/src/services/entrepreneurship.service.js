const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM Emprendimiento')
    return rows
};

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM Emprendimiento WHERE idEmprendimiento = ?', [id]);
    if (rows.length === 0) throw new Error('Emprendimiento no encontrado');
    return rows[0]
}

exports.create = async (data) => {
    const fechaActual = new Date()
    const [result] = await pool.execute(
        `INSERT INTO Emprendimiento (
            Nombre, Descripcion, TipoEmprendimiento, SectorProductivo,
            RedesSociales, Acompanamiento, FechaCreacion, FechaActualizacion,
            ActaCompromiso, EtapadeEmpedimiento_idEtapadeEmpedimiento
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [
            data.Nombre,
            data.Descripcion,
            data.TipoEmprendimiento,
            data.SectorProductivo,
            data.RedesSociales,
            data.Acompanamiento,
            fechaActual,
            fechaActual,
            data.ActaCompromiso,
            data.EtapadeEmpedimiento_idEtapadeEmpedimiento
        ]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    const [result] = await pool.execute(
        `UPDATE Emprendimiento SET
            Nombre = ?, Descripcion = ?, TipoEmprendimiento = ?, SectorProductivo = ?,
            RedesSociales = ?, Acompanamiento = ?, FechaActualizacion = ?,
            ActaCompromiso = ?, EtapadeEmpedimiento_idEtapadeEmpedimiento = ?
        WHERE idEmprendimiento = ?`,
        [
            data.Nombre,
            data.Descripcion,
            data.TipoEmprendimiento,
            data.SectorProductivo,
            data.RedesSociales,
            data.Acompanamiento,
            new Date(),
            data.ActaCompromiso,
            data.EtapadeEmpedimiento_idEtapadeEmpedimiento,
            id
        ]
    )
    return result.affectedRows > 0;
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM Emprendimiento WHERE idEmprendimiento = ?', [id]
    )
    return result.affectedRows > 0;
}