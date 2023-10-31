import os
from typing import Final

import pydantic
import toml
from pydantic import ConfigDict

NOVA_TOKEN: Final[str] = 'NOVA_TOKEN'
NOVA_CONFIG_PATH: Final[str] = '/app/nova.toml'


class MissingEnvironmentVariableError(Exception):
    """
    Error raised when an environment variable could not be found in the configured environment.
    """

    def __init__(self, env_var_name: str):
        self.env_var_name = env_var_name

    def __str__(self):
        return f'An environment variable with the name: {self.env_var_name} could not be found.'


def env_var(name: str, default: str = None, environment=os.environ) -> str:
    """
    Retrieves a specified environment variable. A default value can be provided in the case the value could
    not be found. Otherwise, an exception is raised detailing that the variable could not be retrieved.

    :param name: The name of the environment variable to retrieve
    :param default: The value that will be used if no environment variable could be found.
    :param environment: Reference to the environment. By default, the os environment is used.
    :return: The value of the env var.
    :raises MissingEnvironmentVariableError: Raised when an env var with the given name does not exist and no default
    was provided.
    """

    try:
        return environment[name]
    except KeyError:
        if default is None:
            raise MissingEnvironmentVariableError(name)
        return default


class NovaExtension(pydantic.BaseModel):
    model_config = ConfigDict(extra='allow')

    name: str


class NovaConfiguration(pydantic.BaseModel):
    """
    Represents any configuration data will require throughout it's execution.
    """

    token: str
    extensions: list[str | NovaExtension] = []


def load() -> NovaConfiguration:
    """
    Attempts to load nova configuration from either an excepted toml file or environment variables.
    The nova.toml file will take precedence over any environment variables.
    """

    return from_toml() if os.path.exists(NOVA_CONFIG_PATH) else from_env()


def from_env() -> NovaConfiguration:
    token = env_var(NOVA_TOKEN)
    return NovaConfiguration(token=token)


def from_toml(path: str = NOVA_CONFIG_PATH) -> NovaConfiguration:
    toml_dict = toml.loads(path)
    return NovaConfiguration(**toml_dict)
