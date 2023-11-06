"""
This module exports comfiguration for the current system
"""
import os


def boolean_env(environ_name, default='FALSE'):
    return bool(os.getenv(environ_name, default).upper() in ["1", "Y", "YES", "TRUE"])


IS_OFFLINE = boolean_env('SLS_OFFLINE')  # set by serverless-wsgi plugin
REGION = os.getenv('REGION', 'ap-southeast-2')
DEPLOYMENT_STAGE = os.getenv('DEPLOYMENT_STAGE', 'LOCAL').upper()
STACK_NAME = os.getenv('STACK_NAME', 'nshm_hazard_graphql_api')
LOGGING_CFG = os.getenv('LOGGING_CFG', './logging_aws.yaml')
ENABLE_METRICS = bool(os.getenv('ENABLE_METRICS', '').upper() in ["1", "Y", "YES", "TRUE"])
CW_METRICS_RESOLUTION = os.getenv('CW_METRICS_RESOLUTION', 60)  # 1 for high resolution or 60

ES_HOST = (
    'https://search-nzshm22-toshi-api-es-test-ybx3zlp6hz2shrytj2ns4zx6bm.ap-southeast-2.es.amazonaws.com'  # TOSHI_TEST
)
# ES_HOST = "https://search-nzshm22-toshi-api-es-prod-cj4taqcgnefophpxzan55xeswa.ap-southeast-2.es.amazonaws.com"
# # TOSHI_PROD
