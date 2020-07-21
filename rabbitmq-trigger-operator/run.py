import kopf
import kubernetes
import yaml
from config import TRIGGERS_STORE_FILENAME, TRIGGERS_STORE_PVC_NAME

# Operator startup handler
@kopf.on.startup()
def operator_startup(logger, **kwargs):
  # Check if shared volume exists
  
  # Get all RabbitMQTrigger objects in the cluster

  # Create the file in the PVC
  # Create the secret if it doesn't exist
  # Update the secret if exists already

  # Check if events-proxy service is running in the cluster. Otherwise, fail


# New trigger object handler
@kopf.on.create('zalando.org', 'v1', 'databases')
def handle_new_trigger(body, spec, **kwargs):
    # Get info from the trigger object
    destination_function = body['spec']['functionSelector']['matchLabels']['function']

    # Make sure type is provided
    if not type:
        raise kopf.HandlerFatalError(f"Type must be set. Got {type}.")

    # Pod template
    pod = {'apiVersion': 'v1', 'metadata': {'name' : name, 'labels': {'app': 'db'}}}

    # Service template
    svc = {'apiVersion': 'v1', 'metadata': {'name' : name}, 'spec': { 'selector': {'app': 'db'}, 'type': 'NodePort'}}

    # Update templates based on Database specification

    if type == 'mongo':
      image = 'mongo:4.0'
      port = 27017
      pod['spec'] = { 'containers': [ { 'image': image, 'name': type } ]}
      svc['spec']['ports'] = [{ 'port': port, 'targetPort': port}]
    if type == 'mysql':
      image = 'mysql:8.0'
      port = 3306
      pod['spec'] = { 'containers': [ { 'image': image, 'name': type, 'env': [ { 'name': 'MYSQL_ROOT_PASSWORD', 'value': 'my_passwd' } ] } ]}
      svc['spec']['ports'] = [{ 'port': port, 'targetPort': port}]

    # Make the Pod and Service the children of the Database object
    kopf.adopt(pod, owner=body)
    kopf.adopt(svc, owner=body)

    # Object used to communicate with the API Server
    api = kubernetes.client.CoreV1Api()

    # Create Pod
    obj = api.create_namespaced_pod(namespace, pod)
    print(f"Pod {obj.metadata.name} created")

    # Create Service
    obj = api.create_namespaced_service(namespace, svc)
    print(f"NodePort Service {obj.metadata.name} created, exposing on port {obj.spec.ports[0].node_port}")

    # Update status
    msg = f"Pod and Service created by Database {name}"
    return {'message': msg}

# Deleted trigger object handler
@kopf.on.delete('zalando.org', 'v1', 'databases')
def delete(body, **kwargs):
    msg = f"Database {body['metadata']['name']} and its Pod / Service children deleted"
    return {'message': msg}