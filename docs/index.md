<img src="images/cassio_logo1_transparent.png" alt="CassIO logo" style="width: 30%;"/>

## Welcome to CassIO

Do you want to use [Apache Cassandra®](https://cassandra.apache.org) with your ML/LLM/GenAI workloads,
and **do you want to start NOW**?

This is the place for you.

## How to use this site

Don't just browse the website: you should clone the [repository](https://github.com/cassioML/cassio-website)
and start running the code examples yourself (notebooks, tutorials, full-fledged small applications).
You'll find everything in this repo.

### General pre-requisites

Most code examples require a Cassandra / Astra DB database.
In the [general setup instructions](/db_setup), we show how to create a free Astra DB instance out of convenience,
but of course you can use any Cassandra installation, provided you adapt
the few lines of code that connect to your database.

Similarly, many of the examples need access to third-party
services such as LLMs provided by OpenAI: make sure you
follow the [API setup](/api_setup) to configure the necessary API Keys
and other secrets.

### Per-framework specific setup

We cover Cassandra integrations with several ML-centric tools and frameworks:
for each of them (a section of the site), there is a subdirectory with
explanations and examples. The code there is stand-alone, provided you
did the general setup (see above): but usually you have first to
go through a framework-specific setup (covering e.g. the setup
of a suitable Python environment with the right dependencies),
described at the top of the section.

!!! example

    If you want to run the sample code for [LangChain](/frameworks/langchain/about/) follow these steps:

    1. clone [this repo](https://github.com/cassioML/cassio-website);
    2. do the [general DB setup](/db_setup);
    3. do the [API setup](/api_setup);
    4. do the [LangChain-specific setup](/frameworks/langchain/setup/).

    At this point you can fire up Jupyter notebook and start running any of the
    provided notebooks.
    When moving on to testing another framework, only the last step will be needed.