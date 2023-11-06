"""The main API schema."""

import logging

import graphene
import nzshm_model
from graphene import relay

log = logging.getLogger(__name__)


class TectonicRegionEnum(graphene.Enum):
    CRUSTAL = 'crustal'
    SUBDUCTION = 'subduction'
    INTERFACE = ' interface'


class SourceTypeEnum(graphene.Enum):
    Undefined = 99
    ScaledInversionSolution = 0
    AggregateInversionSolution = 10
    InversionSolution = 20
    # DistributedSourceModel = 30


class InversionSource(graphene.ObjectType):
    # tag = graphene.String()
    # notes = graphene.String()
    nrml_id = graphene.String()
    inversion_solution_id = graphene.String()
    rupture_set_id = graphene.String()
    source_type = graphene.Field(SourceTypeEnum)


class DistributedSource(graphene.ObjectType):
    nrml_id = graphene.String()


class SourceLogicTreeSource(graphene.Union):
    class Meta:
        types = (InversionSource, DistributedSource)


class SourceLogicTreeBranch(graphene.ObjectType):
    tag = graphene.String()
    weight = graphene.Float()
    sources = graphene.List(SourceLogicTreeSource)


class SourceLogicTreeGroup(graphene.ObjectType):
    short_name = graphene.String()
    long_name = graphene.String()
    tectonic_region = graphene.Field(TectonicRegionEnum)
    branches = graphene.List(SourceLogicTreeBranch)


class SourceLogicTree(graphene.ObjectType):
    version = graphene.String()
    title = graphene.String()

    # correlations
    groups = graphene.List(SourceLogicTreeGroup)


class SeismicHazardModel(graphene.ObjectType):
    version = graphene.String()
    notes = graphene.String()
    source_logic_tree = graphene.Field(SourceLogicTree)

    def resolve_source_logic_tree(root, info, **args):
        log.info("resolve_source_logic_tree:")
        model = nzshm_model.versions[root.version]
        slt = model.source_logic_tree()

        def get_sources(branch):
            if branch.onfault_nrml_id:
                st = branch.inversion_solution_type or 'Undefined'
                yield InversionSource(
                    inversion_solution_id=branch.inversion_solution_id,
                    nrml_id=branch.onfault_nrml_id,
                    rupture_set_id=branch.rupture_set_id,
                    source_type=SourceTypeEnum[st].value,
                )
            if branch.distributed_nrml_id:
                yield (DistributedSource(nrml_id=branch.distributed_nrml_id))

        def get_branches(group):
            for branch in group.branches:
                yield SourceLogicTreeBranch(tag=str(branch.values), weight=branch.weight, sources=get_sources(branch))

        def get_groups(slt):
            for group in slt.fault_system_lts:
                yield SourceLogicTreeGroup(
                    short_name=group.short_name, long_name=group.long_name, branches=get_branches(group)
                )

        return SourceLogicTree(version=slt.version, title=slt.title, groups=get_groups(slt))


class SeismicHazardModelConnection(relay.Connection):
    class Meta:
        node = SeismicHazardModel

    total_count = graphene.Int()
