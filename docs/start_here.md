CassIO is designed to power several LLM frameworks. In the following,
you will see it in action within one such framework,
[LangChain](https://docs.langchain.com/docs/).
You will run a short question-answering (QA) example, whereby an input corpus of text
is first inserted into a Vector Search database index and then, for a given
"user question", queried to retrieve the relevant subdocuments and construct an
answer to the question.

The quickstart is designed to run out-of-the-box as a notebook in
Google Colaboratory ("Colab" for short)
and to use Astra DB as the Vector Database.

??? tip "Other ways to run the code"

    The following will guide you through running your own QA pipeline in LangChain.

    Feel free to look around for other examples and use cases: all you need is
    a database and access to an LLM provider (as shown through the rest of this page).

    If you prefer, however, you can run the very same examples using Jupyter on your
    machine instead of Colab: only the setup is a bit different. Check the
    ["Further Reading"](/more_info/) section for details.

    We suggest to use a cloud database on DataStax Astra DB, which
    currently offers Vector Search capabilities in Public Preview.
    Should you prefer to run a local Cassandra cluster equipped with that feature,
    you can definitely do that -- but bear in mind that Vector Search has not made
    it to official Cassandra releases, hence you'll have to build a pre-release
    from source code. We'll outline the process in the ["Further Reading"](/more_info/) section
    for your convenience.

We'll come to the code in a moment;
first, let's check the pre-requisites needed to run the examples.

## Vector Database

Create your Vector Database with Astra DB: it's free, quick and easy.

??? info "What is Astra DB?"

    Astra DB is a serverless DBaaS by DataStax, built on Apache Cassandra. It offers
    a free tier with generous traffic and storage limits. Using Astra DB frees you
    from the hassle of running your own cluster while retaining all the advantages, such as the excellent data distribution and very high availability that make Cassandra a world-class NoSQL database.

### Create the Database

Go to [astra.datastax.com](https://astra.datastax.com) and sign up.

Click "Create Database" and _make sure to select_ "Serverless with Vector Search".

In the following we assume you called the database `cassio_db`.
You will also be asked for a "Keyspace name" when creating the database:
you can call it something like `cassio_tutorials` for example.
(A keyspace is simply a way to keep related tables grouped together.)

In a couple of minutes your database will be in the "Active" state, as
shown in the DB Quickstart page.

Detailed explanations can be found
[at this page](https://awesome-astra.github.io/docs/pages/astra/create-instance/).

### Database Access Token

Now you need credentials to connect securely to your database.

On the DB Quickstart panel, locate the "Create a custom token" link
and generate a new token **with role "Database Administrator"**. _Make sure you
safely store all parts of the Token, as you won't be shown
them anymore for security reasons._

Detailed information on DB Tokens can be found
[here](https://awesome-astra.github.io/docs/pages/astra/create-token/).

### Database Secure Connect Bundle

Next, you need a "Secure Connect Bundle" zipfile, containing certificates
and routing information for the drivers to properly establish a connection to
your database.

On the DB Quickstart panel, find the "Get Bundle" button and click on it.
You don't need to unpack the zip file, just save it on you computer: you
will need it momentarily.

For more info on the Secure Connect Bundle
see [this page](https://awesome-astra.github.io/docs/pages/astra/download-scb/#c-procedure).

## LLM Access

In order to run the quickstart, you should have access to an LLM.
You will be asked to provide the appropriate access secrets in order to run
the full code example: make sure you have them ready.

The notebooks currently support the following providers for LLMs:

- [OpenAI](https://openai.com/). In this case you will be asked for a valid API Key;
- [GCP VertexAI](https://cloud.google.com/vertex-ai). In this case you need a JSON API for a Service Account whose permissions include the VertexAI API.

## Run the quickstart

Once you have the Token and the Secure Connect Bundle,
and the secrets required to use an LLM, click on the Colab Notebook link below
to start using your Vector Search Database in the LangChain QA example:

<p align="center">
  <a href="http://colab.research.google.com/github/CassioML/cassio-website/blob/main/docs/frameworks/langchain/.colab/colab_qa-basic.ipynb" target="blank;">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" style="height: 2.0em; vertical-align: middle;"/>
  </a>
</p>

## What now?

Now you have first-hand experience on how easily you can power
up your application with Vector Search capabilities.

Check out other use cases which benefit from Vector Search, and other ways to
enrich your application with LangChain and Cassandra, by browsing the
[LangChain section](/frameworks/langchain/about/) of the site.

Look for the Colab
<img src="/images/colab.png" style="height: 1.4em; vertical-align: middle;"/>
symbol at the top of most code examples.

As mentioned at the top of this page, CassIO is designed as a general-usage
library: and, sure enough, we will offer integrations with other frameworks,
such as Llamaindex or Microsoft Semantic Kernel.

Come back and check again in a few days for more!