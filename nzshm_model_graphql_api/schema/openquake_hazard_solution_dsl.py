from elasticsearch_dsl import (
    Document, Keyword, Text, Index,
    Date, Nested, InnerDoc,
    connections # noqa Date, Integer, 
)

from nzshm_model_graphql_api.config import ES_HOST

COMMON_INDEX = 'toshi_index'

# Define a default Elasticsearch client
connections.create_connection(hosts=ES_HOST)

class KeyValuePair(InnerDoc):
    k = Text(fields={'raw': Keyword()})
    v = Text(fields={'raw': Keyword()})

class OpenquakeHazardSolutionDocument(Document):
    '''Document schema - reverse engineered from raw object'''
    class Index:
        name = COMMON_INDEX

    id = Text({'raw': Keyword()})
    created = Date()
    config = Text({'raw': Keyword()})
    modified_config = Text({'raw': Keyword()})
    csv_archive = Text({'raw': Keyword()})
    hdf5_archive = Text({'raw': Keyword()})
    task_args = Text({'raw': Keyword()})
    produced_by = Text({'raw': Keyword()})
    clazz_name = Text({'raw': Keyword()})

    meta = Nested(KeyValuePair, field="meta")
