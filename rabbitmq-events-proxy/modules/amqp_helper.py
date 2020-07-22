import amqpstorm 

class AMQPHelper(object):
    def __init__(self):
        self._consumers = dict()
        self._queue_purge = list()

    def connect(self, amqp_uri, exchange_name):
        self._exchange_name = exchange_name
        self._connection = amqpstorm.UriConnection(amqp_uri)
        self._channel = self._connection.channel()
        self._channel.exchange.bind(source=exchange_name)

    def topic_subscribe(self, topic, callback):
        '''
            Bind topic (queue) to the exchange, in case it's not already binded.
            Give a common queue name, as we're sharing the queue across the exchange
        '''
        self._channel.queue.bind(queue=topic, exchange=self._exchange_name)
        
        # Consume messages from topic, handled by the specified callback
        self._consumers[topic] = 
            self._channel.basic.consume(callback=self._callback(callback), queue=topic)

    def topic_unsubscribe(self, topic):
        # Remove consumer tag from the list of current consumers
        consumer_tag = self._consumers.pop(topic, None)
        
        if consumer_tag not None:
            # Stop queue consumer
            self._channel.basic.cancel(consumer_tag)

        # Check for empty queue
        if self._channel.basic.get(queue=topic):
            # Mark queue for future deletion, when empty
            self._queue_purge.append(topic)
        else:
            self._channel.queue.delete(queue=topic, if_empty=True)


    def _callback(self, callback):
        def post_cleanup():
            # Call the original callback
            callback()

            # Check for queues pending deletion
            if (len(self._queue_purge)):
                for queue in self._queue_purge:
                    # If the queue is empty, perform deletion
                    if not self._channel.basic.get(queue=topic):
                        self._channel.queue.delete(queue=topic, if_empty=True)
        return post_cleanup

    def get_current_subscriptions(self):
        return self._consumers
