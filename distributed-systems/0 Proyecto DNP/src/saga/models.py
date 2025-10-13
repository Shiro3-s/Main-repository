import pika
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def send_event(event_type: str, data: Optional[Dict[str, Any]] = None):
    try:
        host = os.getenv("RABBITMQ_HOST", "localhost")
        port = int(os.getenv("RABBITMQ_PORT", "5672"))
        user = os.getenv("RABBITMQ_USER", "guest")
        password = os.getenv("RABBITMQ_PASSWORD", "guest")
        
        credentials = pika.PlainCredentials(user, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue='entidades_events', durable=True)
        
        message = {
            "event_type": event_type,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat(),
            "service": "ms-proyectos"
        }
        
        channel.basic_publish(
            exchange='',
            routing_key='entidades_events',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        connection.close()
        logger.info(f"Event sent successfully: {event_type}")
        
    except pika.exceptions.AMQPConnectionError:
        logger.error(f"Could not connect to RabbitMQ at {host}:{port}")
        logger.warning("Continuing without sending event (RabbitMQ unavailable)")
    except Exception as e:
        logger.error(f"Error sending event {event_type}: {e}")
        logger.warning("Continuing without sending event")

def send_event_simple(event: str):
    if ":" in event:
        parts = event.split(":", 1)
        event_type = parts[0]
        event_data = {"message": parts[1]}
    else:
        event_type = event
        event_data = {}
    
    send_event(event_type, event_data)