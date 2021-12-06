import os

from CloudProviders.AWS.provider import AWSProvider

class CloudManager():

	providers = {
		"AWS": AWSProvider
	}

	def check_valid_config(self, config):
		print(config)
		return os.path.exists(config)

	def load_config(self, config):
		with open(config, "r") as conf_file:
			contents = conf_file.readlines()

		values = {i.split("=")[0].strip("\n"): i.split("=")[1].strip("\n") for i in contents if "=" in i}

		return values

	def get_config_client(self, config):
		if not self.check_valid_config(config):
			raise Exception("Invalid config file!")

		set_config = self.load_config(config)

		if not set_config.get("provider") in self.providers:
			raise Exception(f"Invalid provider {set_config.get('provider')} in config file {config}")

		return self.providers.get(set_config.get("provider"))(set_config)
