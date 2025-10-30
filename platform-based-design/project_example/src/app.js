const express = require('express');
const userRoutes = require('./routes/user.routes'); //declaramos las rutas de usuarios
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

//prefijo de la API y montaje de las rutas, por cada entidad habrá una ruta
app.use('/api/users', userRoutes);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});