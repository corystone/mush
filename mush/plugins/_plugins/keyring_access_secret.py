import os
import keyring
from mush.config import config
from mush.plugins import interfaces

class access_secret(interfaces.access_secret):
    __keyname__="keyring"

    def __call__(self, environment_variables):
        magic_prefix = config.get("access_secret.keyring", "magic_prefix")
        service_name = config.get("access_secret.keyring", "service")
        for key, val in environment_variables.iteritems():
            if val.startswith(magic_prefix):
                keyring_key = val.replace(magic_prefix, '')
                keyring_val = None
                try:
                    keyring_val = keyring.get_password(
                        service_name, keyring_key)
                except exception as e:
                    print e
                    environment_variables[key] = val
                environment_variables[key] = keyring_val
        return environment_variables
