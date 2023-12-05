If you want to see CassIO in action without runnig anything locally,
as outlined in the ["Start Here"](/start_here/) page, just open a Colab example
backed by an Astra DB cloud instance.

However, you may want to switch to a different setup. This page outlines how
this is accomplished in two separate respects: running the examples locally
as Jupyter notebooks, and running your own Cassandra cluster
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

First, clone this repository on your machine
(the repo spans both the website and the examples).
In a directory of your choice, execute the following:

```
git clone https://github.com/CassioML/cassio-website.git
cd cassio-website
```

Note that the following commands are to be run in the `cassio-website` directory.

### DB (Astra DB case)

You need a `.env` file which defines the database credentials and connection
parameters.

You can copy the provided `.env.template` file and replace
the environment variables you see there.
If using Astra DB, these amount to the database ID,
the Token (with role "database administrator"), and optionally a keyspace name.

If you plan on using a local Cassandra, the `.env` setup instructions are given
[below](#use-the-local-cassandra-in-the-code).

#### Pre-populate the database

Some of the provided code examples require pre-existing data on your
database.

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
for a list of supported LLMs: each requires different variable(s)
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

Starting with version 5.0, Apache Cassandra®
[ships](https://cassandra.apache.org/doc/trunk/cassandra/vector-search/overview.html)
with Vector capabilities.

You can easily launch a locally-running (single-node) Cassandra cluster through
Docker. First make sure you have Docker [installed](https://www.docker.com/),
then launch the following command:

```
docker run --name my-cassandra -d cassandra:5.0-alpha2
```

In the command above, you can name the container any way you like:
but keep in mind that the instructions on this page assume you
used `my-cassandra`.

The `5.0-alpha2`
is an image tag: you may want to check Cassandra's
[DockerHub page](https://hub.docker.com/_/cassandra#!)
for the newest `5.*` tag to use.

In a few minutes, the container will be up and running, ready to be used. You
can verify this by running `docker exec -it my-cassandra  nodetool status` and
looking for an output line starting with `UN ...`
(which stands the "Up" and "Normal" state of the node).

!!! note "Other ways to run Cassandra"

    If you have a running Cassandra cluster through other means than
    Docker, no problem. Just make sure to specify the contact point(s)
    and the keyspace name in the `.env` file as outlined below.

    For more advanced setup involving e.g. authentication, you might have to
    modify the Python code that creates the `Session` to fit your needs.

### CQL Console

To launch a CQL Console on the Docker container, run the following:

```
docker exec -it my-cassandra cqlsh
```

### Populate the database

Still in the CQL Console, create a keyspace for the examples by executing the following:

```
CREATE KEYSPACE IF NOT EXISTS cassio_tutorials
    WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
```

You can check that the keyspace exists with:

```
DESC KEYSPACES;
```

Exit the CQL console (`EXIT` + Enter) and ensure you are back to this repo's root dir
(you should have cloned it earlier to `/some/directory/cassio-website/`).

Now there's a small script to run, that populates the newly-created keyspace
with sample tables occasionally used by some of the examples you'll encounter.

To run the script, copy it to the Docker container and
then ask `cqlsh` to run it there:

```
docker cp setup/provision_db/write_sample_data.cql my-cassandra:/
docker exec -it my-cassandra cqlsh \
    -k cassio_tutorials \
    -f /write_sample_data.cql
```

### Use the local Cassandra in the code

Your local Cassandra is ready to support all examples. Now make sure you
set the connection parameters in the `.env` file (at the root of this repo).

You can copy from the provided `.env.template` example file if
you haven't yet and, ignoring the `ASTRA_DB...` variables, make sure
the `LOCAL_...` variables in the `.env` define:

- the correct keyspace name used above;
- and the IP address (or "contact point") for the Docker image.

In particular, the IP address of the container is found within the very long
output of `docker inspect my-cassandra`. The following command
should locate it for you:

```
docker inspect my-cassandra | \
    jq -r '.[].NetworkSettings.Networks.bridge.IPAddress'

# ... with an output such as "172.17.0.2"
```

All notebooks offer the choice between using Cassandra and Astra DB: the former
case relies on a `c1qlsession.py`, imported from the notebooks,
which provides the simple logic to create the session and read the keyspace
from the environment variables. If you need additional customization (such as
setting up authentication, using a custom port for CQL, etc), this is the
file you should
[further edit](https://docs.datastax.com/en/developer/python-driver/latest/getting_started/#connecting-to-cassandra)
to fit your needs.

Keep in mind that if you are running the notebooks in a cloud environment such
as Google Colab the only supported choice will be the cloud database Astra DB.
_(Should you need to run a Colab targeting a Cassandra cluster, you will have to_
_essentially transport the logic in `cqlsession.py` into a notebook cell.)_
