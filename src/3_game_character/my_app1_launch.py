"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/hierarchy.html
    
Here I have tried to implement the simplest hydra-zen wrapper for the game_library
"""

from hydra_zen import zen, builds, make_config
from game_library import inventory, Character

# Task function
def task_function(player: Character):
    print(player)
    with open("player_log.txt", "a") as f:
        f.write("Game session log:\n")
        f.write(f"Player: {player}\n")
    return player

# Inventory config
starter_gear = builds(inventory, gold=10, weapon="stick", costume="tunic")

# Character config
CharConf = builds(Character, inventory=starter_gear, populate_full_signature=True)

# Build config compatible with zen(task_function), with desired default values coming from CharConf
    # Have two options on how to do this; by inferring the config by looking at the task_function
    # or by making the config explicitly
option = 'a'
if option=='a':
    NewConfig = builds(task_function, player=CharConf)
elif option=='b':
    NewConfig = make_config(player=CharConf)


if __name__ == "__main__":
    from hydra_zen import launch
    job = launch(
        NewConfig,
        zen(task_function),
        overrides=["player.name=sam"],
        version_base='1.1'
    )