# About LangChain

[LangChain](https://docs.langchain.com/docs/) is a popular and rapidly evolving
framework to automate most of the management of and interaction with large language
models: among its features are support for memory, vector-based similarity search,
an advanced prompt templating abstraction and much more.

LangChain comes with a Python and a Javascript implementation. This section
targets the Python version.

!!! info

    To be able to run the examples below, first go through the
    [LangChain-specific setup instructions](/frameworks/langchain/setup/).

## Available components

CassIO seamlessly integrates with LangChain, offering Cassandra-specific
tools for the following tasks:

- Automatic [injection](/frameworks/langchain/prompt-templates-basic/) of data from Cassandra into a prompt;
- ... the same, as part of a [longer LLM conversation](/frameworks/langchain/chat-prompt-templates/).
- Support for ["partialing" of prompts](/frameworks/langchain/prompt-templates-partialing/) (i.e. leaving some input unspecified, to supply later).
- Automatic injection of data [from a Feast feature store](/frameworks/langchain/prompt-templates-feast/) (e.g. backed by Cassandra) into a prompt.
- A [memory module](/frameworks/langchain/memory-basic/) for LLMs that uses Cassandra for storage;
- ... that can be used to ["remember" the recent exchanges](/frameworks/langchain/memory-conversationbuffermemory/) in a chat interaction;
- ... including [keeping a summary](/frameworks/langchain/memory-summarybuffermemory/) of the whole past conversation.
- A facility for [caching LLM responses](/frameworks/langchain/caching-llm-responses/) on Cassandra, thereby saving on latency and tokens where possible.

Additionally, the "Vector Search" capabilities that are being added to Cassandra / Astra DB enables another set of "semantically aware" tools:

- A [cache of LLM responses](/frameworks/langchain/semantic-caching-llm-responses/) that is oblivious to the exact form a test is phrased.
- A ["semantic index"](/frameworks/langchain/qa-basic/) that can store a knowledge base and retrieve its relevant parts to buil the best answer to a given question ("Q&A use case");
- ... whose usage can be [adapted](/frameworks/langchain/qa-advanced/) to suit many specific needs.
- ... and that can be configured to retrieve pieces of information [as diverse as possible](/frameworks/langchain/qa-maximal-marginal-relevance/) to maximize the actual information flowing to the answer.
- A ["semantic memory" element](/frameworks/langchain/memory-vectorstore/) for inclusion in LLM chat interactions, that can retrieve relevant past exchanges even if occurred in the far past.

This list will grow over time as new needs are addressed
and the current extensions are refined.