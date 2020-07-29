from config import TRIGGERS_STORE_FILENAME, TRIGGERS_STORE_PVC_NAME
from utils.exceptions import MissingTriggerStore

# Marshalling of k8s trigger object(s)
def marshall_trigger(trigger):
    return (trigger['spec']['topic'], trigger['spec']['functionSelector']['matchlabels']['function'])


# Remove a trigger from a provided store
def remove_trigger_store(trigger_topic, store):
    try:
        store.pop(trigger_topic)
        return store
    except KeyError:
        raise MissingTriggerStore(f'Missing trigger (topic {trigger_topic}) in provided store')
