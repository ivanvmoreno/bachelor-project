import base64
from os import getenv

# k8s cluster FQDN
CLUSTER_FQDN = getenv("CLUSTER_FQDN")

# RabbitMQ cluster connection URI
RABBITMQ_URI = getenv("RABBITMQ_CONNECTION_URI")

# Default exchange name for shared queues binding
RABBITMQ_EXCHANGE_NAME = getenv("RABBITMQ_EXCHANGE_NAME")

# Path to the directory in which the triggers store volume is mounted
TRIGGERS_VOLUME_PATH = getenv("TRIGGERS_PATH")

# Filename of the triggers store at TRIGGERS_VOLUME_PATH/
TRIGGERS_FILENAME = 'triggers_store'

# Refresh rate to check for differences in the global state, in ms
TRIGGERS_REFRESH_RATE = 500
