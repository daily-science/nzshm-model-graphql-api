import os

os.environ.setdefault("ANYSEARCH_PREFERRED_BACKEND", "Elasticsearch")

# from nzshm_model_graphql_api.schema.openquake_hazard_solution_dsl import OpenquakeHazardSolutionDocument
from nzshm_model_graphql_api.config import ES_HOST

from elasticsearch_dsl import Search
from elasticsearch_dsl import connections, Q

connections.create_connection(hosts=ES_HOST)

s = Search()
q1 = ~Q("term", meta__k="hazard_agg_target")
q2 = Q("term", clazz_name__keyword="OpenquakeHazardSolution")
# q3 = Q("term", produced_by__keyword="T3BlbnF1YWtlSGF6YXJkVGFzazo2NTI5NzI3")
s = s.query( q2 & q1)
# s = s.filter("term", meta__k="logic_tree_permutations")
# s = s.query('wildcard', meta__v="False")
# s = s.query('regexp', meta__v="enabled")
# s = s.query(Q('regexp', meta__v=False))
# s = s.query('regexp', meta__v="config")
# s = s.query('regexp', meta__v="{}")
# aggregate by month ...

s.aggs.bucket('solutions_per_month', 'date_histogram', field='created', interval='month')
    # .metric('solutions_per_month', 'count', field='id')

s = s.extra(explain=True, track_total_hits=True)

print('query')
print(s.to_dict())

s = s[:2]

response = s.execute()
print(f'Total {response.hits.total.value} hits found.' )

print( response.aggregations)
for bucket in response.aggregations.solutions_per_month.buckets:
    # print(bucket)
    # print(dir(bucket))
    print(bucket.key_as_string, bucket.doc_count)


for hit in response:
    print(hit, hit.created, hit.clazz_name) #, hit['meta'])