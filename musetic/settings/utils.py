import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, default=None):
    """
    Verifies that the requested environment variable is present or a 
    default is provided.
    """

    try:
        value = os.environ[var_name]
        if default is not None:
            value = default
        return value
    except KeyError:
        if default is None:
            error_msg = "Set the %s env variable" % var_name
            raise ImproperlyConfigured(error_msg)
        else:
            return default
