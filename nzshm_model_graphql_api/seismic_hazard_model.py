"""The main API schema."""

import logging

import graphene
from graphene import relay

log = logging.getLogger(__name__)


class SeismicHazardModel(graphene.ObjectType):
    version = graphene.String()
    notes = graphene.String()


class SeismicHazardModelConnection(relay.Connection):
    class Meta:
        node = SeismicHazardModel

    total_count = graphene.Int()
