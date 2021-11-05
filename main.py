import logging

from CloudProviders.CloudManager import CloudManager

def main():
	logging.basicConfig(level=logging.INFO)

	cm = CloudManager()

	client = cm.get_config_client("aws.cfg")

	deployment = client.create_new_deployment()

if __name__ == "__main__":
	main()