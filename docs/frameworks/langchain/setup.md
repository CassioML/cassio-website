# Setup to run the LangChain examples

## Setup

!!! note

    This is required if you want to _run the examples yourself_ (recommended).

Make sure complete the [general setup](/db_setup/) before proceeding with this tutorial.
You will have a local clone of this repository, in which you will run the following
commands.

Go to `docs/frameworks/langchain`.

Create a Python 3.8+ [virtual environment](https://virtualenv.pypa.io/en/latest/user_guide.html), activate it and install dependencies with:

```
pip install -r requirements_langchain.txt
```

!!! info

    Pending a PR to upstream, the current requirements file temporarily installs LangChain from a fork we maintain.

## Launch

Make sure you are in `docs/frameworks/langchain` and the virtual environment is active.

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

In most notebooks you'll find a cell where the two
calls `getCQLSession` and `getCQLKeyspace` take place.
You can switch between the Astra DB instance and the local database (if you have
one) by changing the value of the variable `cqlMode` therein
from `astra_db` to `local`.
