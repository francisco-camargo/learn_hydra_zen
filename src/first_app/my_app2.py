"""
following the following hydro-zen tutorial:
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/basic_app.html

"""

from hydra_zen import builds

def new_task_function(player1, player2): # this task function is better than the one in my_app.py because it doesn't know anything about the hydra-zen library
    # write the log with the names
    with open("player_log.txt", "w") as f:
        f.write("Game session log:\n")
        f.write(f"Player 1: {player1}\n" f"Player 2: {player2}")

    return player1, player2

# auto-populates the fields of our configs based on the signature of
# `task_function`
Config = builds(new_task_function, populate_full_signature=True) # using builds() is better than how Config was defined in my_app.py because it doesn't require specifying the config fields of interest explicitly



if __name__ == '__main__':
    from hydra_zen import zen, launch

    wrapped_fn = zen(new_task_function)
    job = launch(Config, wrapped_fn, overrides=["player1=link", "player2=zelda"], version_base="1.1")