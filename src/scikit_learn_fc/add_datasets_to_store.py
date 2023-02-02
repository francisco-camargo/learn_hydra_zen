"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/using_scikit_learn.html#configuring-and-building-an-experiment

making a file to handle only adding datasets to the local hydra-zen store

"""

################################
# Configure and store datasets #
################################

from sklearn.datasets import make_circles, make_classification, make_moons
import numpy as np
from hydra_zen import store


# For the linear dataset, add a wrapper that
# randomly spaces our the data
def add_random_scattering(make_dataset):
    def wraps(*args, **kwargs):
        X, y = make_dataset(*args, **kwargs)
        rng = np.random.RandomState(2)
        X += 2 * rng.uniform(size=X.shape)
        return X, y
    return wraps


def all_datasets():
    dataset_store = store(group="dataset")

    dataset_store(
        make_classification,
        zen_wrappers=add_random_scattering,  # <- apply wrapper here
        zen_partial=True,
        n_features=2,
        n_redundant=0,
        n_informative=2,
        random_state=1,
        n_clusters_per_class=1,
        name="linear",
    )
    dataset_store(
        make_moons,
        zen_partial=True,
        noise=0.3,
        random_state=0,
        name="moons",
    )
    dataset_store(
        make_circles,
        zen_partial=True,
        noise=0.2,
        factor=0.5,
        random_state=1,
        name="circles",
    )


if __name__ == '__main__':
    all_datasets()