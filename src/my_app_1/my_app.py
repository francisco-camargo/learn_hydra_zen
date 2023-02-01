"""
following this specific section where we use hydra_zen.zen()
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/basic_app.html#simplifying-things-with-hydra-zen-zen
    
    We now what to be able to write the task function without having to say anything about hydra or hydra-zen in the function definition.
    So we are going to do two things:
        use hydra_zen.builds() instead of hydra_zen.make_config() to make the configuration
        use hydra_zen.zen() in order to convert our task function into a Hydra-compatible task function
            unlike the task function that accepts two strings, the zen() wrapped function accepts a single input config (just like the original task function in /src/my_app_0/my_app.py)
    
    input: two player names
    output: log names in player_log.txt file
"""

from hydra_zen import builds

def new_task_function(player1, player2):
    # write the log with the names
    with open("player_log.txt", "w") as f:
        f.write("Game session log:\n")
        f.write(f"Player 1: {player1}\n" f"Player 2: {player2}")

    return player1, player2

# auto-populates the fields of our configs based on the signature of `new_task_function`
    # this results in the corresponding config.yaml having
    # _target_: __main__.new_task_function
    # in the first line now
    
Config = builds(new_task_function, populate_full_signature=True)


if __name__ == '__main__':
    # from my_app import Config, new_task_function
    from hydra_zen import zen, launch
    wrapped_fn = zen(new_task_function)
    job = launch(Config, wrapped_fn, overrides=["player1=link", "player2=zelda"], version_base="1.1")
    
    print(job.status) # status of code execution
    print(job.return_value) # outputs from task function

    from pathlib import Path
    # inspect where the outputs were saved to
    job_dir = Path(job.working_dir)  # type: ignore
    print(job_dir)  # output will vary based on reader's date/time/OS

    # access the outputs by reading in the output file
    import file_inspect
    file_inspect.print_file(job_dir / 'player_log.txt')