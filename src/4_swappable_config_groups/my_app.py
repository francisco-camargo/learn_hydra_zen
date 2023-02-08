"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/config_groups.html
    
    
Run from CLI examples:
    $ python src\4_swappable_config_groups\my_app.py player.name=ivy
    $ python src\4_swappable_config_groups\my_app.py player.name=ivy +player/inventory=hard_mode
    $ python src\4_swappable_config_groups\my_app.py player.name=ivy player.level=3 +player/inventory=hard_mode player.inventory.gold=10
    $ python src\4_swappable_config_groups\my_app.py player=rakesh
    $ python src\4_swappable_config_groups\my_app.py player=brinda player.inventory.costume=armor
    
Noticing that '+' is used whenever we want to use a subgroup definition; e.g. +player/inventory=
"""

from hydra_zen import store, make_custom_builds_fn, zen

from game_library import inventory, Character

builds = make_custom_builds_fn(populate_full_signature=True)

########################################################
# Create inventory configs
InventoryConf = builds(inventory)
starter_gear = InventoryConf(gold=10, weapon="stick", costume="tunic")
advanced_gear = InventoryConf(gold=500, weapon="wand", costume="magic robe")
hard_mode_gear = InventoryConf(gold=0, weapon="inner thoughts", costume="rags")

# Register inventory configs under group: player/inventory
inv_store = store(group="player/inventory")

inv_store(starter_gear, name="starter")
inv_store(advanced_gear, name="advanced")
inv_store(hard_mode_gear, name="hard_mode")

########################################################
# Create player-profile configs
CharConf = builds(Character, inventory=starter_gear)

brinda_conf = CharConf(
    name="brinda",
    level=47,
    inventory=InventoryConf(costume="cape", weapon="flute", gold=52),
)

rakesh_conf = CharConf(
    name="rakesh",
    level=300,
    inventory=InventoryConf(costume="PJs", weapon="pillow", gold=41),
)

# Register player-profile configs under group: player
player_store = store(group="player")

player_store(CharConf, name="base")
player_store(brinda_conf, name="brinda")
player_store(rakesh_conf, name="rakesh")


########################################################
# The `hydra_defaults` field is specified in our task function's config.
# It instructs Hydra to use the player config that named 'base' in our
# config store as the default config for our app.
# @store(name="my_app",  hydra_defaults=["_self_", {"player": "base"}])
def task_function(player: Character):

    print(player)

    with open("player_log.txt", "a") as f:
        f.write("Game session log:\n")
        f.write(f"Player: {player}\n")

    return player

from hydra_zen import make_config
store(
    make_config(
        hydra_defaults=["_self_", {"player": "base"}],
        player=None,
    ),
    name="my_app",
)

if __name__ == "__main__":
    # We need to add the configs from our local store to Hydra's
    # global config store
    store.add_to_hydra_store()

    # Our zen-wrapped task function is used to generate
    # the CLI, and to specify which config we want to use
    # to configure the app by default
    zen(task_function).hydra_main(config_name="my_app",
                                  version_base="1.1",
                                  config_path=".",
                                  )