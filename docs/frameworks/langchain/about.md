# About LangChain

[LangChain](https://docs.langchain.com/docs/) is a popular and rapidly evolving
framework to automate most of the management of, and interaction with, large language
models (LLMs): among its features are support for memory, vector-based similarity search,
an advanced prompt templating abstraction and much more.

LangChain comes with a Python and a Javascript implementation. These pages
target the Python version.

!!! info

    Most of the examples in this section can run straight away as Colab notebooks,
    provided you have checked the [pre-requisites](/start_here/#vector-database).

    If you prefer to run in local Jupyter, set up the
    [LangChain Python environment](/frameworks/langchain/setup/) first.

## Available components

CassIO seamlessly integrates with LangChain, offering Cassandra-specific
tools for many tasks. All of the following examples can run as Colab
notebooks straight away (look for the
<img src="/images/colab.png" style="height: 1.4em; vertical-align: middle;"/>
icon at the top of each page):

- A [Vector Store](/frameworks/langchain/qa-basic/) that can store a knowledge base and retrieve its relevant parts to build the best answer to a given question (the so-called RAG, or retrieval-augmented-generation, technique);
- ... with support for [metadata filtering](/frameworks/langchain/qa-vector-metadata/) to narrow down vector similarity queries;
- ... whose usage can be [adapted](/frameworks/langchain/qa-advanced/) to suit many specific needs.
- ... and that can be configured to retrieve pieces of information [as diverse as possible](/frameworks/langchain/qa-maximal-marginal-relevance/) to maximize the actual information flowing to the answer.
- A [memory module](/frameworks/langchain/memory-basic/) for LLMs that uses Cassandra for storage;
- ... that can be used to ["remember" the recent exchanges](/frameworks/langchain/memory-conversationbuffermemory/) in a chat interaction;
- ... including [keeping a summary](/frameworks/langchain/memory-summarybuffermemory/) of the whole past conversation.
- ... and a ["semantic memory" element](/frameworks/langchain/memory-vectorstore/), for inclusion in LLM chat interactions, that can retrieve relevant past exchanges even if occurred in the far past.
- A facility for [caching LLM responses](/frameworks/langchain/caching-llm-responses/) on Cassandra, thereby saving on latency and tokens where possible.
- ... and a semantic [version of the LLM cache](/frameworks/langchain/semantic-caching-llm-responses/), oblivious to the exact form a text is phrased.

<!-- - `[Preview]` Automatic [injection](/frameworks/langchain/prompt-templates-basic/) of data from Cassandra into a prompt;
- `[Preview]` Automatic injection of data [from a Feast feature store](/frameworks/langchain/prompt-templates-feast/) (e.g. backed by Cassandra) into a prompt.
- `[Preview]` A detour to look at the very [engine](/frameworks/langchain/prompt-templates-engine/) powering "database-bound prompt templates"... (useful to develop templates for automatic extraction of data from custom sources).
 -->