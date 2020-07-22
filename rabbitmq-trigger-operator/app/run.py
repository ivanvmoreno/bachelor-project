import yaml
import kopf
import kubernetes
from utils.triggers_helper import marshall_trigger, remove_trigger_store
from exceptions import MissingTriggerStore, ServiceNotRunning
from config import EVENTS_PROXY_SERVICE, NAMESPACE_NAME, TRIGGER_OBJECT_NAME_PLURAL, TRIGGERS_STORE_SECRET, TRIGGER_OBJECT_GROUP, TRIGGER_OBJECT_API_VERSION

# Operator startup handler
@kopf.on.startup()
def operator_startup(logger, **_):
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
def handle_new_trigger(spec, **_):
  # Initialize k8s client
  kubernetes.config.load_incluster_config()
  api = kubernetes.client.CoreV1Api()

  # Get info from the trigger object
  destination_function = spec['functionSelector']['matchLabels']['function']
  exchange_topic = spec['topic']

  try:
    # Read secret
    secret = api.read_namespaced_secret(TRIGGERS_STORE_SECRET, NAMESPACE_NAME)

    # Update secret contents
    secret.body = { exchange_topic: destination_function, **secret.body }
    api.replace_namespaced_secret(TRIGGERS_STORE_SECRET, NAMESPACE_NAME, secret)
  except ApiException:
    raise kopf.TemporaryError(f'Secret {TRIGGERS_STORE_SECRET} not found in the namespace {NAMESPACE_NAME}', delay=30)
    

# Deleted trigger object handler
@kopf.on.delete(TRIGGER_OBJECT_GROUP, TRIGGER_OBJECT_API_VERSION, TRIGGER_OBJECT_NAME_PLURAL)
def delete(spec, **_):
  # Initialize k8s client
  kubernetes.config.load_incluster_config()
  api = kubernetes.client.CoreV1Api()

  # Get info from the trigger object
  exchange_topic = spec['topic']

  try:
    # Read secret
    secret = api.read_namespaced_secret(TRIGGERS_STORE_SECRET, NAMESPACE_NAME)
  except ApiException:
    raise kopf.TemporaryError(f'Secret {TRIGGERS_STORE_SECRET} not found in the namespace {NAMESPACE_NAME}', delay=30)

  try:
    # Update secret contents
    secret.body = remove_trigger_store(exchange_topic, secret.body)
    api.replace_namespaced_secret(TRIGGERS_STORE_SECRET, NAMESPACE_NAME, secret)
  except MissingTriggerStore as error:
    raise kopf.TemporaryError(f'Trigger (topic {exchange_topic}) not found in the trigger secret store {TRIGGERS_STORE_SECRET}', delay=30)