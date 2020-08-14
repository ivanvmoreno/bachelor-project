import base64
from os import getenv

# Namespace where kubeless is deployed
KUBELESS_NAMESPACE = getenv('KUBELESS_NAMESPACE')

# RabbitMQ cluster connection URI
RABBITMQ_URI = getenv('RABBITMQ_CONNECTION_URI')

# Default exchange name for shared queues binding
RABBITMQ_EXCHANGE_NAME = getenv('RABBITMQ_EXCHANGE_NAME')

# Path to the directory in which the triggers store volume is mounted
TRIGGERS_MOUNT_PATH = getenv('TRIGGERS_MOUNT_PATH')

# Key (file in the mounted volume) where the secret stores the global triggers state
TRIGGERS_SECRET_KEY = 'triggers_store'

# Full path to the mounted secret
TRIGGERS_STORE_PATH = f'{TRIGGERS_MOUNT_PATH}/{TRIGGERS_SECRET_KEY}'

# Refresh rate to check for differences in the global state, in ms
TRIGGERS_REFRESH_RATE = 500
