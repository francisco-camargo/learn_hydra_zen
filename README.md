Learn `hydra-zen`
======

***Sandbox to learn and explore the Python library `hydra-zen`***

Francisco Camargo

# Learn Hydra Zen

Will use this repo as a sandbox to experiment using `hydra-zen`

# Open questions

* [ ] hydra store

  * [ ] save something to the store in one `.py` file, and then use it in another
  * [ ] what the heck is going on in the `if __name__ == '__main__'` section of example code?
    * [ ] is this how the datasets and model classes actually get saved to the store?
    * [ ] What's the deal with `version_base`?
  * [ ] `hydra_zen.store()` vs `hydra_zen.ZenStore.add_to_hydra_store`
  * [ ] how do I clear the store?
* [ ] how do I experiment

  * [ ] control which models to use
    * [ ] control which hyperparameters to use
    * [ ] control a gridsearchCV run
    * [ ] control a run over a specified list of values for a hyperparameter
  * [ ] control which data to use
  * [ ] control what data to plot

# Working directory

Still trying to get my head around how the directory situation is/needs to be handled. [Here ](https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/using_scikit_learn.html#id1)is one example that has the `hydra-zen` code in a subfolder yet the artifacts from having run the code are saved to `/outputs/` or `/multirun/`

```python
if __name__ == "__main__":  
    from hydra.conf import HydraConf, JobConf
    # Configure Hydra to change the working dir to
    # match that of the output dir
    store(HydraConf(job=JobConf(chdir=True)), name="config", group="hydra")
```

[Reference ](https://hydra.cc/docs/upgrades/1.1_to_1.2/changes_to_job_working_dir/)from Hydra

# Learning to use `hydra_zen.ZenStore()`

[docs](https://mit-ll-responsible-ai.github.io/hydra-zen/generated/hydra_zen.ZenStore.html)

# scikit_learn_howto

Following [this](https://mit-ll-responsible-ai.github.io/hydra-zen/how_to/using_scikit_learn.html) guide.

To run all experiments via CLI:

```shell
python src/scikit_learn_howto/my_app.py "dataset=glob(*)" "classifier=glob(*)" --multirun
```

seems like the `--multirun` option is needed to enable the `glob(*)` syntax

To run plotter code in CLI

```shell
python src/scikit_learn_howto/plotter.py
```

These two scripts are meant to be run in tandom, that is, if you run the experiment code multiple times, the plotter will likely not work. In this case, the easy fix is to delete the multirun folder and start the experiments over again.

If succeful, you should see the following plot:

![1675139723253](image/README/1675139723253.png)

# scikit_learn_fc

Here I will make changes to the scikit_learn_howto from the previous section

To run a single combination of data and classifier, can do the following:

```shell
python src/scikit_learn_fc/my_app_fc.py "dataset=moons" "classifier=knn"
```

where I have chosen the moons data and the knn classifier. Note that this will put the results into an `/outputs/` folder
