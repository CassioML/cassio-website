# Global init

```python
import cassio

cassio.init(...)
```

The purpose of this statement is to set a globally-available
`cassandra.cluster.Session`, together with a keyspace name,
as the default database connection for all subsequent instantiations.

## Example signatures

```python
cassio.init(session=S, keyspace=K)
```

```python
cassio.init(database_id="acd", token="AstraCS:...")
```

```python
cassio.init(auto=True)
```

For more, try `help cassio.init` in a Python REPL.

## Usage

## Accessing the session/keyspace

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

