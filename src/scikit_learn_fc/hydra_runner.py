"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/using_scikit_learn.html#configuring-and-building-an-experiment

set up CLI to used defined classifiers, datasets, and task function

run in CLI with
$ python src\scikit_learn_fc\hydra_runner.py
to use default options

to run with desired overrides
$ python src\scikit_learn_fc\hydra_runner.py "dataset=circles" "classifier=decision_tree"

to run all experiments use
$ python src\scikit_learn_fc\hydra_runner.py "dataset=glob(*)" "classifier=glob(*)" --multirun

"""

import add_classifiers_to_store
import add_datasets_to_store
from hydra_zen import make_config, store

# Define and save all classifiers of interest to the local hydra-zen store
add_classifiers_to_store.all_classifiers()

# Define and save all datasets of interest to the local hydra-zen store
add_datasets_to_store.all_datasets()

# Task configuration:
#    Set the default dataset to be `moons`
#    and the default classifier to be `knn`
store(
    make_config(
        hydra_defaults=["_self_", {"dataset": "moons"}, {"classifier": "knn"}],
        dataset=None,
        classifier=None,
    ),
    name="config",
)


if __name__ == "__main__":
    from hydra_zen import zen
    from hydra.conf import HydraConf, JobConf
    from train_models import task
    # Configure Hydra to change the working dir to match that of the output dir
    store(HydraConf(job=JobConf(chdir=True)), name="config", group="hydra")

    # Add all of the configs, that we put in hydra-zen's (local) config store,
    # to Hydra's (global) config store.
    store.add_to_hydra_store(overwrite_ok=True)

    # Use `zen()` to convert our Hydra-agnostic task function into one that is
    # compatible with Hydra.
    # Use `.hydra_main(...)` to generate the Hydra-compatible CLI for our program.
    zen(task).hydra_main(config_path=None, config_name="config", version_base="1.2")