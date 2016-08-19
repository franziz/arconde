from ..shell            import Shell
from ..exceptions       import HandlerInterruption, CannotFindField
from ..factories.config import ConfigFactory
from ..host     		import Host
from ..sftp 			import SFTP
from . 					import Handler
import os
import json

class PushHandler(Handler):
	def __init__(self):
		pass

	def handle(self, payload=None):
		""" This push handler will try to pull a new data from GitHub to related route
			In order to know which route that the handler should go, you need to specify the route
			inside `/root/app/config/route.json` file. 

			The route name is a combination of
				payload.repository + payload.branch
			example:
				isidsea/engine_sources/high_priority
				- payload.repository = "isidsea/engine_sources"
				- payload.branch     = "high_priority"
		"""
		try:
			Handler.handle(self, payload)

			# Make a route name by combining payload.repository + payload.branch
			route_name = "%s/%s" % (payload.repository, payload.branch)

			# Opening /root/app/config/route.json
			self.route_config = ConfigFactory.get_config(ConfigFactory.ROUTE)
			route_details     = self.route_config.get(route_name) # This will throw an error if the route_name cannot be found
			push_details      = route_details["route"]["push"]

			is_new = not os.path.isdir(route_details["full_path"])
			if is_new:
				os.makedirs(route_details["full_path"], exist_ok=True)
			
			# Updating the source files
			os.chdir(route_details["full_path"])			
			if is_new:
				Shell.run_command("git init")
				Shell.run_command("git remote add origin %s" % payload.clone_url)
				Shell.run_command("git remote update --prune")
				Shell.run_command("git pull origin %s" % payload.branch)
				Shell.run_command("git branch --set-upstream-to=origin/%s" % payload.branch)
			else:
				Shell.run_command("git remote update --prune")
				Shell.run_command("git pull")

			# SSH-ing the host machine
			# and try to copy everything necessary using scp
			host_config  = ConfigFactory.get_config(ConfigFactory.HOST)
			host_details = host_config.get(push_details["host"])
			host         = Host(host_details)
			host.connect()
			
			stdin, stdout, stderr = host.run_command(
				command = "sudo rm -rv %s" % push_details["target"], 
				get_pty = True
			)
			stdin.write("%s\n" %host_details["password"])
			stdin.flush()
			stdout.channel.recv_exit_status() # wait until the command gives exit_status			

			stdin, stdout, stderr = host.run_command("docker inspect %s" % push_details["container"])
			container_details     = ""
			for line in stdout:
				container_details += line
			container_details = json.loads(container_details)[0]
			mount             = container_details["Mounts"][0]

			# Making directory from extended_path
			# for example "/src" is the extended_path, then the iteration is based on
			# number of words splitted by "/"
			extended_path     = push_details["target"].replace(mount["Source"],"")
			sftp              = SFTP(host.get_ssh())
			current_directory = mount["Source"]
			for path in extended_path.split("/")[1:]:
				sftp.mkdir("%s/%s" % (current_directory, path))
			put_dir(sftp, route_details["full_path"], push_details["target"]) # Copy all files inside full_path to target
		except CannotFindField as cannot_find_field:
			raise HandlerInterruption(cannot_find_field)