# API Setup

## Credentials file

In the repo root directory, create file `.api_keys` by copying
`.api_keys.template` and insert your valid credentials.

!!! note Available LLM Services

    Depending on which API Keys you define in the file,
    a different provider will be used as the source of
    the LLMs.

    Currently, only OpenAI is supported.

## API Setup completed.

The (optional) next is the [setup of the local Cassandra](/local_db_setup). to be able to use
the experimental features (Vector Similarity Search).

You can skip it and start browsing the code examples right now!