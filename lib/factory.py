from .git.webhook             import WebHook
from .listeners.engine_source import EngineSourceListener
from .handlers.push           import PushHandler

class ListenerFactory:
	ENGINE_SOURCE = 0

	def __init__(self):
		pass

	@classmethod
	def get_listener(self, listener_name=None):
		assert listener_name is not None, "listener_name is not defined."

		if listener_name == ListenerFactory.ENGINE_SOURCE:
			return EngineSourceListener()

class HandlerFactory:
	def __init__(self):
		pass

	def get(self, handler_name=None):
		assert handler_name is not None, "handler_name is not defined."

		if handler_name == WebHook.EventType.PUSH:
			return PushHandler()