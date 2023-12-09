# LlamaIndex setup for running locally

## Setup

!!! note

    You can skip this page if you are interested in Colab notebooks only.

    These are the instructions for local setup of the LlamaIndex-specific
    Python environment. A prerequisite is the [general setup for running locally](/more_info/#run-with-local-jupyter).

You should have a copy of this repository from the [general local-run setup](/more_info/#run-with-local-jupyter) already.
Go to the `docs/frameworks/llamaindex` subdirectory.

Create a Python 3.8+
[virtual environment](https://virtualenv.pypa.io/en/latest/user_guide.html),
activate it and install the required dependencies with:

```
pip install -r requirements_llamaindex.txt
```

## Launch

Make sure you are in `docs/frameworks/llamaindex` and the virtual environment is active.

Source the API Key configuration with

```
. ../../../.api_keys
```

Now fire up Jupyter with:

```
jupyter notebook
```

and wait for a browser window to open with the notebooks in this directory,
ready to run.

## Database choice

The notebooks provide a choice between using Cassandra and Astra DB.
Keep in mind that, if on a Colab, only Astra DB is supported out of the box.
Check the ["Further reading"](/more_info/) section for more information.
