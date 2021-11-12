from Deployment.Deployment import Deployment

import logging

class AWSDeployment(Deployment):
	security_group: str
	ec2_instance: object

	def __init__(self, 
		security_group: object, 
		ec2_instance: object
		):

		self.security_group = security_group
		self.ec2_instance = ec2_instance

		logging.info("Waiting for Instance to enter \"Running\" state")
		self.ec2_instance.wait_until_running()
		self.ec2_instance.reload()
		self.location = self.ec2_instance.public_dns_name

	def open_port(self, 
		port: int, #port to open
		proto: str #protocol to open port for
		):

		self.security_group.authorize_ingress(
			IpProtocol=proto,
			CidrIp="0.0.0.0/0", #allow connection from anywhere
			FromPort=port,
			ToPort=port
		)


	def close_port(self,
		port: int, #port to close
		proto: str #protocol to close port for
		):
		self.security_group.revoke_ingress(
			IpProtocol=proto,
			CidrIp="0.0.0.0/0", #allow connection from anywhere
			FromPort=port,
			ToPort=port
		)