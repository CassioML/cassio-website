# Vector Similarity Search

This section shows what `cassIO` is offering to support
easy usage of the "Vector Similarity Search" capabilities.

These are being added to Cassandra (CEP-30) and,
at the time of writing, have not yet made it to `trunk`.
For this reason, at the moment you need to build
the database from the source and run it yourself
locally. [This page](/local_db_setup) offers a guide on how to do that.

!!! note

    While the LangChain wrappers are expected to remain
    reasonably stable, the internals (e.g. the cassIO
    implementation, or the CQL syntax used therein) are probably going
    to change quite a bit.

    Please refrain from using these capabilities in a production environment
    for a little while more.

Correspondingly, until the vector search capabilities are not merged to
`trunk` in the Cassandra codebase, you will need to enable the associate
components in the CassIO library. Don't worry, the next examples will show you
how to do just that.