class Payload:
	def __init__(self, payload=None):
		assert payload is not None, "payload is not defined."

		self.branch     = payload["ref"].split("/")[-1]
		self.repository = payload["repository"]["full_name"]
		self.clone_url  = payload["repository"]["clone_url"]
		self.content    = payload
	