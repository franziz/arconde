from ..factories.handler import HandlerFactory
from ..git.webhook       import WebHook
from ..git.payload       import Payload
import json
import falcon

class Listener:
	def on_get(self, req, res):
		raise NotImplemented

	def on_post(self, req, res):
		self.payload = req.stream.read()
		if not self.payload:
			raise falcon.HTTPBadRequest("Empty request body","A valid JSON document is required.")
		self.payload = self.payload.decode("utf-8")
		self.payload = json.loads(self.payload)
		self.payload = self.parse(self.payload)
		if self.payload is None:
			raise falcon.HTTPBadRequest("Parse failed","Cannot parse the payload.")
		handler = HandlerFactory.get_handler(self.payload.event_type)
		handler.handle(self.payload)

	def parse(self, payload=None):
		assert payload is not None, "payload is not defined."

		parsed_payload = Payload(payload)
		if "ref" in payload and "before" in payload and "after" in payload:
			parsed_payload.event_type = WebHook.EventType.PUSH
		return None
