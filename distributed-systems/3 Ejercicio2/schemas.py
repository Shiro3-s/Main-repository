from pydantic import BaseModel
from typing import Optional

class tipoIdBase(BaseModel):
    i_id_tipoid: str  # Cambiado de i_tipoId e int
    v_descripcion: str  # Cambiado de v_nombreTipoDoc
    
class tipoIdCreate(tipoIdBase):
    pass    

class tipoIdResponse(tipoIdBase):   # Cambiado de tipoidResponse
    class Config:
        from_attributes = True  # Cambiado de orm_mode

class personasBase(BaseModel):
    v_id_docente: str  # Cambiado para coincidir con el modelo
    v_nombre: str
    v_apellido: str
    i_id_genero: Optional[str] = None  # Cambiado a str y opcional
    i_id_tipoid: Optional[str] = None  # Agregado

class personasCreate(personasBase):
    pass

class personasResponse(personasBase):
    class Config:
        from_attributes = True

class generosBase(BaseModel):
    i_id_genero: str  # Cambiado de int
    v_descripcion: str

class generosCreate(generosBase):
    pass

class generosResponse(generosBase):
    class Config:
        from_attributes = True