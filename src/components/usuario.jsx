import React, { useEffect, useState } from "react";

function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);

  useEffect(() => {
    fetch("http://localhost:3005/segmed/users")
      .then((res) => res.json())
      .then((data) => {
        console.log("Usuarios cargados:", data);
        setUsuarios(data);
      })
      .catch((err) => console.error("Error al cargar usuarios:", err));
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1> Lista de Usuarios</h1>
      {usuarios.length > 0 ? (
        <ul>
          {usuarios.map((u) => (
            <li key={u.id_usuario}>
              <strong>{u.nombre}</strong> — {u.usuario}
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay usuarios registrados o no se pudieron cargar los datos.</p>
      )}
    </div>
  );
}

export default Usuarios;
