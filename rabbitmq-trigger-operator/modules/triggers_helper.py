from config import TRIGGERS_STORE_FILENAME, TRIGGERS_STORE_PVC_NAME

# Marshalling of k8s trigger object(s)
def marshall_trigger(trigger):
    return (trigger['spec']['topic'], trigger['spec']['functionSelector']['matchlabels']['function'])
    

# def update_store():
    


# def initialize_store():
    