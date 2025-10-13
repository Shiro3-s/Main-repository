import pika

def send_event(event: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='entidades_events')
    channel.basic_publish(exchange='', routing_key='entidades_events', body=event)
    connection.close()