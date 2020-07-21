import amqpstorm

class AMQPHelper(object):
    def connect(self, amqp_uri, exchange_name):
        self._connection = amqpstorm.UriConnection(amqp_uri)
        self._channel = self._connection.channel()
        self._channel.exchange.bind(source=exchange_name)

    def topic_subscribe(self, topic, callback):
        # let server give unique queue name, as we're not sharing the queue across producers / consumers
        self._channel.queue.bind(queue=topic, exchange=topic)
        self._channel.basic.consume(callback=callback, queue=topic)

    def topic_unsubscribe(self, topic):
        # unsubscribe from queue
        self._channel.queue.bind(queue=topic)

    def get_current_subscriptions(self):
        # return subscriptions
        return self._channel.queues

    def consume(self):
        self._channel.start_consuming()
