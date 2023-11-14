"""Tests for `nzshm_model_graphql_api` package."""

import os
import unittest
from pathlib import Path

from graphene.test import Client

import nzshm_model_graphql_api
from nzshm_model_graphql_api.schema import schema_root
from nzshm_model_graphql_api.api import create_app

os.environ.setdefault("ANYSEARCH_PREFERRED_BACKEND", "Elasticsearch")

class TestFlaskApp(unittest.TestCase):
    """Tests the basic app create."""

    def test_create_app(self):
        app = create_app()
        print(app)
        assert app


class TestSchemaAboutResolver(unittest.TestCase):
    """
    A simple `About` resolver returns some metadata about the API.
    """

    def setUp(self):
        self.client = Client(schema_root)

    def test_get_about(self):

        QUERY = """
        query {
            about
        }
        """

        executed = self.client.execute(QUERY)
        print(executed)
        self.assertTrue('Hello World' in executed['data']['about'])

    def test_get_about_has_version(self):

        QUERY = """
        query {
            about
        }
        """

        executed = self.client.execute(QUERY)
        print(executed)
        self.assertTrue(nzshm_model_graphql_api.__version__ in executed['data']['about'])


class TestSetup(unittest.TestCase):
    def test_no_logging_config(self):
        config = Path(os.getenv('LOGGING_CFG', 'nzshm_model_graphql_api/logging.yaml'))
        assert config.is_file()
        ren_config = config.rename(config.with_suffix('.txt'))

        app = create_app()
        print(app)
        assert app

        ren_config.rename(config)

        self.client = Client(schema_root)

        ## TODO assert "Warning, no logging config found, using basicConfig(INFO)" in stdout"
