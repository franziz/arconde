import json
import falcon

class Listener:
	def on_get(self, req, res):
		raise NotImplemented

	def on_post(self, req, res):
		pass
