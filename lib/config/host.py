from . import Config

class HostConfig(Config):
	def __init__(self):
		Config.__init__(self, "/root/app/config/hosts.json")