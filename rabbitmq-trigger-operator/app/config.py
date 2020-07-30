from os import getenv

# Namespace grouping the project components and RabbitMQTrigger objects
TRIGGERS_NAMESPACE = getenv('TRIGGERS_NAMESPACE')

# Group of the trigger CRD
TRIGGERS_GROUP = getenv('TRIGGERS_GROUP')

# k8s ApiVersion of the trigger CRD
TRIGGERS_VERSION = getenv('TRIGGERS_VERSION')

# Plural name of the trigger CRD
TRIGGERS_PLURAL = getenv('TRIGGERS_PLURAL')

# Name of the secret containing the triggers store
TRIGGERS_STORE_SECRET = getenv('TRIGGERS_PLURAL')

# Key in which to store the triggers global state on the secret
TRIGGERS_SECRET_KEY = 'triggers_store'

# Service name of the RabbitMQ events proxy
EVENTS_PROXY_SERVICE = getenv('EVENTS_PROXY_SERVICE')
