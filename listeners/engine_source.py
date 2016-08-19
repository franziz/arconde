from . import Listener
import falcon
import json

class EngineSourceListener(Listener):
	def on_post(self, req, res):
		payload = req.stream.read()
		if not payload:
			raise falcon.HTTPBadRequest("Empty request body","A valid JSON document is required.")
		payload        = payload.decode("utf-8")
		payload        = json.loads(payload)
		parsed_payload = self.parse(payload)
		if parsed_payload is None:
			raise falcon.HTTPBadRequest("Parse failed","Cannot parse the payload.")
		event_type, payload = parsed_payload

		res.status = falcon.HTTP_200
		res.body   = json.dumps({
					     "event_type":event_type,
					     "branch":payload.branch
					 })