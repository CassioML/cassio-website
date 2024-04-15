# About LangChain

[LangChain](https://docs.langchain.com/docs/) is a popular and rapidly evolving
framework to automate most of the management of, and interaction with, large language
models (LLMs): among its features are support for memory, vector-based similarity search,
an advanced prompt templating abstraction and much more.

LangChain comes with a Python and a Javascript implementation. This section
targets the Python version.

!!! info

    Most of the examples in this section can run straight away as Colab notebooks,
    provided you have checked the [pre-requisites](/start_here/#vector-database).

    If you prefer to run in local Jupyter, set up the
    [LangChain Python environment](/frameworks/langchain/setup/) first.

**Note** with the exception of the items marked as `[Preview]` below,
all other components are in the latest LangChain release and can be used
straight away after doing a `pip install langchain`. To allow experimenting with
the preview elements, however, the local environment setup will install
our preview fork of LangChain throughout. _You do not need to depart from_
`pip install langchain` _if you're not interested in the preview components._

## Available components

CassIO seamlessly integrates with LangChain, offering Cassandra-specific
tools for many tasks. Almost all of the following examples can run as Colab
notebooks straight away (look for the
<img src="/images/colab.png" style="height: 1.4em; vertical-align: middle;"/>
icon at the top of each page):

- A [memory module](/frameworks/langchain/memory-basic/) for LLMs that uses Cassandra for storage;
- ... that can be used to ["remember" the recent exchanges](/frameworks/langchain/memory-conversationbuffermemory/) in a chat interaction;
- ... including [keeping a summary](/frameworks/langchain/memory-summarybuffermemory/) of the whole past conversation.
- A facility for [caching LLM responses](/frameworks/langchain/caching-llm-responses/) on Cassandra, thereby saving on latency and tokens where possible.

Additionally, the "Vector Search" capabilities that are being added to Cassandra / Astra DB enables another set of "semantically aware" tools:

- A [cache of LLM responses](/frameworks/langchain/semantic-caching-llm-responses/) that is oblivious to the exact form a test is phrased.
- A ["semantic index"](/frameworks/langchain/qa-basic/) that can store a knowledge base and retrieve its relevant parts to buil the best answer to a given question ("QA use case");
- ... with support for [metadata filtering](/frameworks/langchain/qa-vector-metadata/) to narrow down vector similarity queries;
- ... whose usage can be [adapted](/frameworks/langchain/qa-advanced/) to suit many specific needs.
- ... and that can be configured to retrieve pieces of information [as diverse as possible](/frameworks/langchain/qa-maximal-marginal-relevance/) to maximize the actual information flowing to the answer.
- A ["semantic memory" element](/frameworks/langchain/memory-vectorstore/) for inclusion in LLM chat interactions, that can retrieve relevant past exchanges even if occurred in the far past.

Last, there is a set of components around zero-boilerplate prompt templating
using Cassandra as the source of data. Note: this is still in preview as of December 10th, 2023 and requires installation from the fork to be used.

- `[Preview]` Automatic [injection](/frameworks/langchain/prompt-templates-basic/) of data from Cassandra into a prompt;
- `[Preview]` Automatic injection of data [from a Feast feature store](/frameworks/langchain/prompt-templates-feast/) (e.g. backed by Cassandra) into a prompt.
- `[Preview]` A detour to look at the very [engine](/frameworks/langchain/prompt-templates-engine/) powering "database-bound prompt templates"... (useful to develop templates for automatic extraction of data from custom sources).


This list will grow over time as new needs are addressed
and the current extensions are refined.
