import json
from pathlib import Path

test_configs = Path(__file__).parent / "configurations"
test_configs.mkdir(exist_ok=True)

with (open(test_configs.joinpath("prod.ini"), mode='w') as prod,
      open(test_configs.joinpath("dev.ini"), mode='w') as dev):
    
    prod.write("[Database]\n")
    prod.write("db_host=prod.mynetwork.com\n")
    prod.write("db_port=5432\n")
    prod.write("user=localhost\n")
    prod.write("[Server]\n")
    prod.write("port=8080\n")

    dev.write("[Globals]\n")
    dev.write("username=ioannis\n")
    dev.write("[Database]\n")
    dev.write("db_host=dev.mynetwork.com\n")
    dev.write("db_port=5432\n")
    dev.write("user=localhost\n")
    dev.write("[Server]\n")
    dev.write("port=3000\n")

prod_dict = {"Database": {
                          'db_host': 'prod.mynetwork.com',
                          'db_port': 5432,
                          'user': 'localhost',
                         },
             "Server": {'port': 8080}
             }

dev_dict = {"Database": {
                         'db_host': 'dev.mynetwork.com',
                         'db_port': 5432,
                         'user': 'localhost',
                         },
            "Server": {'port': 3000},
            "Globals": {"username": "ioannis"}
            }


json.dump(obj=prod_dict,
          fp=open(test_configs.joinpath("prod.json"), "w"),
          indent=4
          )

json.dump(obj=dev_dict,
          fp=open(test_configs.joinpath("dev.json"), "w"),
          indent=4
          )


