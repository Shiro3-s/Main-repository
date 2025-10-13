from pydantic import BaseModel

class Region(BaseModel):
    id_region: int
    nombre_region: str

class Departamento(BaseModel):
    id_departamento: int
    cod_dane_departamento: str
    nombre_departamento: str
    id_region: int

class Municipio(BaseModel):
    id_municipio: int
    cod_dane_municipio: str
    nombre_municipio: str
    coordenadas_lat: str
    coordenadas_long: str
    id_departamento: int

class NivelGobierno(BaseModel):
    id_nivel_gob: int
    nombre_nivel_gob: str
    desc_nivel_gob: str

class EntidadEjecutora(BaseModel):
    id_entidad_ejecutora: int
    nombre_entidad: str
    nit_entidad: str
    email_contacto: str
    telefono_contacto: str
    representante_legal: str
    estado_entidad: int
    id_tipo_entidad: int
    id_nivel_gob: int