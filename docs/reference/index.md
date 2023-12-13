# CassIO reference

This part of the site provides documentation
for the CassIO library itself.

Check the individual pages for detailed docs on the available classes
and modules. Below  are a few general tips to keep in mind.

### Global init

You can invoke `cassio.init(...)`, in various ways, to set up a globally-available
connection to the database, in the form of a Session and a keyspace.
Later instantiations of CassIO objects which do not specify a database session
will default to this global setting.

### Data format

"Rows" of data entering and exit the CassIO abstractions are
in the form of regular Python dictionaries. In other words, you will not have to
worry about the `Row` named-tuple data format that is customary at the Cassandra
driver level.

### Table creation behind the scenes

When CassIO table abstractions are instantiated, normally a
`CREATE TABLE IF NOT EXISTS` statement is run. In particular, if a table was
created earlier with that name but different properties, that may silently
induce schema compatibility issues later on.
