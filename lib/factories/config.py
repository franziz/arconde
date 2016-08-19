from ..config.route import RouteConfig
from ..config.host  import HostConfig

class ConfigFactory:
	ROUTE = 0
	HOST  = 1

	def __init__(self):
		pass

	@classmethod
	def get_config(self, config_name=None):
		assert config_name is not None, "config_name is not defined."

		if config_name == ConfigFactory.ROUTE:
			return RouteConfig()
		elif config_name == ConfigFactory.HOST:
			return HostConfig()