"""
following the following hydro-zen tutorial:
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/basic_app.html

"""

from hydra_zen import make_config, instantiate


def task_function(cfg):
    # cfg: Config
    obj = instantiate(cfg)

    # access the player names from the config
    p1 = obj.player1
    p2 = obj.player2

    # write the log with the names
    with open("player_log.txt", "w") as f:
        f.write("Game session log:\n")
        f.write(f"Player 1: {p1}\n" f"Player 2: {p2}")

    return p1, p2


Config = make_config("player1", "player2")


if __name__ == '__main__':
    from hydra_zen import launch
    job = launch(Config, task_function, overrides=['player1=link', 'player2=zelda'], version_base='1.1')
    print(job.status)
    print(job.return_value)