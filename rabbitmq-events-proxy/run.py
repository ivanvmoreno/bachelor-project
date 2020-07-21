from time import sleep
from threading import Thread
from models.event import EventModel
from config import CLUSTER_FQDN, TRIGGERS_REFRESH_RATE
from modules.amqp_helper import AMQPHelper
from modules.triggers_helper import diff_triggers, get_function_uri, read_triggers
import requests

def refresh_triggers():
    while(True):
        global local_state, amqp_connection
        global_state = read_triggers()
        subscriptions = get_current_subscriptions()
        state_diff = diff_triggers(local_state, global_state)
        if state_diff:
            for topic, functions in state_diff.items():
                if topic not in local_state:
                    topic_subscribe(topic)
                else:
                    topic_unsubscribe(topic)
            local_state = global_state
        sleep(TRIGGERS_REFRESH_RATE)


def consume_event(message):
    try:
        event = EventModel.deserialize(message.body)
        # event.subject, event.data
        # invoke the function based on the message subject
        # http invokation with the cluster FQDN
        # only acknowledge message after successful response from the HTTP request
        # as of now, procceed only with POSTs (webhooks-like)
        r = requests.post(get_function_uri(event.subject), data=event.data)
        # check for successful request

    except ValueError as error:
        print('Error consuming event', message.body, error)


if __name__ == "__main__":
    # Initialize local status from the global store
    local_state = read_triggers()
    amqp_connection = AMQPHelper()
