Learn `hydra-zen`
======

***Sandbox to learn and explore the Python library `hydra-zen`***

Francisco Camargo

# Learn Hydra Zen

Will use this repo as a sandbox to experiment using `hydra-zen`

# Open questions

* [ ] hydra store
* [ ] how do I experiment

# scikit-learn example

Following [this](https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/using_scikit_learn.html) guide.

To run all experiments via CLI:

```shell
python src/scikit_learn_howto/my_app.py "dataset=glob(*)" "classifier=glob(*)" --multirun
```

To run plotter code in CLI

```shell
python src/scikit_learn_howto/plotter.py
```

These two scripts are meant to be run in tandom, that is, if you run the experiment code multiple times, the plotter will likely not work. In this case, the easy fix is to delete the multirun folder and start the experiments over again.
