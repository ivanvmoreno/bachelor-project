from os import getenv

# Target directory of the frontend application build
FRONTEND_BUILD_DIR = getenv('FRONTEND_BUILD_DIR')

# Namespace where kubeless is deployed
KUBELESS_NAMESPACE = getenv('KUBELESS_NAMESPACE')

# k8s object type name for kubeless functions
KUBELESS_FUNCTION_PLURAL = getenv('KUBELESS_FUNCTION_PLURAL')

# k8s group for kubeless functions
KUBELESS_FUNCTION_GROUP = getenv('KUBELESS_FUNCTION_GROUP')

# k8s custom resource version for kubeless functions
KUBELESS_FUNCTION_VERSION = getenv('KUBELESS_FUNCTION_VERSION')

# Group of the trigger CRD
TRIGGER_OBJECT_GROUP = getenv('TRIGGER_OBJECT_GROUP')

# k8s ApiVersion of the trigger CRD
TRIGGER_OBJECT_VERSION = getenv('TRIGGER_OBJECT_VERSION')

# Plural name of the trigger CRD
TRIGGER_OBJECT_PLURAL = getenv('TRIGGER_OBJECT_PLURAL')
