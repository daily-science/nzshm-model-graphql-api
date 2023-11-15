import logging

import graphene

"""
    <logicTree logicTreeID='lt1'>
            <logicTreeBranchSet uncertaintyType="gmpeModel" branchSetID="bs_crust"
                    applyToTectonicRegionType="Active Shallow Crust">

                    <logicTreeBranch branchID="STF22_upper">
                <uncertaintyModel>[Stafford2022]
                  mu_branch = "Upper" </uncertaintyModel>
                <uncertaintyWeight>0.117</uncertaintyWeight>
                    </logicTreeBranch>
"""

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


class LogicTreeBranch(graphene.ObjectType):
    tag = graphene.String()
    weight = graphene.Float()
    uncertainty_models = graphene.List('nzshm_model_graphql_api.schema.logic_tree.UncertaintyModel')


class LogicTreeBranchSet(graphene.ObjectType):
    short_name = graphene.String()
    long_name = graphene.String()
    tectonic_region = graphene.Field(TectonicRegionEnum)
    branches = graphene.List(LogicTreeBranch)


class LogicTree(graphene.ObjectType):
    # logic_tree_id = graphene.String()
    version = graphene.String()
    title = graphene.String()

    branch_sets = graphene.List(LogicTreeBranchSet)

    # correlations are not covered withing NRML


class InversionSource(graphene.ObjectType):
    # tag = graphene.String()
    # notes = graphene.String()
    nrml_id = graphene.String(description="API nodeId for the NRML resource.")
    inversion_solution_id = graphene.String(description="API nodeId for the InversionSolution.")
    rupture_set_id = graphene.String(description="API nodeId for the RuptureSet.")
    source_type = graphene.Field(SourceTypeEnum)

class DistributedSource(graphene.ObjectType):
    nrml_id = graphene.String(description="API nodeId for the NRML resource.")

class GroundMotionPredictionEquation(graphene.ObjectType):
    nrml_id = graphene.String(description="API nodeId for the NRML resource.") 

class UncertaintyModel(graphene.Union):
    """
    An abstract class for the 'leaf' object of a LogicTree.

    NSHM differs from NRML as we use explicit Types
    """
    class Meta:
        types = (InversionSource, DistributedSource, GroundMotionPredictionEquation)
