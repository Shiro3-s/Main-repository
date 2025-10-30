const mysql = require('mysql2/promise');

const dbConfig = {
    host: 'localhost',
    port: '3306',
    user: 'root',
    password: '',
    database: 'db_segmed',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
};

// Crear pool de conexiones
const pool = mysql.createPool(dbConfig);

// Probar la conexión
async function testConnection() {
    try {
        const connection = await pool.getConnection();
        console.log('Conexión a la base de datos exitosa');
        connection.release();
        return true;
    } catch (error) {
        console.error('Error conectando a la base de datos:', error.message);
        return false;
    }
}

module.exports = {
    pool,
    testConnection
};