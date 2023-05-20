# DB Setup

We show how to create an Astra DB instance and set the connection
details and secrets that all code examples can then use.

Astra DB is a serverless DBaaS by DataStax, built on Apache Cassandra, that offers
a free tier with generous traffic and storage limits. Using Astra DB frees you
from the hassle of running your own cluster while retaining all the advantages, such as the excellent data distribution and very high availability that make Cassandra a world-class NoSQL database.

!!! note "Self-managed Cassandra alternative"

    Nothing prevents you from adapting the examples to any Cassandra cluster:
    in most cases all you have to do is to build the database `Session` object
    differently, and that's it. Inspect the code to find out: generally it's
    just a couple of lines to change.

### Create your Astra DB instance

Go to [astra.datastax.com](https://astra.datastax.com), sign up and create an Astra DB database in the Free Tier -- in the following we assume you called it
`cassio_db`.

You will be asked for a "Keyspace name" when creating the database:
you can call it something like `cassio_tutorials` for example.

Detailed explanations can be found [at this page](https://awesome-astra.github.io/docs/pages/astra/create-instance/).

### Get Token and Secure Connect Bundle, create `.env` file

In order to establish a connection to your Cloud Database,
you need a secret string ("Token") and a "Secure Connect Bundle" zipfile, containing certificates/proxy/routing information.

The easiest way to do so is to first generate a database token with
role "Database Administrator", then use the Astra CLI to automate the
remaining part:

- how to [generate a token](https://awesome-astra.github.io/docs/pages/astra/create-token/) (remember to pick the "Database Administrator role);
- how to [install Astra CLI](https://awesome-astra.github.io/docs/pages/astra/astra-cli/#1-installation)

Now you can configure the CLI by running

```
astra setup
```

and providing the token (the string starting with `AstraCS:...`).
Then, in the root directory of this repo, launch

```
# Replace database and keyspace name with your values!
astra db create-dotenv cassio_db -k cassio_tutorials
```

This will download the bundle zipfile and create a `.env` file
with all connection parameters you'll need later.

??? tip "Alternatives to Astra CLI"

    If you prefer to proceed manually, you can
    [download the Secure Connect Bundle](https://awesome-astra.github.io/docs/pages/astra/download-scb/#c-procedure) somewhere on your machine,
    then create the `.env` file yourself, as long as it defines the same
    environment variables you see in the provided `.env.template` file
    (essentially, the full path to bundle file, the keyspace name and your database secret token string).

### Import sample data

Some of the provided code examples require pre-existing data on your
database. Run the following (which launches a CQL scripts in your database)
to write the reference data:

```
astra db cqlsh cassio_db -k cassio_tutorials \
  -f setup/provision_db/write_sample_data.cql
```

!!! note

    If you target a Cassandra cluster, make sure you `USE` your
    keyspace before running the script above.

### Your database is ready

The next step is to configure the necessary [API Keys](/api_setup).