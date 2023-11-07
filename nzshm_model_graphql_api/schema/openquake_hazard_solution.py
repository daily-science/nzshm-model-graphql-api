"""
This is a test of graphene-elastic API

We want to use ES query to find the relevant OpenquakeHazardSolution objects 
and subclass them based on their meta data.
"""

import graphene
from graphene import relay
import os

# import elasticsearch
# import elasticsearch_dsl

from graphene_elastic import (
    ElasticsearchObjectType,
    ElasticsearchConnectionField,
)

import datetime
from anysearch.search_dsl import (
    Boolean,
    connections,
    Completion,
    Date,
    Document,
    InnerDoc,
    Keyword,
    Nested,
    Text,
    Integer,
    Float,
    Index
)

from graphene_elastic.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    # HighlightFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
)
from graphene_elastic.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_TERM,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_IN,
)

from nzshm_model_graphql_api.config import ES_HOST
# Define a default Elasticsearch client
connections.create_connection(hosts=ES_HOST)


class KeyValuePair(InnerDoc):
    k = Text(fields={'raw': Keyword()})
    v = Text(fields={'raw': Keyword()})


class OpenquakeHazardSolutionDocumentPost(Document):
    '''Document schema - reverse engineered from raw object'''
    class Index:
        name = 'toshi_index'

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

# Object type definition
class OpenquakeHazardSolution(ElasticsearchObjectType):

    class Meta(object):
        document = OpenquakeHazardSolutionDocumentPost
        interfaces = (relay.Node,)

        filter_backends = [
            FilteringFilterBackend,
            SearchFilterBackend,
            # HighlightFilterBackend,
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
        ]

        # For `FilteringFilterBackend` backend
        filter_fields = {
            'clazz_name': {
                'field': 'clazz_name.keyword',
                'lookups': [
                    LOOKUP_FILTER_TERM,
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
            },
            'created': {
                'field:': 'created',
            },
        }

        search_fields = {
            'clazz_name': None,
            'produced_by': None,
        }

        ordering_fields =  {
            'created': 'created'
        }

        ordering_defaults = (
            '-created',  # Field name in the Elasticsearch document
        )        

    def resolve_meta(root, info, **args):
        """We must manually resolve this fieldname"""
        # log.info("resolve_meta:")
        for kvpair in root['meta']:
            yield KeyValuePair(k=kvpair['k'], v=kvpair['v'])

    # def resolve_id(root, info, **args):
    #     print(f'{root.clazz_name}_{root.id}')
    #     return root.id

# TEST
demo = """
query {
  all_openquake_hazard_solutions(
    first:5 
    search: {
      produced_by: {value:"T3BlbnF1YWtlSGF6YXJkVGFzazoxMDE0NDA="}
    }
    filter: {
      clazz_name: { value: "OpenquakeHazardSolution"}
      created: { 
        gt: {datetime:"2022-07-18T23:29:31.658767+00:00"}}
      } 
  ){
    pageInfo {
      hasNextPage
    }
    edges {
      cursor
      node 
      {
        id
        clazz_name
        csv_archive
        created
        produced_by 
        meta {
          k
          v
        } 
      }
    }
  }
}
"""