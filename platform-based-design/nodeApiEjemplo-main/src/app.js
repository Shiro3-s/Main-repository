const express = require('express');
const userRoutes = require('./routes/user.routes');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Prefijo de la API y montaje de las rutas
app.use('/api/users', userRoutes);

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});