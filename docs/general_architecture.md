# cassIO, general architecture

The purpose of CassIO is to abstract away the details of
accessing the Cassandra database for the typical needs of
Generative AI or other Machine Learning workloads,
so as to offer a low-boilerplate, ready-to-use set of
tools for seamless integration of Cassandra in
most AI-oriented applications.

CassIO is framework-agnostic: it does not know the specific
implementation details of interfaces of LangChain, Llamaindex
or any of the various toolkits built around Generative AI.
Rather, for each such framework, a set of "thin adapters" is built
that fits the interfaces of the framework while leveraging
the capabilities implemented in CassIO.

Here is a sketch of the relation between your application, an LLM
framework such as LangChain, and CassIO:

![CassIO, sketch](images/cassio_sketch.png)

### Latest status

CassIO is evolving rapidly. Note that at the time of writing

1. only LangChain is supported;
2. a fork of LangChain is needed (a PR to upstream is on its way).

As long as you follow the setup instructions we offer, this is easy and quick.
