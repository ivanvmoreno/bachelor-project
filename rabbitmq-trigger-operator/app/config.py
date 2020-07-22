from os import getenv

# Name of the namespace
NAMESPACE_NAME = getenv('NAMESPACE_NAME')

# Group of the trigger CRD
TRIGGER_OBJECT_GROUP = getenv('TRIGGER_OBJECT_GROUP')

# k8s ApiVersion of the trigger CRD
TRIGGER_OBJECT_API_VERSION = getenv('TRIGGER_OBJECT_API_VERSION')

# Plural name of the trigger CRD
TRIGGER_OBJECT_NAME_PLURAL = getenv('TRIGGER_OBJECT_NAME_PLURAL')

# Name of the secret containing the triggers store
TRIGGERS_STORE_SECRET = getenv('TRIGGER_OBJECT_NAME_PLURAL')

# Service name of the RabbitMQ events proxy
EVENTS_PROXY_SERVICE = getenv('TRIGGER_OBJECT_NAME_PLURAL')
