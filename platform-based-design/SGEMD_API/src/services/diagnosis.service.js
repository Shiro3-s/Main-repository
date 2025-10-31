const { pool } = require('../config/db.config')

exports.findAll = async () => {
    const [rows] = await pool.execute('SELECT * FROM Diagnosticos')
    return rows
}

exports.findById = async (id) => {
    const [rows] = await pool.execute('SELECT * FROM Diagnosticos WHERE idDiagnosticos = ?', [id])
    if (rows.length === 0) throw new Error('Diagnóstico no encontrado')
    return rows[0]
}

exports.create = async (data) => {
    const [result] = await pool.execute(
        `INSERT INTO Diagnosticos (
            FechaEmprendimiento, AreaEstrategia, Diferencial, Planeacion,
            MercadoObjetivo, Tendencias, Canales, DescripcionPromocion,
            SectoEconomico_idSectoEconomico, Emprendimiento_idEmprendimiento,
            Presentacion, PasosElaboracion, SituacionFinanciera, FuenteFinanciero,
            EstructuraOrganica, ConocimientoLegal, MetodologiaInnovacion,
            HerramientaTecnologicas, Marca, AplicacionMetodologia,
            ImpactoAmbiental, ImpactoSocial, Viabilidad
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [
            data.FechaEmprendimiento,
            data.AreaEstrategia,
            data.Diferencial,
            data.Planeacion,
            data.MercadoObjetivo,
            data.Tendencias,
            data.Canales,
            data.DescripcionPromocion,
            data.SectoEconomico_idSectoEconomico,
            data.Emprendimiento_idEmprendimiento,
            data.Presentacion,
            data.PasosElaboracion,
            data.SituacionFinanciera,
            data.FuenteFinanciero,
            data.EstructuraOrganica,
            data.ConocimientoLegal,
            data.MetodologiaInnovacion,
            data.HerramientaTecnologicas,
            data.Marca,
            data.AplicacionMetodologia,
            data.ImpactoAmbiental,
            data.ImpactoSocial,
            data.Viabilidad
        ]
    )
    return { id: result.insertId, ...data }
}

exports.update = async (id, data) => {
    const [result] = await pool.execute(
        `UPDATE Diagnosticos SET
            FechaEmprendimiento = ?, AreaEstrategia = ?, Diferencial = ?, Planeacion = ?,
            MercadoObjetivo = ?, Tendencias = ?, Canales = ?, DescripcionPromocion = ?,
            SectoEconomico_idSectoEconomico = ?, Emprendimiento_idEmprendimiento = ?,
            Presentacion = ?, PasosElaboracion = ?, SituacionFinanciera = ?, FuenteFinanciero = ?,
            EstructuraOrganica = ?, ConocimientoLegal = ?, MetodologiaInnovacion = ?,
            HerramientaTecnologicas = ?, Marca = ?, AplicacionMetodologia = ?,
            ImpactoAmbiental = ?, ImpactoSocial = ?, Viabilidad = ?
        WHERE idDiagnosticos = ?`,
        [
            data.FechaEmprendimiento,
            data.AreaEstrategia,
            data.Diferencial,
            data.Planeacion,
            data.MercadoObjetivo,
            data.Tendencias,
            data.Canales,
            data.DescripcionPromocion,
            data.SectoEconomico_idSectoEconomico,
            data.Emprendimiento_idEmprendimiento,
            data.Presentacion,
            data.PasosElaboracion,
            data.SituacionFinanciera,
            data.FuenteFinanciero,
            data.EstructuraOrganica,
            data.ConocimientoLegal,
            data.MetodologiaInnovacion,
            data.HerramientaTecnologicas,
            data.Marca,
            data.AplicacionMetodologia,
            data.ImpactoAmbiental,
            data.ImpactoSocial,
            data.Viabilidad,
            id
        ]
    )
    return result.affectedRows > 0
}

exports.remove = async (id) => {
    const [result] = await pool.execute(
        'DELETE FROM Diagnosticos WHERE idDiagnosticos = ?', [id]
    )
    return result.affectedRows > 0
}