from time import sleep
from models.event import EventModel
from config import CLUSTER_FQDN, RABBITMQ_URI, RABBITMQ_EXCHANGE_NAME, TRIGGERS_REFRESH_RATE
from utils.amqp_helper import AMQPHelper
from utils.triggers_helper import diff_triggers, invoke_function, read_triggers

def consume_event(message):
    try:
        # Deserialize event body
        event = EventModel.deserialize(message.body)
        invoke_function(event['subject'], event['data'])
    except ValueError as error:
        print('Error consuming event', message.body, error)


if __name__ == "__main__":
    # Initialize local state from the global state
    local_state = read_triggers()

    # Establish connection to the RabbitMQ message bus
    amqp_connection = AMQPHelper()
    amqp_connection.connect(RABBITMQ_URI, RABBITMQ_EXCHANGE_NAME)

    while(True):
        # Read global state from mounted secret
        global_state = read_triggers()

        # Perform a diff check between local and global states
        state_diff = diff_triggers(local_state, global_state)

        if state_diff:
            for topic, functions in state_diff.items():
                if topic not in local_state:
                    amqp_connection.topic_subscribe(topic, consume_event)
                else:
                    amqp_connection.topic_unsubscribe(topic)
            # Update local state
            local_state = global_state
        
        sleep(TRIGGERS_REFRESH_RATE)
