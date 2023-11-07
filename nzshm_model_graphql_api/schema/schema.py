"""The main API schema."""

import logging

import graphene
import nzshm_model
from graphene import relay

import nzshm_model_graphql_api

from .seismic_hazard_model import SeismicHazardModel, SeismicHazardModelConnection
from .openquake_hazard_solution import OpenquakeHazardSolution

from graphene_elastic import ElasticsearchConnectionField

log = logging.getLogger(__name__)


class QueryRoot(graphene.ObjectType):
    """This is the entry point for graphql query operations"""

    node = relay.Node.Field()

    about = graphene.String(description='About this API ')

    def resolve_about(root, info, **args):
        return (
            f"Hello World, I am nzshm_model_graphql_api! Version: {nzshm_model_graphql_api.__version__}. "
            f"Using nzshm_model version: {nzshm_model.__version__}"
        )

    all_seismic_hazard_models = graphene.Field(SeismicHazardModelConnection, description="list the available models.")

    def resolve_all_seismic_hazard_models(root, info, **args):
        log.info("resolve_all_seismic_hazard_models:")

        nodes = [SeismicHazardModel(version=version) for version in nzshm_model.versions]

        edges = [SeismicHazardModelConnection.Edge(node=node) for idx, node in enumerate(nodes)]

        # REF https://stackoverflow.com/questions/46179559/custom-connectionfield-in-graphene
        connection_field = relay.ConnectionField.resolve_connection(SeismicHazardModelConnection, {}, edges)
        connection_field.total_count = len(edges)
        connection_field.edges = edges
        return connection_field

    seismic_hazard_model = graphene.Field(
        SeismicHazardModel,
        version=graphene.Argument(graphene.String, required=True, description="the version id for desired model"),
        description="Return a seismic_hazard_model.",
    )

    def resolve_seismic_hazard_model(root, info, version, **args):
        log.info('resolve_seismic_hazard_model args: %s version:%s' % (args, version))
        return SeismicHazardModel(version=nzshm_model.versions[version].version)

    # Query definition
    all_openquake_hazard_solutions = ElasticsearchConnectionField(OpenquakeHazardSolution)


schema_root = graphene.Schema(query=QueryRoot, mutation=None, auto_camelcase=False)
