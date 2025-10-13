import pika

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='entidades_events')

    def callback(ch, method, properties, body):
        print(f"Received event: {body}")

    channel.basic_consume(queue='entidades_events', on_message_callback=callback, auto_ack=True)
    print('Waiting for events...')
    channel.start_consuming()