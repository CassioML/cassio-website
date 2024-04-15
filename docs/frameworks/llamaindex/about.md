# About LlamaIndex

[LlamaIndex](https://gpt-index.readthedocs.io/en/latest/index.html),
formerly GPT Index, is a Python data framework designed to manage and structure
LLM-based applications, with a particular emphasis on storage,
indexing and retrieval of data.

LlamaIndex provides a complete set of tools to automate tasks such as
data ingestion from heterogeneous sources (PDF files, Web pages, ...) and
retrieval-augmented generation (RAG); it also features a rich ecosystem of
plugins that make it possible to connect with third-party components,
from vector stores to data readers.

!!! info

    Most of the examples in this section can run straight away as Colab notebooks,
    provided you have checked the [pre-requisites](/start_here/#vector-database).

    If you prefer to run in local Jupyter, set up the
    [LlamaIndex Python environment](/frameworks/llamaindex/setup/) first.

## Available components

CassIO powers integration with LlamaIndex, making it possible to easily
develop LLM applications within this framework while taking advantage
of Astra DB / Cassandra as the storage system.

The following examples can be run either locally as Jupyter notebooks
(see the [local setup](/frameworks/llamaindex/setup/)
section for instructions) or directly as Colab
notebooks (look for the
<img src="/images/colab.png" style="height: 1.4em; vertical-align: middle;"/>
icon at the top of each page).

- Check out the [Vector Store Quickstart](/frameworks/llamaindex/vector-quickstart/) for a primer on creating and using a Vector Store on top of a Cassandra (vector-capable) database.
