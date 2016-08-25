from .                  import Listener
from ..factories.config import ConfigFactory
from ..host             import Host
from ..sftp             import SFTP
import falcon
import json
import os
import zipfile
import shutil

class DeployListener(Listener):
	def on_post(self, req, res):
		Listener.on_post(self, req, res)
		
		route = req.get_param("route", required=True)

		print("[deploy][debug] Preparing storage folder...")
		route_config = ConfigFactory.get_config(ConfigFactory.ROUTE)
		route_config = route_config.get(route)
		if os.path.isdir(route_config["full_path"]):
			shutil.rmtree(route_config["full_path"])
		os.makedirs(route_config["full_path"], exist_ok=True)		

		print("[deploy][debug] Receiving files...")
		file_param  = req.get_param("file")
		zipped_file = zipfile.ZipFile(file_param.file)
		zipped_file.extractall(route_config["full_path"])

		# SSH-ing the host machine
		# and try to copy everything necessary using scp
		print("[deploy][debug] Connecting to host...")
		route        = route_config["route"]
		host_config  = ConfigFactory.get_config(ConfigFactory.HOST)
		host_details = host_config.get(route["host"])
		host         = Host(host_details)
		host.connect()
		print("[deploy][debug] Connected!")
		
		print("[deploy][debug] Removing %s folder..." % route["target"])
		stdin, stdout, stderr = host.run_command(
			command = "sudo rm -rv %s" % route["target"], 
			get_pty = True
		)
		stdin.write("%s\n" %host_details["password"])
		stdin.flush()
		stdout.channel.recv_exit_status() # wait until the command gives exit_status	

		print("[deploy][debug] Deploying....")
		sftp = SFTP(host.get_ssh())
		sftp.mkdir(route["target"]) # Assuming the target folder already removied
		sftp.put_dir(route_config["full_path"], route["target"]) # Copy all files inside full_path to target
		host.restart(route["container"])
		print("[deploy][debug] Deployed!")

		res.status = falcon.HTTP_200		