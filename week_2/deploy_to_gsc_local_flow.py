from prefect.deployments import Deployment
from etl_web_to_gcs import etl_to_gsc_parent_flow

deployment = Deployment.build_from_flow(
    flow = etl_to_gsc_parent_flow,
    name = "NY Taxi GSC"
)

deployment.apply()