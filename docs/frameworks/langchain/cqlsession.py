import os
from dotenv import find_dotenv, load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# this will climb the directory tree looking for the file
dotenv_file = find_dotenv('.env')
load_dotenv(dotenv_file)

ASTRA_DB_SECURE_BUNDLE_PATH = os.environ["ASTRA_DB_SECURE_BUNDLE_PATH"]
ASTRA_DB_CLIENT_ID = "token"
ASTRA_DB_APPLICATION_TOKEN = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_KEYSPACE = os.environ["ASTRA_DB_KEYSPACE"]

def getCQLSession():
    cluster = Cluster(
        cloud={
            "secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH,
        },
        auth_provider=PlainTextAuthProvider(
            ASTRA_DB_CLIENT_ID,
            ASTRA_DB_APPLICATION_TOKEN,
        ),
    )
    astraSession = cluster.connect()
    return astraSession

def getCQLKeyspace():
    return ASTRA_DB_KEYSPACE

# def getLocalCassandraSession():
#     # A session to a locally-running Cassandra
#     cluster = Cluster()
#     localSession = cluster.connect()
#     return localSession
