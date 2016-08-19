from . import Config

class RouteConfig(Config):
	def __init__(self):
		Config.__init__(self, "/root/app/config/route.json")