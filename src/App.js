import React, { useState } from "react";
import "./App.css";

function App() {
  const [usuario, setUsuario] = useState("");
  const [clave, setClave] = useState("");
  const [mensaje, setMensaje] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
/*
    El endpoint de register esta en el node, si se quiere registrar un nuevo usuario se sigue el siguiente endpoint:
    http://localhost:3005/sgmed/users/register

    realizas la siguiente estructura en el body:

    {
      "Nombre": "Carlos Pérez",
      "CorreoInstitucional": "monocho29@gmail.com",
      "CorreoPersonal": "monocho29@gmail.com",
      "Password": "abcdef123",
      "Celular": "3198765432",
      "Telefono": "6011122233",
      "Direccion": "Carrera 23 #45-67",
      "Genero": "Masculino",
      "EstadoCivil": "Soltero",
      "FechaNacimiento": "1998-07-22",
      "ProgramaAcademico_idProgramaAcademico1": 2,
      "CentroUniversitarios_idCentroUniversitarios": 1,
      "Estado": 1,
      "Semestre": "3",
      "Modalidad": "Virtual",
      "Roles_idRoles1": 2,
      "FechaCreacion": "2025-10-28",
      "FechaActualizacion": "2025-10-28"
    }
*/
    try {
      const response = await fetch("http://localhost:3005/sgmed/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          CorreoInstitucional: usuario,
          Password: clave
        }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setMensaje(`Bienvenido ${data.data.user.Nombre}`);
      } else {
        setMensaje(`Error: ${data.message || "Credenciales inválidas"}`);
      }
    } catch (error) {
      setMensaje("Error de conexión con el servidor.");
      console.error("Error de conexión:", error);
    }
  };

  return (
    <div className="App">
      <h1>Inicio de Sesión</h1>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Usuario"
          value={usuario}
          onChange={(e) => setUsuario(e.target.value)}
          required
        />
        <br />
        <input
          type="password"
          placeholder="Contraseña"
          value={clave}
          onChange={(e) => setClave(e.target.value)}
          required
        />
        <br />
        <button type="submit">Ingresar</button>
      </form>
      {mensaje && <p>{mensaje}</p>}
    </div>
  );
}

export default App;
