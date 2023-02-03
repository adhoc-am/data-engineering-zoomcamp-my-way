from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from etl_web_to_gcs import etl_to_gsc_parent_flow

deployment = Deployment.build_from_flow(
    flow = etl_to_gsc_parent_flow, 
    name = "NY Taxi GSC",
    path = "week2/etl_web_to_gcs.py",
    storage = GitHub.load("dez-github-repo")
    
)
deployment.apply()