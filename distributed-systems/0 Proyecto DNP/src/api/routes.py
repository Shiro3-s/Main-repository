from fastapi import APIRouter, Depends, HTTPException, status
from db.models import Hito, Proyecto, Contrato, Riesgo, Impacto, NivelRiesgo, AvanceFisico, FaseProyecto
from saga.handlers import start_saga
from saga.models import SagaInstance, SagaStatus, SagaStep
from messaging.producer import send_event
import logging
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/hitos/", response_model=List[Hito])
async def get_hitos():
    try:
        logger.info("Retrieving all hitos")
        return []
    except Exception as e:
        logger.error(f"Error retrieving hitos: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving hitos")

@router.get("/proyectos/", response_model=List[Proyecto])
async def get_proyectos():
    try:
        logger.info("Retrieving all proyectos")
        return []
    except Exception as e:
        logger.error(f"Error retrieving proyectos: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving proyectos")

@router.get("/contratos/", response_model=List[Contrato])
async def get_contratos():
    try:
        logger.info("Retrieving all contratos")
        return []
    except Exception as e:
        logger.error(f"Error retrieving contratos: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving contratos")

@router.post("/proyectos/post", response_model=Proyecto)
async def create_proyecto(proyecto: Proyecto):
    try:
        logger.info(f"Creating proyecto: {proyecto.codigo_bpin}")
        saga = start_saga(proyecto)
        logger.info(f"Started saga {saga.saga_id} for proyecto {proyecto.codigo_bpin}")
        send_event("proyecto_creado", {"codigo_bpin": proyecto.codigo_bpin})
        return proyecto
    except Exception as e:
        logger.error(f"Error creating proyecto: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating proyecto: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ms-proyectos"}