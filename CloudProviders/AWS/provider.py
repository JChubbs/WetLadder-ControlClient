import boto3
import uuid
import time
import logging

from CloudProviders.CloudProvider import CloudProvider
from CloudProviders.AWS.deployment import AWSDeployment

class AWSProvider(CloudProvider):

	def __init__(self, config_values):
		# aws needs access key and secret key - will fail if not provided
		#(don't feel like catching for custom failure state, blegh)
		self.access_key = config_values["aws_access_key_id"]
		self.secret_key = config_values["aws_secret_access_key"]
		self.aws_region = config_values["aws_region"]

		self.ec2_resource = boto3.resource(
			"ec2",
			aws_access_key_id=self.access_key,
			aws_secret_access_key=self.secret_key,
			region_name=self.aws_region
			#aws_session_token
		)

		self.ec2_client = boto3.client(
			"ec2",
			aws_access_key_id=self.access_key,
			aws_secret_access_key=self.secret_key,
			region_name=self.aws_region
			#aws_session_token
		)

	def create_new_deployment(self):
		logging.info("Creating new deployment")
		#create security group
		security_group = self._create_security_group()

		#user_data is pretty much just commands run on start?
		with open("./CloudProviders/AWS/user-data.sh", "r") as user_data_file:
			user_data = user_data_file.read()

		#create ec2 instance
		instance = self.ec2_resource.create_instances(
			ImageId="ami-087c17d1fe0178315", #Amazon Linux
			InstanceType="t2.micro",
			MinCount=1,
			MaxCount=1,
			SecurityGroupIds=[
				security_group.id
			],
			UserData=user_data,
		)

		deployment = AWSDeployment(
			security_group = security_group,
			ec2_instance = instance[0]
		)

		#open port needed for rest api
		deployment.open_port(5000, "tcp")

		logging.info(f"New deployment created - deployment_id = {deployment.ec2_instance.id}")
		return deployment

	def delete_deployment(self, deployment):
		deployment.ec2_instance.terminate()

	def _create_security_group(self):
		resp = self.ec2_client.create_security_group(
			Description="WetLadded deployment security group",
			GroupName=f"Wetladder - {str(uuid.uuid1())}"
		)
		security_group = self.ec2_resource.SecurityGroup(resp["GroupId"])

		logging.info(f"Security Group created - GroupId = {security_group.id}")
		return security_group