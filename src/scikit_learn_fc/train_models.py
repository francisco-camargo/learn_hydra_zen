"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/using_scikit_learn.html#configuring-and-building-an-experiment

define task function and set up CLI

run in CLI with
$ python src\scikit_learn_fc\train_models.py
to use default options

to run all experiments use
$ python src\scikit_learn_fc\train_models.py "dataset=glob(*)" "classifier=glob(*)" --multirun
"""

#####################################
# Configure and store task function #
#####################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from typing import Callable, Tuple
from hydra_zen import load_from_yaml, make_config, store

import add_classifiers_to_store
import add_datasets_to_store

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

# 2. Build a task function to load data, fit a classifier, and plot the result.
def task(
    dataset: Callable[[], Tuple[np.ndarray, np.ndarray]],
    classifier: BaseEstimator,
):
    fig, ax = plt.subplots()

    # create and split dataset for train and test
    X, y = dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4, random_state=42
    )

    # plot the data
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5

    # just plot the dataset first
    cm = plt.cm.RdBu
    cm_bright = ListedColormap(["#FF0000", "#0000FF"])

    # Plot the training points
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors="k")

    # Plot the testing points
    ax.scatter(
        X_test[:, 0],
        X_test[:, 1],
        c=y_test,
        cmap=cm_bright,
        alpha=0.6,
        edgecolors="k",
    )

    # Fit classifier on data
    clf = make_pipeline(StandardScaler(), classifier)
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    DecisionBoundaryDisplay.from_estimator(clf, X, cmap=cm, alpha=0.8, ax=ax, eps=0.5)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_axis_off()
    ax.text(
        x_max - 0.3,
        y_min + 0.3,
        ("%.2f" % score).lstrip("0"),
        size=25,
        horizontalalignment="right",
    )

    # load overrides to set plot title
    overrides = load_from_yaml(".hydra/overrides.yaml")


    # 3. Save the figure in the local experiment directory.
    if len(overrides) == 2:
        # Running in multirun mode: save fig based
        # on dataset/classifier overrides
        dname = overrides[0].split("=")[1]
        cname = overrides[1].split("=")[1]
        fig.savefig(f"{dname}_{cname}.png", pad_inches=0.0, bbox_inches = 'tight')
    else:
        # Not guaranteed to have overrides, just save as result.png
        fig.savefig("result.png", pad_inches=0.0, bbox_inches = 'tight')

    # For hydra multirun figures will stay open until all runs are completed
    # if we do not close the figure
    plt.close()


if __name__ == "__main__":
    from hydra_zen import zen
    from hydra.conf import HydraConf, JobConf
    # Configure Hydra to change the working dir to match that of the output dir
    store(HydraConf(job=JobConf(chdir=True)), name="config", group="hydra")

    # Add all of the configs, that we put in hydra-zen's (local) config store,
    # to Hydra's (global) config store.
    store.add_to_hydra_store(overwrite_ok=True)

    # Use `zen()` to convert our Hydra-agnostic task function into one that is
    # compatible with Hydra.
    # Use `.hydra_main(...)` to generate the Hydra-compatible CLI for our program.
    zen(task).hydra_main(config_path=None, config_name="config", version_base="1.2")