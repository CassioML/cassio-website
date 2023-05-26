# API Setup

## Credentials file

In the repo root directory, create file `.api_keys` by copying
`.api_keys.template` and insert your valid credentials.

!!! note Available LLM Services

    Depending on which API Key you define in the file,
    you will be able to use certain providers
    for your LLM services.

    Currently, OpenAI and Google VertexAI are supported.

The notebooks use a simple utility to choose the provider
automatically based on the credentials available, but you can
override this choice at any time. The (few) lines of code that
actually instantiate the LLM objects are in the notebooks for
maximum clarity.

## API Setup completed.

The (optional) next is the [setup of the local Cassandra](/local_db_setup). to be able to use
the experimental features (Vector Similarity Search).

You can skip it and start browsing the code examples right now!