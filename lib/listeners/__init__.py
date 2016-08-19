from ..factories.handler import HandlerFactory
from ..git.webhook       import WebHook
from ..git.payload       import Payload

class Listener:
	def on_get(self, req, res):
		raise NotImplemented

	def on_post(self, req, res):
		self.payload = req.stream.read()
		if not payload:
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

		if "ref" in payload and "before" in payload and "after" in payload:
			return Payload(payload)
		return None
