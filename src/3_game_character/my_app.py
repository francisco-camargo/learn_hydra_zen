"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/hierarchy.html
    
In this tutorial we will design an application that has an interface that is hierarchical in nature.
This particular application will describe a player in a video game; this player has a configurable 
name and experience-level, as well as an inventory, which itself has configurable components.

CLI
$ python src/3_game_character/my_app.py player.name=frodo
$ python src/3_game_character/my_app.py player.name=frodo player.level=5
$ python src/3_game_character/my_app.py player.name=frodo player.level=2 player.inventory.costume=robe

"""

from hydra_zen import store, zen, builds, make_config
from game_library import inventory, Character

# Inventory config
starter_gear = builds(inventory, gold=10, weapon="stick", costume="tunic")

# Character config
CharConf = builds(Character, inventory=starter_gear, populate_full_signature=True)
    # need populate_full_signature=True because Character is an Class... I think
    # think it was not needed for inventory because inventory is a dictionary

# Generate and store a top-level config specifying `CharConf` as the
# default config for `player`
@store(name="my_app", player=CharConf)
def task_function(player: Character):

    print(player)

    with open("player_log.txt", "a") as f:
        f.write("Game session log:\n")
        f.write(f"Player: {player}\n")

    return player


if __name__ == "__main__":
    store.add_to_hydra_store()
    zen(task_function).hydra_main(config_name="my_app",
                                  version_base="1.1",
                                  config_path=".",
                                  )

    # from hydra_zen import launch, zen
    # from my_app import task_function
    # from my_app import CharConf
    # # store.add_to_hydra_store(overwrite_ok=True)
    # job = launch(
    #     CharConf,
    #     zen(task_function),
    #     overrides=["player.name=frodo"],
    #     version_base='1.1'
    # )