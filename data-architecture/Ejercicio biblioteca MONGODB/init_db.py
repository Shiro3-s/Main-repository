import pymongo
from datetime import datetime

connection_string = "mongodb://localhost:27017/"


try:
    client = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=5000)
    client.server_info()  # Fuerza la conexión
    print("Conexión exitosa a la base de datos NoSQL")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print("Error de conexión:", err)
finally:
    dbname = client["biblioteca_db_nosql"]
    print("Conexión exitosa a la base de datos NoSQL")

    recurso_collection = dbname["Recurso"]
    recurso_collection.insert_one({
  "_id": 1,
  "nombre_recurso": "El Quijote",
  "tipo_recurso": {
    "_id": 1,
    "nombre_tipo_recurso": "Libro",
    "desc_tipo_recurso": "Libro impreso"
  },
  "autores_recurso": "Miguel de Cervantes",
  "anio_publicacion": 1605,
  "estado_recurso": "Disponible",
  "cantidad": 3,
  "editorial": {
    "_id": 1,
    "nombre_editorial": "Editorial Clásicos",
    "desc_editorial": "Editorial de libros clásicos de España"
  },
  "recurso_categoria": {
    "_id": 1,
    "categoria": {
      "_id": 1,
      "nombre_categoria": "Literatura",
      "desc_categoria": "Libros de literatura clásica"
    }
  }
})
    persona_collection = dbname["Persona"]
    persona_collection.insert_one(
{
  "_id": 1,
  "cargo": {
    "_id": 1,
    "nombre_cargo": "Bibliotecario",
    "descripcion_cargo": "Se encarga de gestionar los libros de la biblioteca",
    "permisos_cargo": "Cambiar estado de libros, gestionar los libros y gestionar a los clientes"
  },
  "tipo_documento": {
    "_id": 1, 
    "nombre_tipo_documento": "Cédula de ciudadanía",
  	"descripcion_tipo_documento": "Documento de identificación nacional principal"
  },
	"nombre_persona": "Juan Pablo Angel Quitian",
  "telefono_persona": "3186659161",
  "email_persona": "juan.angel-q@uniminuto.edu.co",
  "genero": {
    "_id": 1,
    "nombre_genero": "Masculino"
  }
}
)

    movimiento_collection = dbname["Movimiento"]
    movimiento_collection.insert_one(
    {
  "detalle_movimiento": {
    "_id": 1,
    "tipo_movimiento": {
      "_id": 1,
      "nombre_tipo_movimiento": "Préstamo",
      "descripcion_tipo_movimiento": "Movimiento que se usa al brindarle a una persona un libro temporalmente"
    },
    "fecha_movimiento": datetime.strptime("2025-09-23", "%Y-%m-%d"),
    "fecha_limite": datetime.strptime("2025-10-23", "%Y-%m-%d"),
    "id_usuario": 1
  },
  "_id": 1,
  "estado_recurso": "Buen estado",
  "observacion": "Ninguna",
  "id_recurso": 1
}
)
    print("Datos insertados en las colecciones.")
    print(client.list_database_names())
    client.close()
    print("Conexión cerrada con la base de datos NoSQL.")




