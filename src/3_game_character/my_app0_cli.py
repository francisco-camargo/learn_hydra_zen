"""
emulate
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/hierarchy.html#id7

CLI
$ python src/3_game_character/my_app0.py player.name=frodo
$ python src/3_game_character/my_app0.py player.name=frodo player.level=5
$ python src/3_game_character/my_app0.py player.name=frodo player.level=2 player.inventory.costume=robe

"""

from hydra_zen import make_custom_builds_fn, store, zen

from game_library import inventory, Character

builds = make_custom_builds_fn(populate_full_signature=True)

# generating configs
starter_gear = builds(inventory, gold=10, weapon="stick", costume="tunic")

CharConf = builds(Character, inventory=starter_gear)

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