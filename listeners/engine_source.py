from . import Listener
import falcon

class EngineSourceListener(Listener):
	def on_post(self, req, res):
		res.status = falcon.HTTP_200
		res.body   = req.context