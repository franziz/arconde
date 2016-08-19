from ..listeners.engine_source import EngineSourceListener

class ListenerFactory:
	ENGINE_SOURCE = 0

	def __init__(self):
		pass

	@classmethod
	def get_listener(self, listener_name=None):
		assert listener_name is not None, "listener_name is not defined."

		if listener_name == ListenerFactory.ENGINE_SOURCE:
			return EngineSourceListener()