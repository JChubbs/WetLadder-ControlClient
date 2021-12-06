import logging
import argparse

from CloudProviders.CloudManager import CloudManager

def main():
	logging.basicConfig(level=logging.INFO)

	parser = argparse.ArgumentParser(description="Configure and deploy WetLadder VPN Instance.")
	parser.add_argument("--creds", nargs="?", required=True, help="File containing the credentials of the desired Cloud Provider")
	parser.add_argument("--passphrase", nargs="?", required=True, help="Passphrase to be used by Certificate Authority managing VPN certificates")
	parser.add_argument("--instance_name", nargs="?", default="main_instance", help="Name of VPN instance to be created")
	parser.add_argument("--port", nargs="?", type=int, default=1194, help="Port for VPN Instance to be connected through")
	parser.add_argument("--udp", action="store_true", help="Use UDP instead of TCP")
	parser.add_argument("--client", nargs="?", required=True, help="Name of the client to be created")
	parser.add_argument("--target", nargs="?", default="WIN_64", help="Target OS/Architecture for client download")
	parser.add_argument("--client_path", nargs="?", default="./tmp", help="Target dir to output client folder")
	parser.add_argument("--obfs", nargs="?", default=None, help="Obfuscation method to be utilized")
	parser.add_argument("--obfs-port", nargs="?", default=1443, help="Port to have obfuscator listening on")

	args = parser.parse_args()
	
	proto = "udp" if args.udp else "tcp"
	
	cm = CloudManager()

	client = cm.get_config_client(args.creds)

	deployment = client.create_new_deployment()

	deployment.wait_until_deployed()

	deployment.create_instance(
		name=args.instance_name,
		port=args.port,
		proto=proto,
		ca_key_passphrase=args.passphrase
	)

	obfs_id = ""
	if args.obfs:
		resp = deployment.create_obfuscator(
			instance_id=args.instance_name,
			obfs_proto=args.obfs,
			port=args.obfs_port,
			proto=proto
		)

		obfs_id = resp["obfuscator_id"]

	#obfs client
	deployment.create_client(
		instance_id=args.instance_name,
		ca_key_passphrase=args.passphrase,
		client_name=args.client,
		obfuscator_id=obfs_id
	)

	deployment.get_client(
		instance_id=args.instance_name,
		client_name=args.client,
		target=args.target,
		out_location=args.client_path
	)

if __name__ == "__main__":
	main()