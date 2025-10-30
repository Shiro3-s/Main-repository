from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# Este archivo creamos los objetos para trabajar las tablas de la base de datos
class TipoId(Base):
    __tablename__ = "tiposid"

    i_id_tipoid = Column(String(50), primary_key=True, index=True)
    v_descripcion = Column(String(100), nullable=False)

class Generos(Base):
    __tablename__ = "generos"

    i_id_genero = Column(String(50), primary_key=True, index=True)
    v_descripcion = Column(String(100), nullable=False)
# ... (código existente)

class Personas(Base):
    __tablename__ = "personas"

    v_id_docente = Column(String(50), primary_key=True, index=True)
    v_nombre = Column(String(50), nullable=False)
    v_apellido = Column(String(50), nullable=False)
    i_id_genero = Column(String(50), nullable=True) # Mantenemos nullable=True
    i_id_tipoid = Column(String(50), nullable=True) # Mantenemos nullable=True

# ... (resto del código)

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)