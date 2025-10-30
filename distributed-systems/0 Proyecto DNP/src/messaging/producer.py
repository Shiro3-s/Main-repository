import pika
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def send_event(event_type: str, data: Optional[Dict[str, Any]] = None):
    """
    Send event to RabbitMQ with proper structure
    
    Args:
        event_type (str): Tipo de evento (ej: "proyecto_creado")  
        data (dict, optional): Datos adicionales del evento
    """
    try:
        # Configuración de conexión
        host = os.getenv("RABBITMQ_HOST", "localhost")
        port = int(os.getenv("RABBITMQ_PORT", "5672"))
        user = os.getenv("RABBITMQ_USER", "guest")
        password = os.getenv("RABBITMQ_PASSWORD", "guest")
        
        # Crear conexión
        credentials = pika.PlainCredentials(user, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        )
        channel = connection.channel()
        
        # Declarar cola (asegurar que existe)
        channel.queue_declare(queue='entidades_events', durable=True)
        
        # Crear mensaje estructurado
        message = {
            "event_type": event_type,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat(),
            "service": "ms-proyectos"
        }
        
        # Publicar mensaje
        channel.basic_publish(
            exchange='',
            routing_key='entidades_events',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Hacer el mensaje persistente
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Event sent successfully: {event_type}")
        
    except pika.exceptions.AMQPConnectionError:
        logger.error(f"Could not connect to RabbitMQ at {host}:{port}")
        # En desarrollo, no fallar por problemas de RabbitMQ
        logger.warning("Continuing without sending event (RabbitMQ unavailable)")
    except Exception as e:
        logger.error(f"Error sending event {event_type}: {e}")
        # En desarrollo, no fallar la aplicación por errores de eventos
        logger.warning("Continuing without sending event")

def send_event_simple(event: str):
    """
    Función simple para compatibilidad con código existente
    
    Args:
        event (str): Evento como string simple
    """
    # Parsear el evento si viene en formato "tipo:datos"
    if ":" in event:
        parts = event.split(":", 1)
        event_type = parts[0]
        event_data = {"message": parts[1]}
    else:
        event_type = event
        event_data = {}
    
    send_event(event_type, event_data)