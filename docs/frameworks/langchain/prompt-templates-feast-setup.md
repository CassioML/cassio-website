# Feast + Cassandra, setup

The following example shows how to connect your prompt templates
with the Feast feature store with minimal boilerplate.

!!! info "Feast and Cassandra"

    Feast can admit several database technologies as its storage layer, one
    of which being Cassandra (hence, Astra DB as a Cassandra-compatible backend).

    In this spirit, aiming at providing comprehensive information
    on how to integrate LangChain and Cassandra, we chose to cover this use case
    as well.

In order to test the code yourself, you first need to create a sample
feature store. The following instructions will guide you through the
setup of the very feature store (including sample data) that is used
in the next code example.

!!! warning

    The Feast example is not available as Colab and must be run locally.
    This means you'll need to go through a
    [general setup](/more_info/#run-with-local-jupyter),
    followed by
    [LangChain-specific setup](/frameworks/langchain/setup/),
    before reading this page further.

### Provision the Feature Store

You will create a new Feature Store and configure it to use
your database (either Cassandra or Astra DB) as its "online store".

In practice, this amounts to Feast managing a couple of additional tables.

### Preliminaries

Navigate to the directory `docs/frameworks/langchain/feast_store` of this
repo (which you should have cloned in earlier setup steps),
activate the virtual environment for the LangChain examples
and install this dependency:

```bash
pip install "feast[cassandra]>=0.26"
```

!!! warning

    The latest version of LangChain brings an apparent conflict
    with Feast on package `SQLAlchemy`. Pending upgrades on the Feast side,
    our experience is that you will be fine by running the following command
    right after installing Feast: `pip install "sqlalchemy>=2"`.

    Do not worry about a message similar to
    _"feast 0.33.1 requires SQLAlchemy[mypy]<2,>1, but you have sqlalchemy 2.0.20 which is incompatible."_: the example notebook will run just fine.

Keep file `../../../../.env` handy, as you will be shortly asked to provide
database connection parameters and secrets for the Feast setup.

### Create the feature store

The following command starts an interactive creation
of the feature store. Depending on whether you choose Cassandra or Astra DB,
you will supply a different set of parameters:

```bash
feast init -t cassandra user_features
```

Provide the required information, paying attention to the
keyspace name (`cassio_tutorials` if you went with the defaults).
For details, see
[the Feast docs page](https://docs.feast.dev/reference/online-stores/cassandra#getting-started).
Keep also in mind that, for Astra DB, you will be asked to provide
the full path to the "Secure connect bundle" zipfile you can
[download](https://awesome-astra.github.io/docs/pages/astra/download-scb/#c-procedure)
from the dashboard.

!!! Note "Client ID and Client Secret for Astra DB"

    Provide the string literal `token` as "Client ID" and the value of
    `ASTRA_DB_APPLICATION_TOKEN`, found in your `.env`, as "Client Secret".

    If needed, please refer to
    [these instructions](https://awesome-astra.github.io/docs/pages/astra/create-token/#c-procedure)
    on how to generate a Token for your database.

A brand new feature store has been created in subdirectory `user_features`.
_(Note: if you give a different name to your store,_
_adapt the following commands accordingly.)_

### Prepare data sources

This command creates the data sources for ingestion by Feast
in the form of two `*.parquet` files:

```bash
python prepare_feast_data.py
```

Place the sources within the store, ready to be found by Feast:

```bash
mv *.parquet user_features/feature_repo/data/
```

### Replace feature definitions

We have a ready-to-use feature definition file for this store.
All you have to do is to copy it over the default one:

```bash
cp user_data_feature_definitions.py user_features/feature_repo/example_repo.py
```

### Provision the store backend

This step will trigger Feast to create the required table in your Astra DB:

```bash
cd user_features/feature_repo/
feast apply
```

### Materialize data to online store

Now you can have Feast transport the data into the (still empty) tables that
constitute the online store:

```bash
DATE0=$(date -d "`date` - 10 years" "+%Y-%m-%dT%H:%M:%S")
DATE1=`date "+%Y-%m-%dT%H:%M:%S"`
feast materialize $DATE0 $DATE1
```

### Ready to go

That's it. Now you can run the examples that require the Feast store.
