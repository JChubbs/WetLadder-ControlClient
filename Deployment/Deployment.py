import abc
import requests
import time
import logging
import json

class Deployment(object):
	__metaclass__ = abc.ABCMeta

	location: str

	app_port = 5000

	request_options = {
		"verify": False #for now disable ssl verification - at some point the public key needs to be passed to client
	}

	@abc.abstractmethod
	def __init__(self):
		pass

	@abc.abstractmethod
	def open_port(self, 
		port: int, #port to open
		proto: str #protocol to open port for
		):
		pass

	@abc.abstractmethod
	def close_port(self,
		port: int, #port to close
		proto: str #protocol to close port for
		):
		pass

	def wait_until_deployed(
		self,
		delay: int = 30, #30 seconds
		timeout: int = 300 #5 minutes
		):

		logging.info(f"Waiting for deployment to complete @ {self.location}")

		timeout_time = time.time() + timeout

		#TODO change to health check endpoint
		while time.time() <= timeout_time:
			try:
				resp = requests.get(f"https://{self.location}:{self.app_port}/instances", **self.request_options) 
				if resp.status_code == 200:
					logging.info(f"Successfully finished deployment @ {self.location}")
					return True
				else:
					raise Exception(f"Invalid response code returned by {self.location} {resp.status_code}")
			except requests.exceptions.RequestException:
				logging.info("Still Deploying! Trying again!")
				time.sleep(delay)
				continue

		raise Exception(f"Deployment of @ {self.location} took too long to start!")

	def create_instance(
		self,
		name: str, #name for instance, must be unique
		port: int, #port number to access instance through
		proto: str, #either tcp or udp - used to communicate with instance
		ca_key_passphrase: str #passphrase used by instances CA
		):

		body = {
			"name": name,
			"port": port,
			"proto": proto,
			"ca_key_passphrase": ca_key_passphrase
		}

		resp = requests.post(f"https://{self.location}:{self.app_port}/instances", json=body, **self.request_options)

		if resp.status_code == 200:
			logging.info(f"Successfully created new instance @ {self.location} - {name}")
			self.open_port(port, proto)
			return resp.text
		else:
			raise Exception(f"Invalid response code returned by {self.location} {resp.status_code}")

	def create_obfuscator(
		self,
		instance_id: str,
		obfs_proto: str,
		port: int,
		proto: str
		):

		body = {
			"obfuscation_method": obfs_proto,
			"listener_port": port
		}

		resp = requests.post(f"https://{self.location}:{self.app_port}/instances/{instance_id}/obfuscators", json=body, **self.request_options)

		if resp.status_code == 200:
			logging.info(f"Successfully created obfuscator @ {self.location} - {instance_id} {obfs_proto}:{port} {proto}")
			self.open_port(port, proto)
			return json.loads(resp.text)
		else:
			raise Exception(f"Invalid response code returned by {self.location} {resp.status_code}")

	def create_client(
		self,
		instance_id: str,
		ca_key_passphrase: str,
		client_name: str,
		obfuscator_id: str = None
		):

		body = {
			"client_name": client_name,
			"ca_key_passphrase": ca_key_passphrase,
			"obfuscator_id": obfuscator_id
		}

		resp = requests.post(f"https://{self.location}:{self.app_port}/instances/{instance_id}/clients", json=body, **self.request_options)

		if resp.status_code == 200:
			logging.info(f"Successfully created client @ {self.location} - {instance_id} {client_name} - {obfuscator_id}")
			return resp.text
		else:
			raise Exception(f"Invalid response code returned by {self.location} {resp.status_code}")

	def get_client(
		self,
		instance_id: str,
		client_name: str,
		target: str,
		out_location: str = "./tmp"
		):

		resp = requests.get(
			f"https://{self.location}:{self.app_port}/instances/{instance_id}/clients/{client_name}",
			params={
				"action": "download",
				"target": target
			},
			**self.request_options
		)

		if resp.status_code == 200:
			logging.info(f"Successfully retrieved client @ {self.location} - {instance_id} {client_name}")
			out_name = resp.headers["Content-Disposition"].split("; ")[1][9:]
			with open(f"{out_location}/{out_name}", "wb") as out_f:
				for chunk in resp.iter_content(chunk_size=128):
					out_f.write(chunk)
			return 
		else:
			raise Exception(f"Invalid response code returned by {self.location} {resp.status_code}")