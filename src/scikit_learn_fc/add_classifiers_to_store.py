"""
following
    https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/using_scikit_learn.html#configuring-and-building-an-experiment

making a file to handle only adding classifiers to the local hydra-zen store

"""

from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from hydra_zen import builds, store

###################################
# Configure and store classifiers #
###################################

def all_classifiers():
    classifier_store = store(group="classifier")

    classifier_store(KNeighborsClassifier, n_neighbors=3, name="knn")
    classifier_store(SVC, kernel="linear", C=0.025, name="svc_linear")
    classifier_store(SVC, gamma=2, C=1, name="svc_rbf")
    classifier_store(
        GaussianProcessClassifier,
        kernel=builds(RBF, length_scale=1.0),
        name="gp",
    )
    classifier_store(DecisionTreeClassifier, max_depth=5, name="decision_tree")
    classifier_store(
        RandomForestClassifier,
        max_depth=5,
        n_estimators=10,
        max_features=1,
        name="random_forest",
    )
    classifier_store(MLPClassifier, alpha=1, max_iter=1000, name="mlp")
    classifier_store(AdaBoostClassifier, name="ada_boost")
    classifier_store(GaussianNB, name="naive_bayes")
    classifier_store(QuadraticDiscriminantAnalysis, name="qda")