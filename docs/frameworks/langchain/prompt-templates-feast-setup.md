# Feast + Cassandra, setup

The following example shows how to connect your prompt templates
with the Feast feature store with minimal boilerplate.

!!! info Feast and Cassandra

    Feast can admit several database technologies as its storage layer, one
    of which being Cassandra.

    In this spirit, aiming at providing comprehensive information
    on how to integrate LangChain and Cassandra, we chose to cover this use case
    as well.

In order to test the code yourself, you first need to create a sample
feature store. The following instructions will guide you through the
setup of the very feature store (including sample data) that is used
in the next code example.

### Provision the Feature Store

You will create a new Feature Store and configure it to use
the Astra DB instance you should already have as its "online store".

In practice, this amounts to Feast managing a couple of additional tables
on your database.

### Preliminaries

Navigate to the directory `docs/frameworks/langchain/feast_store` of this
repo, activate the virtual environment for the LangChain examples
and install this dependency:

```
pip install "feast[cassandra]>=0.26"
```

Keep file `../../../../.env` handy, as you will be shortly asked to provide
the Secure Connect Bundle location and the keyspace name defined there.

### Create the feature store

Launch the following:

```
feast init -t cassandra user_features
```

choose Astra DB (recommended) or Cassandra,
then provide the other required information (pay attention
to the question about the keyspace: provide the name of the keyspace you
created earlier in the "DB setup" step).
You can skip the optional parameters altogether.

!!! Note "Client ID and Client Secret"

    Provide the literal `token` as "Client ID" and the value of
    `ASTRA_DB_APPLICATION_TOKEN` as found in `.env` as "Client Secret".

    If you did not use the Astra CLI to set up the global `.env` file,
    please refer to [these instructions](https://awesome-astra.github.io/docs/pages/astra/create-token/#c-procedure)
    on how to generate a Token for your database.

A brand new feature store has been created in subdirectory `user_features`.
_(Note: if you give a different name to your store,_
_adapt the following commands accordingly.)_

### Prepare data sources

This command creates the data sources for ingestion by Feast
in the form of two `*.parquet` files:

```
python prepare_feast_data.py
```

Place the sources within the store, ready to be found by Feast:

```
mv *.parquet user_features/feature_repo/data/
```

### Replace feature definitions

We have a ready-to-use feature definition file for this store.
All you have to do is to copy it over the default one:

```
cp user_data_feature_definitions.py user_features/feature_repo/example_repo.py
```

### Provision the store backend

This step will trigger Feast to create the required table in your Astra DB:

```
cd user_features/feature_repo/
feast apply
```

### Materialize data to online store

Now you can have Feast transport the data into the (still empty) tables that
constitute the online store:

```
DATE0=$(date -d "`date` - 10 years" "+%Y-%m-%dT%H:%M:%S")
DATE1=`date "+%Y-%m-%dT%H:%M:%S"`
feast materialize $DATE0 $DATE1
```

### Ready to go

That's it. Now you can run the examples that require the Feast store.
