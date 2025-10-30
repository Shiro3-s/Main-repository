from saga.models import SagaInstance, SagaStatus, SagaStep
from messaging.producer import send_event
from db.models import Proyecto
import logging

logger = logging.getLogger(__name__)

def start_saga(proyecto: Proyecto):
    try:
        saga = SagaInstance(
            saga_id=f"saga-{proyecto.codigo_bpin}",
            codigo_bpin=proyecto.codigo_bpin,
            status=SagaStatus.PENDING,
            current_step=SagaStep.CREATE
        )
        
        send_event("proyecto_creado", {"codigo_bpin": proyecto.codigo_bpin})
        
        saga.current_step = SagaStep.RESERVE_INVENTORY
        saga.status = SagaStatus.PENDING
        
        logger.info(f"Saga started: {saga.saga_id}")
        return saga
        
    except Exception as e:
        logger.error(f"Error starting saga for proyecto {proyecto.codigo_bpin}: {e}")
        raise