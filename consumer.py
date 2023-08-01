import pika


class RabbitMQConsumer:
    def __init__(self, callback_fn):
        self.__host = 'localhost'
        self.__port = 5672
        self.__username = 'guest'
        self.__password = 'guest'
        self.__queue = 'data_queue'
        self.__callback = callback_fn
        self.__channel = self.__create_chanell()

    def __create_chanell(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()

        channel.queue_declare(queue=self.__queue, durable=True)

        channel.basic_consume(queue=self.__queue, auto_ack=True, on_message_callback=self.__callback)

        return channel

    def start(self):
        print('Running rabbitmq')
        self.__channel.start_consuming()


def my_callback(ch, method, properties, body):
    print(body)


if __name__ == '__main__':
    consumer = RabbitMQConsumer(my_callback)
    consumer.start()
