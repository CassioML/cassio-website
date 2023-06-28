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

- [OpenAI](https://openai.com/). In this case you will be asked for a valid API Key.
- [GCP Vertex AI](https://cloud.google.com/vertex-ai). In this case you need a JSON API for a Service Account whose permissions include the Vertex AI API.
- [Azure OpenAI](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/). In this case you will need several parameters: the base URL to your Azure OpenAI resource, the API version string, an API Key, and the deployment and model name for both the LLM and the embedding models.

See the inserts below for more information on each provider.

??? info "OpenAI"

    Log in with [OpenAI](https://openai.com/) (creating an account if you haven't yet).

    By visiting the [API Keys](https://platform.openai.com/account/api-keys) page
    in your user account, you will be able to generate an API Key. Make sure to
    copy it and store it in a safe place.

    ![OpenAI API Keys page](images/services/openai-api-key.png)

??? info "GCP Vertex AI"

    In order to use Google's Vertex AI service, you need an [account](https://cloud.google.com/vertex-ai)
    with access to that service. 

    Once you log in, go to the [API Credentials Console](https://console.cloud.google.com/apis/credentials), make sure the right project is selected, and click "Create Credentials".

    ![GCP Vertex AI Credentials Console](images/services/vertexai-api-key-1.png)

    Choose to generate a "Service account" and fill the wizard, then hit "Done".

    ![GCP Vertex AI, Creating Service Account](images/services/vertexai-api-key-2.png)

    The new service account will be visible in the "Credentials" list. Click the "edit" symbol
    next to it, then go to the "Keys" tab for this account.

    ![GCP Vertex AI, Edit Service Account](images/services/vertexai-api-key-3.png)

    There will be no keys yet:
    click "Add Key" to create a new one and make it of "JSON" type. You will be prompted to
    save the JSON key file. **Save it on your computer in a safe place, as it will not be
    made available again.**

    ![GCP Vertex AI, Create JSON Key](images/services/vertexai-api-key-4.png)

    That's it: the full path to the JSON key is the required secret for Vertex AI.

??? info "Azure OpenAI"

    To use LLMs and embedding services from Azure OpenAI, you first need to create
    a "Resource" in OpenAI Studio and deploy the desired models in it.
    Next, you retrieve the secrets and connection parameters needed for
    programmatic API access.

    First you need an Azure account allowed to access
    the [Azure OpenAI](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/) service.

    Log in to the [Azure Portal](portal.azure.com) and choose the "Azure OpenAI" service
    in the dashboard.

    ![Azure OpenAI Service](images/services/azure-openai-api-key-1.png)

    You will see a list of "Resources" (initially empty). Click "Create" and fill
    the "Create Azure OpenAI" wizard. (You may need to create a "Resource Group"
    if you don't have one already.)

    ![Azure OpenAI, Create a Resource](images/services/azure-openai-api-key-2.png)

    Confirm the process by clicking "Create" at the end of the wizard.

    ![Azure OpenAI, Resource Creation Wizard](images/services/azure-openai-api-key-3.png)

    After a few minutes with "Deployment in progress...", you will see
    "Your deployment is complete". You can click "Go to resource".

    ![Azure OpenAI, Go to Resource](images/services/azure-openai-api-key-4.png)

    Now, you can "Deploy" a model in your newly-created resource.

    ![Azure OpenAI, Deploy a Model](images/services/azure-openai-api-key-5.png)

    The current deployment list is empty: click "Create new deployment" and pick
    the model you want. Notice that to have _both an LLM and an embedding model_
    you have to do _two separate deployments_. **Take note of the exact
    deployment name (which you freely choose) and of the model name
    (chosen from a list)**, as these will be needed among the connection parameters.

    Your models should now be available. To retrieve the connection parameters,
    start from the [Azure OpenAI Studio](https://oai.azure.com/portal) and click
    on the "Playground/Chat" item in the left navigation bar.

    Locate the "View code" button at the top of the "Chat session" panel and
    click on it.

    ![Azure OpenAI, Chat Playground](images/services/azure-openai-api-key-6.png)

    A dialog will be shown (make sure that Python code is
    the selected option), where you will find the remaining
    connection parameters: the API Version, the "API Base"
    (an URL to your resource), and the API Key (shown as masked copyable text box).

    ![Azure OpenAI, View-Code Dialog](images/services/azure-openai-api-key-7.png)

    This is it: keep the connection parameters you just collected, as you will
    have to supply them to run the examples.


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