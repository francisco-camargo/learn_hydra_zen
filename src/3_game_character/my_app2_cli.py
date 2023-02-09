"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/hierarchy.html
    
In this tutorial we will design an application that has an interface that is hierarchical in nature.
This particular application will describe a player in a video game; this player has a configurable 
name and experience-level, as well as an inventory, which itself has configurable components.

CLI
$ python src/3_game_character/my_app2_cli.py player.name=frodo
$ python src/3_game_character/my_app2_cli.py player.name=frodo player.level=5
$ python src/3_game_character/my_app2_cli.py player.name=frodo player.level=2 player.inventory.costume=robe

"""

from hydra_zen import store, zen, builds, make_config
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
    # Use auto-config feature of store
store(
    Character,
    inventory=starter_gear,
    populate_full_signature=True,
    group="player",
    name="base",
)

# Add top-level config to store
store(
    make_config(
        hydra_defaults=["_self_", {"player":"base"}],
        player=None,
    ),
    name="my_app",
)


if __name__ == "__main__":
    store.add_to_hydra_store()
    zen(task_function).hydra_main(config_name="my_app",
                                  version_base="1.1",
                                  config_path=".",
                                  )
