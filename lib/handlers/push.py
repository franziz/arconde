from ..shell            import Shell
from ..exceptions       import HandlerInterruption, CannotFindRoute
from ..factories.config import ConfigFactory
import os

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

			is_new = not os.path.isdir(route_details["full_path"])
			if is_new:
				os.makedirs(route_details["full_path"], exist_ok=True)

			os.chdir(route_details["full_path"])
			if is_new:
				Shell.run_command("git remote add origin %s" % payload.clone_url)
				Shell.run_command("git remote update --prune")
				Shell.run_command("git pull orgin %s" payload.branch)
				Shell.run_command("git branch --set-upstream-to=origin/%s" % payload.branch)
			else:
				Shell.run_command("git remote update --prune")
				Shell.run_command("git pull")
		except CannotFindField as cannot_find_field:
			raise HandlerInterruption(cannot_find_field)