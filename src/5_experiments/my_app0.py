"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/configuring_experiments.html
    
run in CLI with
    python src/5_experiments/my_app0.py
    
    run "aplite" experiment
    python src/5_experiments/my_app0.py db=sqlite server.port=8080
    
    run "nglite" experiment
    python src/5_experiments/my_app0.py db=sqlite server=nginx server.port=8080
    
    To run from previous config.yaml file
    $ python my_app.py -cp outputs\2023-02-10\12-03-55\.hydra -cn config
    or if I want to have a "special" config.yaml that I play with just under the parent directory
    $ python my_app.py -cp ./ -cn config
    Note: seems like I need to set hydra_main(config_path= to have ANY string value, doesn't matter what in order to get this to work
        but I think using config_path="." allows me to run the app when I don't want to change the config_path in the CLI via -cp
    Note: the config_path that you need to specify is relative to the location of where this file (my_app0.py), which holds the hydra_main() call, is located
        so write the relative path that takes you from the hydra_main() file to the folder that holds the config.yaml file of interest
    eg. if myconfig.yaml is right under the parent directory, and you want to use this script which is under ./src/5_experiments, then run
        $ python src/5_experiments/my_app0.py -cp ../../ -cn myconfig
    eg. if exp_config.yaml is in same folder as app code
        $ python src/5_experiments/my_app0.py -cp ./ -cn exp_config


"""

from dataclasses import dataclass

from hydra_zen import store, zen, builds

# 1. Creating and storing basic configs

@dataclass
class Server:
    name: str
    port: int


@dataclass
class Database:
    name: str

# For convenience:
# Tell the store to automatically infer the entry-name from
# the config's `.name` attribute.
auto_name_store = store(name=lambda cfg: cfg.name)

# Pre-set the group for store's db entries
db_store = auto_name_store(group="db")

db_store(Database(name="mysql"))
db_store(Database(name="sqlite"))

# Pre-set the group for store's server entries
server_store = auto_name_store(group="server")

server_store(Server(name="apache", port=80))
server_store(Server(name="nginx", port=80))


# 2. Defining our app's task function and the top-level config
def task(db: Database, server: Server):
    from hydra_zen import to_yaml

    print(f"db:\n{to_yaml(db)}")
    print(f"server:\n{to_yaml(server)}")


# The 'top-level' config for our app w/ a specified default
# database and server
Config = builds(
    task,
    populate_full_signature=True,
    hydra_defaults=["_self_", {"db": "mysql"}, {"server": "apache"}],
)

store(Config, name="config")

if __name__ == "__main__":
    store.add_to_hydra_store()
    zen(task).hydra_main(config_path=".", config_name="config", version_base="1.2")
