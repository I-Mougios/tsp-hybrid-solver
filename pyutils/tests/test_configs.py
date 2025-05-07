from pathlib import Path
import sys
base = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(base))
from pyutils import ConfigMeta

config_directory = base / 'pyutils' / 'configurations'
class DevConfig(metaclass=ConfigMeta,
                config_directory= config_directory,
                config_filename='dev.ini'):
    """
    Configuration of Development Environment
    """

print(DevConfig.database.db_host)
print(DevConfig.globals.username)
print(DevConfig.database.get('username'))
print(DevConfig.server.get('missing', 'Default'))

# get = DevConfig.server.get

# print(get.__closure__)

class DevConfig(metaclass=ConfigMeta,
                config_directory= config_directory,
                config_filename='dev.json'):
    """
    Configuration of Development Environment
    """

print(DevConfig.database.db_host)
print(DevConfig.globals.username)
print(DevConfig.database.get('username'))
print(DevConfig.server.get('missing', 'Default'))
