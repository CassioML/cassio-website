# "Direct CassIO" setup for running locally

## Setup

!!! note

    You can skip this page if you are interested in Colab notebooks only.

    These are the instructions for local setup of the
    Python environment for the "direct CassIO" examples.
    A prerequisite is the [general setup for running locally](/more_info/#run-with-local-jupyter).

    Note that not many demos here will require access to an LLM provider (so you may safely ignore the LLM requirement and still run most of the notebooks provided here).

You should have a copy of this repository from the [general local-run setup](/more_info/#run-with-local-jupyter) already.
Go to the `docs/frameworks/direct_cassio` subdirectory.

Create a Python 3.8+
[virtual environment](https://virtualenv.pypa.io/en/latest/user_guide.html),
activate it and install the required dependencies with:

```
pip install -r requirements_direct_cassio.txt
```

## Launch

Make sure you are in `docs/frameworks/direct_cassio` and the virtual environment is active.

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

The code looks for an Astra DB instance by default (as defined in
the `.env` file at the root of this repo).

If you have a Cassandra cluster
and want to use it instead, all you need is to find the notebook cell
where the two calls `getCQLSession` and `getCQLKeyspace` take place:
you can switch to a Cassandra cluster by changing the value
of the variable `cqlMode` therein from `astra_db` to `local`.
See the
["Further reading"](/more_info/#use-the-local-cassandra-in-the-code)
section for more on using a local Cassandra.
