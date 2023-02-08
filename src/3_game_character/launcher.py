"""
write code to launch the hydra-zen wrapped version of game_library.py

if instead we want to use the CLI

Ex1
$ python my_app.py player.name=frodo
frodo, lvl: 1, has: {'gold': 10, 'weapon': 'stick', 'costume': 'tunic'}

Ex2
$ python my_app.py player.name=frodo player.level=5
frodo, lvl: 5, has: {'gold': 10, 'weapon': 'stick', 'costume': 'tunic'}

Ex3
$ python my_app.py player.name=frodo player.level=2 player.inventory.costume=robe
frodo, lvl: 2, has: {'gold': 10, 'weapon': 'stick', 'costume': 'robe'}

"""

# TODO: broken at the moment

from hydra_zen import launch, zen
from my_app import task_function
from my_app import CharConf
job = launch(
    CharConf,
    zen(task_function),
    overrides=["player.name=frodo"],
    version_base='1.1'
)
# frodo, lvl: 2, has: {'gold': 10, 'weapon': 'stick', 'costume': 'robe'}