# DB Setup

We show how to create an Astra DB instance and set the connection
details and secrets that all code examples can then use.

Astra DB is a serverless DBaaS by DataStax, built on Apache Cassandra, that offers
a free tier with generous traffic and storage limits. Using Astra DB frees you
from the hassle of running your own database, while retaining the advantages
of Cassandra such as data distribution and very high availability.

> Nothing prevents you from adapting the examples to any Cassandra cluster:
> in most cases all you have to do is to build the database `Session` object
> differently, and that's it. Inspect the code to find out: generally it's
> just a couple of lines to change.

### Create your Astra DB instance

...

### Create the `.env` file

Either by hand (+ scb download)

Or with `astra-cli`

### Import sample data

Some of the examples assume the presence of sample data in the database
to work properly as they are: follow these steps to pre-load the required
data in your database.

### Everything is set

Well done, you can now browse the website and run the code examples!