"""The main API schema."""

import logging

import graphene
import nzshm_model
from graphene import relay

log = logging.getLogger(__name__)


class SourceLogicTree(graphene.ObjectType):
    version = graphene.String()
    notes = graphene.String()


class SeismicHazardModel(graphene.ObjectType):
    version = graphene.String()
    notes = graphene.String()

    source_logic_tree = graphene.Field(SourceLogicTree)

    def resolve_source_logic_tree(root, info, **args):
        log.info("resolve_source_logic_tree:")
        model = nzshm_model.versions[root.version]
        # print()
        # print(dir(model.source_logic_tree()))
        # print()
        # print(model.source_logic_tree())
        slt = model.source_logic_tree()

        return SourceLogicTree(version=slt.version, notes=slt.title)


class SeismicHazardModelConnection(relay.Connection):
    class Meta:
        node = SeismicHazardModel

    total_count = graphene.Int()
