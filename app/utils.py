import yaml


def load_constants_from_yaml(file_path):
    with open(file_path, "r") as stream:
        try:
            return yaml.safe_load(stream).get("constants", {})
        except yaml.YAMLError as exc:
            print(exc)
