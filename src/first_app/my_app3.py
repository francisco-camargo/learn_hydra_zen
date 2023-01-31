"""
following the following hydro-zen tutorial:
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/add_cli.html

Now going to add CLI functionality

Ex. how to run this in the command line
    $ python my_app3.py player1=mario player2=luigi

"""

from hydra_zen import store, zen

# 1) `hydra_zen.store generates a config for our task function
#    and stores it locally under the entry-name "my_app"
@store(name="my_app3")
def task_function(player1, player2):
    # write the log with the names
    with open("player_log.txt", "w") as f:
        f.write("Game session log:\n")
        f.write(f"Player 1: {player1}\n" f"Player 2: {player2}")

    return player1, player2

# 2) Executing `python my_app3.py [...]` will run our task function
if __name__ == "__main__":
    # 3) We need to add the configs from our local store to Hydra's
    #    global config store
    store.add_to_hydra_store()

    # 4) Our zen-wrapped task function is used to generate
    #    the CLI, and to specify which config we want to use
    #    to configure the app by default
    zen(task_function).hydra_main(config_name="my_app3",
                                  version_base="1.1",
                                  config_path=None,
                                  )