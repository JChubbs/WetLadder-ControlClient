from dataclasses import dataclass
from CloudProviders.deployment import Deployment

@dataclass
class AWSDeployment(Deployment):
	security_group_id: str
	ec2_instance: object