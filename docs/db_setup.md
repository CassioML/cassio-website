# DB Setup

We show how to create an Astra DB instance and set the connection
details and secrets that all code examples can then use.

!!! question "Run locally or use Colab?"

    You can run most of the examples either locally on your environment
    or taking advantage of Google Colaboratory, it's up to you.

    Just keep in mind that each Colab instance is ephemeral: as such,
    to run each notebook there you will have to repeat a modicum of setup
    such as installing dependencies and supplying DB connection parameters
    and API Keys, whereas if you configure a local environment once you will
    be able to run all notebooks straight away.

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

!!! tip "Vector Search"

    If you want to take advantage of the Vector Search capabilities that are
    currently in Public Preview in Astra, make sure to pick the
    **"Serverless with Vector (Preview)"** option when creating your database.

    If you choose to use an Astra database without Vector Search support, you
    can still test the corresponding components of CassIO against a
    Cassandra instance with Vector Search enabled. See [here](/local_db_setup/)
    for instructions on how to build and run one such instance locally.

### Get Token and Secure Connect Bundle

In order to establish a connection to your Cloud Database,
you need a secret string ("Token") and a "Secure Connect Bundle"
zipfile, containing certificates/proxy/routing information.

The easiest way to do so is to first generate a database token with
role "Database Administrator", then use the Astra CLI to automate the
remaining part:

- how to [generate a token](https://awesome-astra.github.io/docs/pages/astra/create-token/) (remember to pick the "Database Administrator role);
- how to [install Astra CLI](https://awesome-astra.github.io/docs/pages/astra/astra-cli/#1-installation)

!!! tip "Colab users: you're done"

    If you plan to run the examples within Google Colab, that's all you need
    to do now: you can skip the rest of the page and move on to 
    [API Setup](/api_setup).

    Note, however, that certain notebooks may occasionally require further
    setup steps (we'll make that clear along the way).

### Create `.env` file

Now you can configure the CLI by running

```
astra setup
```

and providing the token (the string starting with `AstraCS:...`).
Then, in the root directory of this repo, adjusting names if needed, launch

```
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
database.
<!-- Run the following (which launches a CQL scripts in your database)
to write the reference data:

```
astra db cqlsh cassio_db -k cassio_tutorials \
  -f setup/provision_db/write_sample_data.cql
```
 -->
To populate the newly-created keyspace with the required data:

- clone [this repo](https://github.com/cassioML/cassio-website) if you haven't already (it contains the website content, but also all code examples for you);
- download the newest (vector-search-compatible) `cqlsh` utility from [this link](https://downloads.datastax.com/enterprise/cqlsh-astra-20230526-vectortype-bin.tar.gz);
- extract the archive to a location of your liking, e.g. `/home/user/myCqlsh`;
- source the environment file you just prepared with `. .env` (make sure you are in this repo's root directory);
- `cd` to this repo's root directory and launch the script that populates the database:

```
/home/user/myCqlsh/cqlsh-astra/bin/cqlsh \
    -b "$ASTRA_DB_SECURE_BUNDLE_PATH" \
    -u token \
    -p "$ASTRA_DB_APPLICATION_TOKEN" \
    -k "$ASTRA_DB_KEYSPACE" \
    -f setup/provision_db/write_sample_data.cql
```


!!! tip "Astra DB's in-browser console"

    You can also run this step without a local `cqlsh` client (for instance,
    if you are using Colab and want to skip local setup entirely).

    Locate the [CQL Console](https://awesome-astra.github.io/docs/pages/astra/faq/#how-to-open-the-web-cql-console) in you Astra DB instance, then:

    1. enter the command `USE cassio_tutorials;` and press Enter. Replace with your keyspace name if you called it differently.
    2. Paste the contents of [this file](https://raw.githubusercontent.com/CassioML/cassio-website/main/setup/provision_db/write_sample_data.cql) in the Console and watch the show.


!!! note

    If you target your own Cassandra cluster, make sure you `USE` your
    keyspace before running the script above.

### Your database is ready

The next step is to configure the necessary [API Keys](/api_setup).
