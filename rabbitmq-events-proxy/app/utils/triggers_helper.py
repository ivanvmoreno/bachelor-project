import json
import requests
from pathlib import Path
from config import KUBELESS_NAMESPACE, TRIGGERS_STORE_PATH

# Read triggers from the mounted secret
def read_triggers():
    content = Path(TRIGGERS_STORE_PATH).read_text()
    return json.loads(content)


# Disjunction of the two sets
def diff_triggers(current, updated):
    diff = dict()
    for key in set(current).difference(updated):
        diff[key] = current[key]
    for key in set(updated).difference(current):
        diff[key] = updated[key]
    return diff if len(diff) else None


# Returns destination function's service ClusterIP URI
def get_function_uri(fn_name):
    return f'{fn_name}.{KUBELESS_NAMESPACE}'


# Perform an HTTP invocation of a kubeless function
def invoke_function(subject, payload):
    # Invoke the function using its HTTP trigger
    r = requests.post(get_function_uri(subject, data=payload))

    try:
        # Check if request has an unsuccessful status code
        r.raise_for_status()

        #  Acknowledge RabbitMQ message
        message.ack()
    except HTTPError:
        # Reject message and put back into the queue
        message.reject(requeue=True)
