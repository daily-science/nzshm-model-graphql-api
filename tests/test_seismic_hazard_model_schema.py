"""Tests for `nzshm_model_graphql_api` package."""

import unittest
from graphene.test import Client

from nzshm_model_graphql_api.schema import schema_root


class TestSeismicHazardModel(unittest.TestCase):
    def setUp(self):
        self.client = Client(schema_root)

    def test_seismic_hazard_model(self):
        QUERY = """
        query {
            seismic_hazard_model(version:"NSHM_v1.0.4") {
                version
                notes
                source_logic_tree {
                    version
                    title
                }
            }
        }
        """

        executed = self.client.execute(QUERY)
        print(executed)
        self.assertTrue(
            'corrected fault geometry' in executed['data']['seismic_hazard_model']['source_logic_tree']['title']
        )

    def test_all_seismic_hazard_models(self):
        QUERY = """
        query {
            all_seismic_hazard_models {
                total_count
                edges {
                node {
                    notes
                    version
                        source_logic_tree {
                            version
                            title
                        }
                    }
                }
            }
        }
        """
        executed = self.client.execute(QUERY)
        print(executed)
        self.assertTrue(len(executed['data']['all_seismic_hazard_models']['edges']) == 2)
        self.assertTrue(executed['data']['all_seismic_hazard_models']['total_count'] == 2)
