from ..listeners.deploy        import DeployListener

class ListenerFactory:	
	DEPLOY = 0

	def __init__(self):
		pass

	@classmethod
	def get_listener(self, listener_name=None):
		assert listener_name is not None, "listener_name is not defined."

		if listener_name == ListenerFactory.DEPLOY:
			return DeployListener()