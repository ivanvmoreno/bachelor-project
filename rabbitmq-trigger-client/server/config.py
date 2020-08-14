from os import getenv

# Target directory of the frontend application build
FRONTEND_BUILD_DIR = getenv('FRONTEND_BUILD_DIR')

# Namespace where kubeless is deployed
KUBELESS_NAMESPACE = getenv('KUBELESS_NAMESPACE')

# k8s object type name for kubeless functions
KUBELESS_FN_PLURAL = getenv('KUBELESS_FN_PLURAL')

# k8s group for kubeless functions
KUBELESS_GROUP = getenv('KUBELESS_GROUP')

# k8s custom resource version for kubeless functions
KUBELESS_FN_VERSION = getenv('KUBELESS_FN_VERSION')

# Group of the trigger CRD
TRIGGERS_GROUP = getenv('TRIGGERS_GROUP')

# k8s ApiVersion of the trigger CRD
TRIGGERS_VERSION = getenv('TRIGGERS_VERSION')

# Plural name of the trigger CRD
TRIGGERS_PLURAL = getenv('TRIGGERS_PLURAL')
