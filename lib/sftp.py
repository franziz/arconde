import os

class SFTP:
	def __init__(self, ssh=None):
		assert ssh is not None, "ssh is not defined."
		self.sftp = ssh.open_sftp()

	def mkdir(self,path=None):
		assert path is not None, "path is not defined."
		self.sftp.mkdir(path)

	def put_dir(self, source=None, target=None):
		""" Copy a whole directory in a recursive way. 
			This function assume that all the source and target are in linux format.
			Therefore, os.path.join() is not implemented.
		"""
		assert source is not None, "source is not defined."
		assert target is not None, "target is not defined."

		for item in os.listdir(source):
			if os.path.isfile(os.path.join(source,item)):
				self.sftp.put("{}/{}".format(source,item), "{}/{}".format(target,item))
			else:				
				self.sftp.mkdir("{}/{}".format(target, item), 511)
				self.put_dir("{}/{}".format(source,item), "{}/{}".format(target,item))