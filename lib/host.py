import paramiko

class Host:
	def __init__(self, config=None):
		assert config is not None, "config is not defined."
		self.config = config
		self.ssh    = None

	def connect(self):
		print("[host][debug] Connecting...")
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(
			    hostname = "%s" % self.config["ip"], 
			    username = "isid", 
			        port = int(self.config["port"]), 
			key_filename = "/root/app/keys/%s" % self.config["key"]
		)
		print("[host][debug] Connected!")

	def get_ssh(self):
		return self.ssh

	def run_command(self, command=None):
		assert command is not None, "command is not defined."
		return ssh.exec_command(command)
		