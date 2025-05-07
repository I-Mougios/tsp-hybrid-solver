import sys
from pathlib import Path
root = Path(__file__).parents[1]
sys.path.append(str(root))
from pyutils import ConfigMeta


configs_dir = root / 'configs'
config_filename = "configs.ini"


class Configs(metaclass=ConfigMeta,
             config_directory=configs_dir,
             config_filename=config_filename):
    """
    Configurations about:
        - Hyperparamters during training
        - Connection to MongoDB in order to create the TSPDataset
        - Paths where the training logs and predictions will be stored
    """

if __name__ == '__main__':
    print(Configs.model.get("hidden_dim", cast=int))
    print(Configs.mongodb.username)