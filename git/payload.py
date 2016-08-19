class Payload:
	def __init__(self, payload=None):
		assert payload is not None, "payload is not defined."

		self.branch  = payload["ref"].split("/")[-1]
		self.content = payload
	