# Global init

```python
import cassio

cassio.init(...)
```

The purpose of this statement is to set a globally-available
`cassandra.cluster.Session`, together with a keyspace name,
as the default database connection for all subsequent CassIO instantiations. Once you have run `init(...)`, you do not need to specify the DB anymore, e.g.

```python
table = cassio.table.MetadataCassandraTable(table="my_table")

reader = cassio.db_reader.MultiTableCassandraReader(
    field_mapper={"v": ("t", "c")},
    admit_nulls=False,
)
```

Of course, you can still specify the parameters `session` and/or `keyspace` when creating the objects, in which case
the latter will take precedence (for example, you may set the Session through `init` and then choose different keyspaces for various objects).

The `init(...)` can be invoked in several ways -- some of which exemplified below; no matter what the call signature, the invocation results in a session and/or a keyspace being set as defaults.

## Example signatures

You have a Session and a Keyspace prepared beforehand:

```python
import cassandra
cluster = cassandra.cluster.Cluster(...)
session = cluster.connect()
cassio.init(session=session, keyspace="my_k")
```

You have the connection parameters to a Cassandra cluster:

```python
cassio.init(
    contact_points=['127.0.0.1'],
    username='u',
    password='p',
)
```

You have the credentials to an Astra DB instance:

```python
cassio.init(database_id="abcd0123-...", token="AstraCS:...")
```

There are suitable environment variables available (e.g. `CASSANDRA_CONTACT_POINTS`, or the combination `ASTRA_DB_APPLICATION_TOKEN` plus `ASTRA_DB_DATABASE_ID`):

```python
cassio.init(auto=True)
```

For more, try `help cassio.init` in a Python REPL.

## Usage

Note that the global defaults thus set are consulted at
constructor time by the various abstractions (e.g. the tables): so the following interaction, for example,

```python
cassio.init(session=S1, keyspace=K1)
my_table = cassio.table.PlainCassandraTable(table="my_table")
cassio.init(session=S2, keyspace=K2)
table.put(row_id="x", body_blob="y")
```

does result in a table, with a row, in session `S1`: `my_table` will never be aware of the second `init(...)`.

## Accessing the session/keyspace

You can access the globally set DB connection at any time:

```
s = cassio.config.resolve_session()
k = cassio.config.resolve_keyspace()
```

These are an ordinary `cassandra.cluster.Session` and an ordinary string
(unless, if not set yet, `None`), which can be used e.g. to execute CQL
statements.

```python
s.execute(f"DROP TABLE IF EXISTS {k}.table_name;")
```
