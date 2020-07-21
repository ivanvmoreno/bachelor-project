import json
from pathlib import Path
from config import CLUSTER_FQDN, TRIGGERS_FILENAME, TRIGGERS_VOLUME_PATH

# { topic: [funA, funB] }
# Read triggrs from the global store
def read_triggers():
    content = Path(f'{TRIGGERS_VOLUME_PATH}/{TRIGGERS_FILENAME}').read_text()
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
    return f'{fn_name}.{CLUSTER_FQDN}'
