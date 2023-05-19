# General setup for the LangChain examples

First clone the [repo](https://github.com/hemidactylus/langchain-cassio-examples) on your machine.

Create a virtualenv and pip-install the `requirements.txt` found in the repo.

**NOTE**: at the moment you need to do dev install of both a certain branch of LangChain and the `cassIO` library:

- clone `https://github.com/hemidactylus/cassio` and `pip install -e .`;
- clone `https://github.com/hemidactylus/langchain` _in the `cassio` branch_ and `pip install -e .`;

At the moment we support Astra DB only (going to change very soon).

Create a dot-env file as in the provided template, about your Astra DB instance.

Now, in the same console, first `. .env` and then `jupyter notebook`.
You can now experiment with the notebooks as in the other pages.