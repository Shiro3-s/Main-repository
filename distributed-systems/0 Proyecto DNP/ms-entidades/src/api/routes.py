from fastapi import APIRouter, Depends
from db.models import Region, Departamento, Municipio, NivelGobierno, EntidadEjecutora

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/region/{id}", response_model=Region)
def get_region(id: int):
    # Aquí iría la consulta a la base de datos
    return Region(id_region=id, nombre_region="Caribe")