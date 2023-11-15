"""The main API schema."""

import logging

import graphene
import nzshm_model
from graphene import relay

log = logging.getLogger(__name__)

from .logic_tree import (
    LogicTree, LogicTreeBranchSet, LogicTreeBranch, 
    InversionSource, DistributedSource
)

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




class SeismicHazardModel(graphene.ObjectType):
    version = graphene.String()
    notes = graphene.String()
    source_logic_tree = graphene.Field(LogicTree)

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
                yield LogicTreeBranch(tag=str(branch.values), weight=branch.weight, uncertainty_models=get_sources(branch))

        def get_branch_sets(slt):
            for group in slt.fault_system_lts:
                yield LogicTreeBranchSet(
                    short_name=group.short_name, long_name=group.long_name, branches=get_branches(group)
                )

        return LogicTree(version=slt.version, title=slt.title, branch_sets=get_branch_sets(slt))


class SeismicHazardModelConnection(relay.Connection):
    class Meta:
        node = SeismicHazardModel

    total_count = graphene.Int()
