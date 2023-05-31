# Local Cassandra Setup

!!! info

    This page is about building a vector-search-capable branch of the Cassandra
    codebase and running it locally. You need these instructions
    only if you are not using a vector-capable Astra DB cluster _but_ you do
    want to experiment with the Vector Search components of these integrations.

    Make sure to redefine the way the `Session` object is obtained in the
    notebooks that make use of this capability.

    These instructions are aimed at those with some knowledge about building
    Java projects.

This section briefly outlines the process to build the Cassandra binaries
from the branch where development of the Vector Search Capabilities is
being actively done, and to start a locally-running single-node cluster
for experimentation.

!!! warning

    This is a development branch at the moment: it is not guaranteed to be
    stable. Please refrain from using it in production environments for a
    little while more.

## Building

You need Java JDK 11.
Go to any directory and:

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

## Running

If the above succeeded, you can
launch the cluster with:

```
sudo bin/cassandra -f -R
```

You may need to create a log directory if not present:

```
sudo mkdir -p /var/log/cassandra
```

## Opening a CQL Console

If you downloaded the vector-capable `cqlsh` as instructed on the
[DB setup](/db_setup/) page, locate it and simply launch

```
# adjust the path as needed
/home/user/myCqlsh/cqlsh-astra/bin/cqlsh
```

## Provisioning the database

The last step is to create a keyspace to host all tables for later usage.

Open a CQL console and run the following:

```
CREATE KEYSPACE IF NOT EXISTS cassio_tutorials
    WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1 };
```

You can check that the keyspace exists with:

```
DESC KEYSPACES;
```

Exit the CQL console and run this script, which will populate the local database
with sample tables occasionally used by some of the examples you'll encounter:

```
# adjust the path as needed
/home/user/myCqlsh/cqlsh-astra/bin/cqlsh \
    -k cassio_tutorials \
    -f setup/provision_db/write_sample_data.cql
```

## Everything is set

Well done: you can now browse the website and run the
code examples against your local database!

Remember to start Cassandra and keep it running when trying out the
examples that need it.

Remember to adjust the routine that creates the
`Session` if you used a different keyspace name.
