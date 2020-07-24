import yaml
from pathlib import Path

# Read contents from a file
def read_file(file_path):
    return Path(file_path).read_text()


# Formats a string with the provided parameters
def format_string(string, *args):
    return string.format(*args)


# Converts a yaml-structured string to a json string
def yaml_to_json(yaml):
    return yaml.load(yaml)
