from . import Listener
import falcon
import json

class EngineSourceListener(Listener):
	def on_post(self, req, res):
		payload = req.stream.read()
		if not payload:
			raise falcon.HTTPBadRequest("Empty request body","A valid JSON document is required.")
		payload = payload.decode("utf-8")
		payload = json.loads(payload)

		event_type, payload = self.parse(payload)

		res.status = falcon.HTTP_200
		res.body   = json.dumps({
					     "event_type":event_type,
					     "branch":payload.branch
					 })