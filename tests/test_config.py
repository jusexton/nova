import pytest

from nova import config


@pytest.fixture
def env() -> dict:
    return {
        'CONNECTION_STRING': 'connect'
    }


def test_env_var_is_retrieved_correctly(env: dict):
    environment_variable = config.env_var('CONNECTION_STRING', environment=env)

    assert environment_variable == 'connect'


def test_env_var_returns_default_when_variable_is_missing(env):
    default = 'default'
    environment_variable = config.env_var('does not exist', default=default, environment=env)

    assert environment_variable == default


def test_env_var_raises_error_when_variable_does_not_exist(env):
    missing_variable = 'does not exist'
    with pytest.raises(config.MissingEnvironmentVariableError) as exception_info:
        config.env_var(missing_variable, environment=env)

        exception = exception_info.value
        assert exception.env_var_name == missing_variable
        assert str(exception) == f'An environment variable with the name: {missing_variable} could not be found.'
