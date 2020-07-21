import yaml
import kopf
import kubernetes
from modules.triggers_helper import marshall_trigger
from exceptions import SecretNotFound, ServiceNotRunning
from config import EVENTS_PROXY_SERVICE, NAMESPACE_NAME, TRIGGER_OBJECT_NAME_PLURAL, TRIGGERS_STORE_SECRET, TRIGGER_OBJECT_GROUP, TRIGGER_OBJECT_API_VERSION

# Operator startup handler
@kopf.on.startup()
def operator_startup(logger, **kwargs):
  # Initialize k8s client
  kubernetes.config.load_incluster_config()
  api = kubernetes.client.CoreV1Api()

  try:
    api.read_namespaced_secret(namespace=NAMESPACE_NAME, name=TRIGGERS_STORE_SECRET)
  except ApiException:
    api_custom_objects = kubernetes.client.CustomObjectsApi()

    # Get all RabbitMQTrigger objects in the cluster (returns list)
    triggers = api_custom_objects.list_namespaced_custom_object(
      TRIGGER_OBJECT_GROUP,
      TRIGGER_OBJECT_API_VERSION,
      NAMESPACE_NAME, 
      TRIGGER_OBJECT_NAME_PLURAL)

    # Marshall list of trigger objects    
    secret_content = dict(map(marshall_trigger, triggers))
    body = api.V1Secret(
      metadata=api.V1ObjectMeta(namespace=NAMESPACE_NAME, name=TRIGGERS_STORE_SECRET),
      data=secret_content)

    # Create k8s namespaced secret containing the marshalled list of triggers
    api.create_namespaced_secret(NAMESPACE_NAME, body)

  try:
    api.read_namespaced_service(EVENTS_PROXY_SERVICE, NAMESPACE_NAME)
  except ApiException:
    raise ServiceNotRunning(f'RabbitMQ events proxy service ({EVENTS_PROXY_SERVICE}) is not running')


# New trigger object handler
@kopf.on.create(TRIGGER_OBJECT_GROUP, TRIGGER_OBJECT_API_VERSION, TRIGGER_OBJECT_NAME_PLURAL)
def handle_new_trigger(body, spec, **kwargs):
    # Initialize k8s client
    kubernetes.config.load_incluster_config()
    api = kubernetes.client.CoreV1Api()

    # Get info from the trigger object
    destination_function = body['spec']['functionSelector']['matchLabels']['function']
    exchange_topic = body['spec']['topic']

    try:
      # Read secret
      secret = api.read_namespaced_secret(TRIGGERS_STORE_SECRET, NAMESPACE_NAME)

      # Update secret contents
      secret.body = { exchange_topic: destination_function, **secret.body }

      api.replace_namespaced_secret(TRIGGERS_STORE_SECRET, NAMESPACE_NAME, secret)
    except ApiException:
      raise SecretNotFound(f'Secret {TRIGGERS_STORE_SECRET} not found in the namespace {NAMESPACE_NAME}')

    # return something?
    

# Deleted trigger object handler
@kopf.on.delete(TRIGGER_OBJECT_GROUP, TRIGGER_OBJECT_API_VERSION, TRIGGER_OBJECT_NAME_PLURAL)
def delete(body, **kwargs):
  # Initialize k8s client
  kubernetes.config.load_incluster_config()
  api = kubernetes.client.CoreV1Api()

  # Get info from the trigger object
  exchange_topic = body['spec']['topic']

  try:
    # Remove secret
    secret = api.read_namespaced_secret(TRIGGERS_STORE_SECRET, NAMESPACE_NAME)
  except ApiException:
    raise SecretDeletionError(f'Secret {TRIGGERS_STORE_SECRET} not found in the namespace {NAMESPACE_NAME}')

  # return something?