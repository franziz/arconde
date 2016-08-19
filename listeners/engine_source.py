from . import Listener
import falcon
import json

class EngineSourceListener(Listener):
	def on_post(self, req, res):
		res.status = falcon.HTTP_200
		res.body   = json.dumps(req.context)