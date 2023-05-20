# Setup to run the LangChain examples

Make sure you did the [general setup](/db_setup/) first.

Go to `examples/langchain`.

Create a Python 3.8+ virtualenv and pip-install the `requirements_langchain.txt` found there.

**NOTE**: at the moment you need to do dev install of both a certain branch of LangChain and the `cassIO` library:

- clone `https://github.com/hemidactylus/cassio` and `pip install -e .`;
- clone `https://github.com/hemidactylus/langchain` _in the `cassio` branch_ and `pip install -e .`;

Now, in the same console, first `. ../.env` and then `jupyter notebook`.

You are now ready to run the notebooks.