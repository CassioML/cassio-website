# Local Cassandra Setup

This section briefly outlines the process to build the Cassandra binaries
from the branch where development of the Vector Search Capabilities is
being actively done, and to start a locally-running single-node cluster
for experimentation.

!!! warning

    This is a development branch at the moment: it is not guaranteed to be
    stable. Please refrain from using it in production environments for a
    little while more.

## Building

Go to a fresh directory and:

```
git clone https://github.com/datastax/cassandra.git
cd cassandra
git checkout cep-vsearch
ant jar
```

## Running

Launch the cluster with:

```
./bin/cassandra -f
```

## Opening a CQL Console

In order to have a CQL console able to fully interoperate with this branch,
do the following in the directory where you cloned the Cassandra code
(and preferrably in a Python virtual environment):

```
pip install git+https://github.com/datastax/python-driver.git@cep-vsearch#egg=cassandra-driver
pip install wcwidth
```

You can now start a CQL console with:

```
CQLSH_NO_BUNDLED=True bin/cqlsh
```

## Create a keyspace

The last step is to create a keyspace, which will be where all examples
will create the tables they need.

Open a CQL console and run the following:

```
CREATE KEYSPACE IF NOT EXISTS demo
    WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1 };
```

You can check that the keyspace exists with:

```
DESC KEYSPACES;
```

### Everything is set

Well done: you can now browse the website and run the code examples!

Remember to start Cassandra and keep it running when trying out the
examples that need it.
