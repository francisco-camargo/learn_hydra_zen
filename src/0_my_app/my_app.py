"""
following top section of
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/basic_app.html
    (everything before https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/basic_app.html#simplifying-things-with-hydra-zen-zen)
    
    input: two player names
    output: log names in player_log.txt file
"""

from hydra_zen import make_config, instantiate

# A config, which defines the configurable interface of our application
    # This defines the structure of the config, not a specific configuration of values (I think)
Config = make_config("player1", "player2")


def task_function(cfg):
    """
    A task function, which accepts the populated config,
    and whose body specifies the code that will be
    executed when our application is launched
    
    input: a config object
    output: player names, derived from looking at attributes of instantiate(cfg)
    """
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


if __name__ == '__main__':
    # # handle the working directory
    # from hydra.conf import HydraConf, JobConf
    # from hydra_zen import store
    # store(HydraConf(job=JobConf(chdir=True)))
        # couldn't figure out how to get this to work in tandem with launch() such that I can use version_base='1.2'
    
    # from my_app import Config, task_function
        # have Config and task_function() on-hand
        
    from hydra_zen import launch
        # use launch to run our application
        # pass our config, task function, and SPECIFIC values for player names
    job = launch(Config, task_function, overrides=["player1=link", "player2=zelda"], version_base="1.1")
        # if I use version 1.1
            # player_log.txt is saved in the corresponding /outputs/ folder
        # if I use version 1.2
            # player_log.txt is saved directly in the parent directory
        # overrides is how we controlled the specific values to use for certain fields in the config
            # this info will get saved to /outputs/*/*/.hydra/config.yaml
    print(job.status) # status of code execution
    print(job.return_value) # outputs from task function

    from pathlib import Path
    # inspect where the outputs were saved to
    job_dir = Path(job.working_dir)  # type: ignore
    print(job_dir)  # output will vary based on reader's date/time/OS

    # access the outputs by reading in the output file
    import file_inspect
    file_inspect.print_file(job_dir / 'player_log.txt')