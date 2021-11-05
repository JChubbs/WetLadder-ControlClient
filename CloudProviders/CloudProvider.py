import abc

class CloudProvider(object):
	__metaclass__ = abc.ABCMeta

	commands = [
		"git clone https://github.com/JChubbs/WetLadder-Server",
		"cd WetLadder-Server",
		"make setup",
		"nohup python3 run.py &"
	]

	@abc.abstractmethod
	def __init__(self, config_values):
		return

	@abc.abstractmethod
	def create_new_deployment(self):
		return

	@abc.abstractmethod
	def delete_deployment(self, deployment):
		return

	@abc.abstractmethod
	def deploy_wetladder_server(self, deployment):
		return

	@abc.abstractmethod
	def open_deployment_port(self, deployment, port_num, port_proto):
		return

	@abc.abstractmethod
	def close_deployment_port(self, deployment, port_num, port_proto):
		return