from elasticsearch_dsl import Document, Keyword, Text, Index, connections # noqa Date, Integer, 

import nzshm_model
from nzshm_model_graphql_api.config import ES_HOST

COMMON_INDEX = 'toshi_nzshm_model_graphql_api_index'
models_index = Index(COMMON_INDEX)
models_index.settings(number_of_shards=1, number_of_replicas=0)


# Define a default Elasticsearch client
connections.create_connection(hosts=ES_HOST)
# connections.create_connection(hosts="http://localhost:9200",
#     verify_certs=False,
#     connection_class=RequestsHttpConnection
# )


class SeismicHazardModelDocument(Document):
    version = Text(fields={'raw': Keyword()})
    notes = Text(fields={'raw': Keyword()})

    clazz_name = Text(fields={'raw': Keyword()})

    class Index:
        name = COMMON_INDEX

    def save(self, **kwargs):
        return super(SeismicHazardModelDocument, self).save(**kwargs)


# create the mappings in elasticsearch
SeismicHazardModelDocument.init()

# create and save and article
print(dir(nzshm_model.versions))
for key, model in nzshm_model.versions.items():
    # model = nzshm_model.get_version(key)
    doc = SeismicHazardModelDocument(
        _id=f'SeismicHazardModel_{model.version}',
        # node_id == base64.uuencode(_id)
        clazz_name='SeismicHazardModel',
        version=model.version,
        notes=model.title,
    )
    doc.save()

# article = Article.get(id=42)
# print(article.is_published())

# Display cluster health
print(connections.get_connection().cluster.health())
