# Examples

This section provides minimal guidance to run your first CassIO-backed code in the
form of Jupyter notebooks.

You can inspect the example in your Web browser, download it to run it locally,
or even launch it in Google Colab (look for the button on the upper right).
If you run the notebook locally, it is suggested to work in a virtual environment.

It is assumed that you know your way around Python and have a Cassandra cluster,
or a DataStax [Astra DB](https://www.datastax.com/products/datastax-astra)
instance, at your disposal. You will provide the connection details
within the notebook.

!!! info "Database connection settings"

    If you target a Cassandra cluster, you need: (a) one or more contact points, i.e.
    IP addresses; (b) the name of a keyspace accessible on the database; (c) optionally,
    username and password for database authentication.

    If, instead, you use an Astra DB, you need: (a) the API Endpoint for the database,
    (b) an associated Database Token, and (c) optionally a keyspace name if you want to
    specify one.
