from . import Listener
import falcon
import json

class EngineSourceListener(Listener):
	def on_post(self, req, res):
		Listener.on_post(self, req, res)

		res.status = falcon.HTTP_200
		res.body   = json.dumps({
						 "event_type":self.payload.event_type,
					     "branch":self.payload.branch,
					     "repository":self.payload.repository
					 })