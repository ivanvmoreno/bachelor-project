import base64
from os import getenv

# Namespace where kubeless is deployed
KUBELESS_NAMESPACE = getenv('KUBELESS_NAMESPACE')

# RabbitMQ cluster connection URI
RABBITMQ_URI = getenv('RABBITMQ_CONNECTION_URI')

# Default exchange name for shared queues binding
RABBITMQ_EXCHANGE_NAME = getenv('RABBITMQ_EXCHANGE_NAME')

# Path to the directory in which the triggers store volume is mounted
TRIGGERS_VOLUME_PATH = getenv('TRIGGERS_PATH')

# Filename of the triggers store at TRIGGERS_VOLUME_PATH/
TRIGGERS_FILENAME = 'triggers_store'

# Full path to the mounted secret
TRIGGERS_STORE_PATH = f'{TRIGGERS_VOLUME_PATH}/{TRIGGERS_FILENAME}'

# Refresh rate to check for differences in the global state, in ms
TRIGGERS_REFRESH_RATE = 500
