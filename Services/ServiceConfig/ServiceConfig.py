"""Get configuration for the service.

Object contains basic configuration info line: API key
"""
import json


class ServiceConfig():
    """Get configuration for the service.

    :param api_key: api key to the service
    :api_key type: str
    """

    def __init__(self, api_key=None) -> None:
        """Create an instance."""
        self.api_key = None if not api_key else api_key

    @classmethod
    def _read_con_file(cls, json_file) -> str:
        """Open config file.

        :param json_file: path to the service config file
        :param type: str, json
        :return: config file content, None if file does not exist
        :rtype: str, json
        """
        try:
            with open(json_file, 'r') as file:
                config = json.load(file)

        except FileNotFoundError:
            config = None

        except json.JSONDecodeError:
            config = None

        finally:
            return config

    @classmethod
    def create(cls, json_file: str):
        """Create an instance of the `ServiceConfig`.

        :param json_file: path to the json config file
        :json_file type: str
        :return: an instance of `ServiceConfig`
        :rtype: `ServiceConfig` or None
        """
        config = cls._read_con_file(json_file)
        api_key = None
        if config:
            api_key = config.get("api_key", None)
            return cls(api_key=api_key)
        else:
            return None
