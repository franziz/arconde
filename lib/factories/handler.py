from ..git.webhook   import WebHook
from ..handlers.push import PushHandler

class HandlerFactory:
	def __init__(self):
		pass

	@classmethod
	def get_handler(self, handler_name=None):
		assert handler_name is not None, "handler_name is not defined."

		if handler_name == WebHook.EventType.PUSH:
			return PushHandler()