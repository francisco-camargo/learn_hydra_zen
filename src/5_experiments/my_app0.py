"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/configuring_experiments.html
    
run in CLI with
    python src/5_experiments/my_app0.py
    
    run "aplite" experiment
    python src/5_experiments/my_app0.py db=sqlite server.port=8080
    
    run "nglite" experiment
    python src/5_experiments/my_app0.py db=sqlite server=nginx server.port=8080
    
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
    zen(task).hydra_main(config_path=None, config_name="config", version_base="1.2")
