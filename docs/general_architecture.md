# General Architecture of CassIO

CassIO simplifies accessing the Cassandra database for Generative AI and other Machine Learning tasks. Its convenient tools require minimal setup and can easily be integrated into most AI-based applications. 

CassIO is adaptable to various frameworks, utilizing "thin adapters" tailored to fit the particular interfaces of each framework while taking advantage of the features offered by CassIO. As a mediator between your application, a framework like LangChain or Llamaindex, and the Cassandra database, CassIO is the optimal solution for efficient and effective data management.

![CassIO, sketch](images/cassio_sketch.png)

### Latest status

CassIO is evolving rapidly. Note that at the time of writing

1. only LangChain is supported;
2. a fork of LangChain is needed (a PR to upstream is on its way).

As long as you follow the setup instructions we offer, this is easy and quick.
