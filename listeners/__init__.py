from git.webhook import WebHook
from git.payload import Payload

class Listener:
	def on_get(self, req, res):
		raise NotImplemented

	def on_post(self, req, res):
		raise NotImplemented

	def parse(self, payload=None):
		assert payload is not None, "payload is not defined."

		if "ref" in payload and "head" in payload and "before" in payload:
			return(WebHook.EventType.PUSH, Payload(payload))
