import logging

from CloudProviders.CloudManager import CloudManager

def main():
	logging.basicConfig(level=logging.INFO)

	cm = CloudManager()

	client = cm.get_config_client("aws.cfg")

	deployment = client.create_new_deployment()

	deployment.wait_until_deployed()

	deployment.create_instance(
		name="main_instance",
		port=1234,
		proto="udp",
		ca_key_passphrase="secret"
	)


if __name__ == "__main__":
	main()