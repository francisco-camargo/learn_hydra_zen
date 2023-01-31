"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/add_cli.html
    
code to look at outputs of my_app 

"""

from pathlib import Path

# find the latest job run using hydra-zen
*_, latest_job = sorted((Path.cwd() / "outputs").glob("*/*")) # this is looking in VSCode's Explorer cwd(), not the VSCode terminal's cwd()
print(latest_job)  # changes based  on reader's date, time, and OS

def print_file(x: Path):
    with x.open("r") as f:
        print(f.read())

# get the contents of the latest job run using hydra-zen
print_file(latest_job / "player_log.txt")