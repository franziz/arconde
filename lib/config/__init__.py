from ..exceptions import CannotFindField
import json

class Config:
	def __init__(self, file_name=None):
		assert file_name is not None, "file_name is not defined."
		file        = open(file_name,"r")
		self.config = json.load(file)

	def get(self, field_name=None):
		assert field_name is not None, "field_name is not defined."

		if field_name not in self.config: raise CannotFindField("Cannot find field in the config file.")
		return self.config[field_name]