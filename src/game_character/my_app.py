"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/hierarchy.html
    
In this tutorial we will design an application that has an interface that is hierarchical in nature.
This particular application will describe a player in a video game; this player has a configurable 
name and experience-level, as well as an inventory, which itself has configurable components.

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
    # zen(task_function).hydra_main(config_name="my_app",
    #                               version_base="1.1",
    #                               config_path=".",
    #                               )

    wrapped_fn = zen(task_function)#.hydra_main(config_name="my_app", version_base="1.1",config_path=".")
    from hydra_zen import launch
    job = launch(CharConf, wrapped_fn, overrides=["player.name=frodo"], version_base="1.1")

# from game_library import inventory, Character

# # from hydra_zen import make_custom_builds_fn
# # builds = make_custom_builds_fn(populate_full_signature=False)

# # generating configs
# from hydra_zen import make_custom_builds_fn, builds
# starter_gear = builds(inventory, gold=10, weapon="stick", costume="tunic", populate_full_signature=True)
# CharConf = builds(Character, inventory=starter_gear)

# # Generate and store a top-level config specifying `CharConf` as the
# # default config for `player`
# from hydra_zen import store
# @store(name="my_app", player=CharConf)
# def task_function(player: Character):

#     print(player)

#     with open("player_log.txt", "a") as f:
#         f.write("Game session log:\n")
#         f.write(f"Player: {player}\n")

#     return player
