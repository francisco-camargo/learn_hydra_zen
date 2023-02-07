"""
following:
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/add_cli.html
    
Want to add a Command Line Interface (CLI) to the application
Run app by running
$ python my_app.py player1=name1 player2=name2
Where we can replace name1 and name2 with any string values
Notice that we did not use quotes in this instance

"""

from hydra_zen import store, zen

# 1) `hydra_zen.store generates a config for our task function
#    and stores it locally under the entry-name "my_app"
# The decorator adds the 'my_app' config to the local store
# Note that the task function is still written without reference
# to hydra_zen
@store(name="my_app")
def task_function(player1, player2):
    # write the log with the names
    with open("player_log.txt", "w") as f:
        f.write("Game session log:\n")
        f.write(f"Player 1: {player1}\n" f"Player 2: {player2}")

    return player1, player2

# 2) Executing `python my_app.py [...]` will run our task function
if __name__ == "__main__":
    # 3) We need to add the configs from our local store to Hydra's
    #    global config store
    store.add_to_hydra_store()

    # 4) Our zen-wrapped task function is used to generate
    #    the CLI, and to specify which config we want to use
    #    to configure the app by default
    zen(task_function).hydra_main(config_name="my_app",
                                  version_base="1.1",
                                  config_path=None,
                                  )