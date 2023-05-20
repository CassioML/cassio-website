# Setup to run the LangChain examples

## Setup

!!! note

    This is required if you want to _run the examples yourself_ (recommended).

Make sure you did the [general setup](/db_setup/) first.

Go to `docs/frameworks/langchain`.

Create a Python 3.8+ virtual environment, activate it and install dependencies with:

```
pip install -r requirements_langchain.txt
```

!!! info

    The current requirements file builds a couple of packages from source.
    We are working to publish the `cassio` package to PyPI very soon.

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





- clone `https://github.com/hemidactylus/cassio` and `pip install -e .`;
- clone `https://github.com/hemidactylus/langchain` _in the `cassio` branch_ and `pip install -e .`;

Now, in the same console, first `. ../.env` and then `jupyter notebook`.

You are now ready to run the notebooks.