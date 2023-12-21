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

```bash
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

```bash
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

```bash
docker run --name my-cassandra -d cassandra:5
```

In the command above, you can name the container any way you like:
but keep in mind that the instructions on this page assume you
used `my-cassandra`.

The `5`
is an image tag: you may want to check Cassandra's
[DockerHub page](https://hub.docker.com/_/cassandra#!)
for the newest beyond `5.*` tag to use.

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

```bash
docker exec -it my-cassandra cqlsh
```

### Populate the database

Still in the CQL Console, create a keyspace for the examples by executing the following:

```sql
CREATE KEYSPACE IF NOT EXISTS cassio_tutorials
    WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
```

You can check that the keyspace exists with:

```sql
DESC KEYSPACES;
```

You can now exit the CQL console (`EXIT` + Enter, or `Ctrl-D`).

### Use the local Cassandra in the code

Your local Cassandra is ready to support all examples. Now make sure you
set the connection parameters in the `.env` file (at the root of this repo).

You can copy from the provided `.env.template` example file if
you haven't yet and, ignoring the `ASTRA_DB...` variables, make sure
the `LOCAL_...` variables in the `.env` define:

- and the IP address (or "contact point") for the Docker image;
- the correct keyspace name used above.

In particular, the IP address of the container is found within the very long
output of `docker inspect my-cassandra`. The following command
should locate it for you:

```bash
docker inspect my-cassandra | \
    jq -r '.[].NetworkSettings.Networks.bridge.IPAddress'

# ... with an output such as "172.17.0.2"
```

All notebooks offer the choice between using Cassandra and Astra DB: the former
case relies on a `cqlsession.py`, imported from the notebooks,
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
