"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/hierarchy.html
    
In this tutorial we will design an application that has an interface that is hierarchical in nature.
This particular application will describe a player in a video game; this player has a configurable 
name and experience-level, as well as an inventory, which itself has configurable components.

"""

# Note: type annotations are *not* required by hydra-zen

__all__ = ["inventory", "Character"]


class Character:
    def __init__(self, name: str, level: int = 1, inventory=None):
        self.name = name
        self.level = level
        self.inventory = inventory

    def __repr__(self):
        out = ""
        out += f"{self.name}, "
        out += f"lvl: {self.level}, "
        out += f"has: {self.inventory}"
        return out


def inventory(gold: int, weapon: str, costume: str):
    return {"gold": gold, "weapon": weapon, "costume": costume}

# if __name__ == '__main__':
#     stuff = inventory(gold=12, weapon="stick", costume="bball jersey")
#     bowser = Character("bowser", inventory=stuff)
#     print(bowser)
    
#     peach = Character("peach")
#     print(peach)
    