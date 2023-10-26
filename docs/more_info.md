The easiest way to see CassIO in action, as outlined in the "Start Here"
page, is certainly to open a Colab example backed by an Astra DB instance.

However, you may want to switch to a different setup. This page outlines how
this is accomplished in two separate respects: running the examples locally
as Jupyter notebooks, and using a local (pre-release) Cassandra cluster
instead of Astra DB.

## Run with local Jupyter

There are several reasons one might prefer to launch the code locally:
for example, it may be easier to evolve the notebooks
into a full-fledged application; also, one can prefer a non-ephemeral
setup, especially when planning to run several examples in a row.

In the following we assume you have fulfilled the
[pre-requisites](/start_here/#vector-database) listed on the previous page.

You should have basic familiarity with `git` and the shell console.

### Clone this repository

First, clone this repo on you machine
(it spans both the website and the examples).
In a directory of your choice, execute the following:

```
git clone https://github.com/CassioML/cassio-website.git
cd cassio-website
```

Note that the following commands are to be run in the `cassio-website` directory.

### DB

You need a `.env` file which defines the database credentials and connection
parameters.

You can copy the provided `.env.template` file and replace
the environment variables you see there
(essentially, the full path to the bundle file, the keyspace
name and your database secret token string and ID).

??? tip "Using the Astra CLI"

    Alternatively, once you have the Database Administrator token,
    you can use the Astra CLI to automate the rest (secure-connect bundle and `.env` file).

    First [install Astra CLI](https://awesome-astra.github.io/docs/pages/astra/astra-cli/#1-installation).

    Then configure it with:

    ```
    astra setup
    ```

    providing the Database Administrator token you created earlier
    (the string starting with `AstraCS:...`).

    Finally, in the root directory of this repo, adjusting names if needed, launch

    ```
    astra db create-dotenv cassio_db -k cassio_tutorials
    ```

    This will download the bundle zipfile and create a `.env` file
    with all connection parameters you'll need later.

#### Pre-populate the database

Some of the provided code examples require pre-existing data on your
database.
<!-- Run the following (which launches a CQL script in your database)
to write the reference data:

```
astra db cqlsh cassio_db -k cassio_tutorials \
  -f setup/provision_db/write_sample_data.cql
```
 -->
To populate the newly-created keyspace with the required data:

- download the newest (vector-search-compatible) `cqlsh` utility from [this link](https://downloads.datastax.com/enterprise/cqlsh-astra-20230526-vectortype-bin.tar.gz);
- extract the `cqlsh` archive to a location of your liking, e.g. `/home/user/myCqlsh`;
- ensure you are still in the repo's root directory;
- source the environment file you prepared in the previous step with `. .env`;
- launch the script that populates the database (adjust the path as needed):

```
/home/user/myCqlsh/cqlsh-astra/bin/cqlsh \
    -b "$ASTRA_DB_SECURE_BUNDLE_PATH" \
    -u token \
    -p "$ASTRA_DB_APPLICATION_TOKEN" \
    -k "$ASTRA_DB_KEYSPACE" \
    -f setup/provision_db/write_sample_data.cql
```

!!! tip "Astra DB's in-browser console"

    Alternatively, you can also populate the database
    without a local `cqlsh` client, all from your browser.

    Locate the [CQL Console](https://awesome-astra.github.io/docs/pages/astra/faq/#how-to-open-the-web-cql-console) in you Astra DB instance, then:

    1. enter the command `USE cassio_tutorials;` and press Enter. Replace with your keyspace name if you called it differently.
    2. Paste the contents of [this file](https://raw.githubusercontent.com/CassioML/cassio-website/main/setup/provision_db/write_sample_data.cql) in the Console and wait for it to complete.

### LLM Credentials

In this repo's root directory again, create a `.api_keys` file where the secrets
necessary for your LLM of choice are defined. You can copy
the provided `.api_keys.template` and adjust the values therein.

Check out the [LLM Pre-requisites](/start_here/#vector-database)
for a list of supported LLMs: each will require a different variable
to be set here.

!!! note "Automatic choice of LLM"

    The code examples generally rely on a helper function to determine
    which LLM to use, based on which secrets are detected in this file.
    You can define your preferred LLM
    (e.g. in case you define more than one secret) by setting
    the environment variable `PREFERRED_LLM_PROVIDER` in `.api_keys`.

Remember to "source" this file before launching notebooks or Python scripts:

```
. .api_keys
```

### Framework-specific setup

Now, database and LLM are all set for running the examples locally.

For each framework, still, you will have to prepare a specific
Python environment with the right dependencies. The instructions are given
in the section of this docs specific to that framework:
for example, here is how you start the
[LangChain examples](/frameworks/langchain/setup/) locally.

## Use a local Vector-capable Cassandra

At the time of writing, the Vector Similarity Search capabilities
are not yet included in the distributions of Cassandra
(see [CEP-30](https://cwiki.apache.org/confluence/display/CASSANDRA/CEP-30%3A+Approximate+Nearest+Neighbor%28ANN%29+Vector+Search+via+Storage-Attached+Indexes) to track the status).

If you want to use the latest Cassandra that implements Vector Search,
you can still do so by building the code yourself.
The following instructions describe how to do that and get a single-node
vector-capable Cassandra cluster running locally.

!!! warning

    This is a development branch at the moment: it is not guaranteed to be
    stable. Please refrain from using it in production environments for a
    little while more.

These instructions require some knowledge of Java building tools.

### Build and run

You need Java JDK 11.
Go to a directory of your choice and execute:

```
# get the code
git clone https://github.com/datastax/cassandra.git
cd cassandra
git checkout vsearch
git pull

# setup usage of JDK 11
sudo update-alternatives --config java    # ... and pick JDK 11
export CASSANDRA_USE_JDK11=true
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/   # adapt this command

# clean and build
ant realclean
ant jar
```

If the above succeeded, you can
launch the cluster with:

```
sudo bin/cassandra -f -R
```

You may need to create a log directory if not present:

```
sudo mkdir -p /var/log/cassandra
```

### CQL Console

Using the vector-aware CQL Console that can be downloaded [here](https://downloads.datastax.com/enterprise/cqlsh-astra-20230526-vectortype-bin.tar.gz), open a CQL Console by launching:

```
# adjust the path as needed
/home/user/myCqlsh/cqlsh-astra/bin/cqlsh
```

### Populate the database

Still in the CQL Console, create a keyspace for the examples by executing the following:

```
CREATE KEYSPACE IF NOT EXISTS cassio_tutorials
    WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1 };
```

You can check that the keyspace exists with:

```
DESC KEYSPACES;
```

Exit the CQL console (`EXIT` + Enter), go back to this repo's root dir (you should have cloned it earlier to `/some/directory/cassio-website/`),
then run this script, which will populate the local database
with sample tables occasionally used by some of the examples you'll encounter:

```
# adjust the path as needed
/home/user/myCqlsh/cqlsh-astra/bin/cqlsh \
    -k cassio_tutorials \
    -f setup/provision_db/write_sample_data.cql
```

### Use the local Cassandra in the code

Your local Cassandra is ready to support all examples.

The only remaining thing is to make sure the `Session` object used in the
code is a connection to your local database: how exactly this is achieved
depends on the framework you use.

With Langchain, for example, you can simply use the provided
`getCQLSession` and `getCQLKeyspace`
functions making sure you pass the parameter `mode="local"` when calling them.

More generally, you can build a connection to the local Cassandra with
Python code similar to the following:

```
from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect()
```

the `session` object, along with the keyspace name (a string),
can then be used e.g. in the `cassio.init(...)` invocations,
or when instantiating individual objects, exactly in the same way
as you would a connection to Astra DB
(see [the drivers documentation](https://docs.datastax.com/en/developer/python-driver/latest/getting_started/#connecting-to-cassandra) for more options).
