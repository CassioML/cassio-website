# Setup for running the "stand-alone" demos locally

Follow these steps to get a local environment able to run the demos about
using CassIO directly.

## Setup

!!! note

    You can skip this page if you are interested in Colab notebooks only.

    These are the instructions for local setup of the
    Python environment for the "Stand-alone" examples.
    A prerequisite is the [general setup for running locally](/more_info/#run-with-local-jupyter).

    Note that not many demos here will require access to an LLM provider (so you may safely ignore the LLM requirement and still run most of the notebooks provided here).

You should have a copy of this repository from the [general local-run setup](/more_info/#run-with-local-jupyter) already.
Go to the `docs/frameworks/standalone` subdirectory.

Create a Python 3.8+
[virtual environment](https://virtualenv.pypa.io/en/latest/user_guide.html),
activate it and install the required dependencies with:

```bash
pip install -r requirements_standalone.txt
```

## Launch

Make sure you are in `docs/frameworks/standalone` and the virtual environment is active.

Source the API Key configuration with

```bash
. ../../../.api_keys
```

Now fire up Jupyter with:

```bash
jupyter notebook
```

and wait for a browser window to open with the notebooks in this directory,
ready to run.

## Database choice

The notebooks provide a choice between using Cassandra and Astra DB.
Keep in mind that, if on a Colab, only Astra DB is supported out of the box.
Check the ["Further reading"](/more_info/) section for more information.
