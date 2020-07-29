from flask import Flask, render_template
import kubernetes

import config
import utils.yaml_helper

app = Flask(__name__, static_url_path='', static_folder=config.FRONTEND_BUILD_DIR, template_folder=config.FRONTEND_BUILD_DIR)

# Initialize k8s client
kubernetes.config.load_incluster_config()
api = kubernetes.client.CustomObjectsApi()

# Serve frontend application
@app.route('/')
def serve_frontend():
    return render_template('index.html')


# Lists all kubeless functions in the cluster
@app.route('/functions', methods=['GET'])
def list_functions(functions):
    # List all kubeless functions in the namespace
    functions = api.list_namespaced_custom_object(
            config.KUBELESS_FUNCTION_GROUP,
            config.KUBELESS_FUNCTION_VERSION,
            config.KUBELESS_NAMESPACE, 
            config.KUBELESS_FUNCTION_PLURAL)
    
    query = request.args.get('search')

    if query:
        # Filter functions by name against regular expression
        regex = re.compile(f'^{query}.*')
        filtered = [fn['metadata']['name'] for fn in functions if regex.match(fn['metadata']['name'])]
    else:
        limit = request.args.get('limit') or 15
        page = request.args.get('page') or 0

        filtered = [fn['metadata']['name'] for fn in functions[page*limit:page*limit+limit-1]]

    return make_response(filtered, 200) if len(filtered) else flask.Response(status=404)


# Returns RabbitMQTrigger objects for a particular kubeless function
@app.route('/functions/<function>/amqp-triggers', methods=['GET'])
def list_function_triggers(function):
    # List all RabbitMQTriggers in the namespace
    triggers = api.list_namespaced_custom_object(
            config.TRIGGER_OBJECT_GROUP,
            config.TRIGGER_OBJECT_VERSION,
            config.KUBELESS_NAMESPACE,
            config.TRIGGER_OBJECT_PLURAL)

    # Filter triggers by subject function
    filtered = [t['metadata']['name'] for t in triggers if t['functionSelector']['matchLabels']['function'] == function]

    return make_response(filtered, 200) if len(filtered) else flask.Response(status=404)


# Creates a new RabbitMQTrigger object
@app.route('/functions/<function>/amqp-triggers', methods=['POST'])
def create_function_trigger(function):
    try:
        req_body = request.json()

        # Load RabbitMQTrigger object model
        object_template = read_file('/models/rabbitmqtrigger.yaml')
        
        # Format model with received information, and convert to JSON
        body = yaml_to_json(format_string(object_template, req_body['name'], function, req_body['topic']))

        # Create RabbitMQTrigger in k8s
        api.create_namespaced_custom_object(
            config.TRIGGER_OBJECT_GROUP,
            config.TRIGGER_OBJECT_VERSION,
            config.KUBELESS_NAMESPACE,
            config.TRIGGER_OBJECT_PLURAL,
            body)

        return flask.Response(status=200)
    except ApiException as e:
        print(f'Error creating RabbitMQTrigger object\n{e}')
        return flask.Response(status=500)


# Deletes a RabbitMQTrigger object
@app.route('/triggers/<trigger>', methods=['DELETE'])
def delete_function_trigger(trigger):
    try:
        # Delete RabbitMQTrigger in k8s
        api.create_namespaced_custom_object(
            config.TRIGGER_OBJECT_GROUP,
            config.TRIGGER_OBJECT_VERSION,
            config.KUBELESS_NAMESPACE,
            config.TRIGGER_OBJECT_PLURAL,
            trigger)
        
        return flask.Response(status=200)
    except ApiException as e:
        print(f'Error deleting RabbitMQTrigger object\n{e}')
        return flask.Response(status=500)

if __name__ == '__main__':
    app.run()
