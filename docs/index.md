<img src="images/cassio_logo1_transparent.png" alt="CassIO logo" style="width: 30%;"/>

## Welcome to CassIO

Do you want to use [Apache Cassandra®](https://cassandra.apache.org) with your ML/LLM/GenAI workloads,
and **do you want to start NOW**?

This is the place for you.

## Installation and usage

Installing CassIO is as simple as

```
pip install cassio
```

However, most likely you will want to use third-party frameworks,
such as LangChain, that in turn _use_ CassIO.
Depending on how these frameworks are structured,
they may require CassIO upfront in their sub-dependencies
or you might have to manually install it.

!!! example

    A good example is the LangChain setup outlined [here](/frameworks/langchain/setup/):
    the LangChain framework itself does not list all of the packages
    it _might_ need and it is up to the user to pick, and install,
    those that will actually be needed by their application.
    In fact, you can see `cassio` being explicitly listed in the
    [requirements file](https://github.com/CassioML/cassio-website/blob/main/docs/frameworks/langchain/requirements_langchain.txt) for these demo notebooks.

## How to use this site

Don't just browse the website: you should clone the [repository](https://github.com/cassioML/cassio-website)
and start running the code examples yourself (notebooks, tutorials, full-fledged small applications).
You'll find everything in this repo.
You can also download a single notebook's code by clicking on the
"Download Notebook" icon at the top of each page
(<svg viewBox="0 0 24 24" style="height: 1.4em; vertical-align: middle;"><path d="M5 20h14v-2H5m14-9h-4V3H9v6H5l7 7 7-7Z"></path></svg>).

!!! Tip "Google Colaboratory"

    You can also run most of the code examples directly in Google Colaboratory
    ("Colab" for short) after a minimal amount of setup.

    Just create your Astra DB instance and get an API Key for an LLM provider
    and you're good to go. We will give Colab-specific setup instructions
    later on.

    If you want to run the examples in Colab, look for the
    "Open in Colab" icon at the top of the page
    (<img src="/images/colab.png" style="height: 1.4em; vertical-align: middle;"/>).

### General pre-requisites

Most code examples require a Cassandra / Astra DB database.
Out of convenience, in the [general setup instructions](/db_setup),
we show how to create a free Astra DB instance,
but of course you can use any Cassandra installation, provided you adapt
the few lines of code that connect to your database.

!!! info "Vector-search Cassandra"

    Some of the features rely on the "Vector Search"
    capabilities, which are being added to Cassandra right now,
    but have not yet made it to Cassandra official releases.

    If you want to use these, you have several options:
    you can make sure the Astra DB instance you create is
    a "Vector Database" (now in Public Preview), or you
    can build and run locally a version of Cassandra that implements
    these features from a pre-release branch.

    Keep reading to find out more.

Similarly, many of the examples need access to a third-party
service for LLMs and embeddings (for instance, Google's Vertex AI or OpenAI):
make sure you follow the [API setup](/api_setup) to configure the
necessary API Keys and other secrets for your provider of choice.

### Per-framework specific setup

We cover Cassandra integrations with several ML-centric tools and frameworks:
for each of them (a section of the site), there is a subdirectory with
explanations and examples.
In order to run locally the code examples you find there,
further, framework-specific setup instructions are given at the top
of the section: these mostly amount to creating a suitable Python environment
with the right dependencies, and not much else.


!!! example

    If you want to run the sample code for [LangChain](/frameworks/langchain/about/) follow these steps:

    1. clone [this repo](https://github.com/cassioML/cassio-website);
    2. do the [general DB setup](/db_setup);
    3. do the [local DB setup](/local_db_setup) if needed;
    4. do the [API setup](/api_setup);
    5. do the [LangChain-specific setup](/frameworks/langchain/setup/).

    At this point you can fire up Jupyter notebook and start running any of the
    provided notebooks.
    When moving on to testing another framework, only the last step will be needed.

    If you prefer to use Colab, instead, just create the Astra DB instance
    and obtain a valid Secret to an LLM provider - the online notebook
    will tell you what else is needed, if anything.

## CassIO repository

The source code is available at [this location](https://github.com/CassioML/cassio).
