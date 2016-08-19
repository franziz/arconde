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

	def run_command(self, command=None, **kwargs):
		assert command  is not None, "command is not defined."
		assert self.ssh is not None, "ssh is not defined."
		
		print("[host][debug] Excuting: %s" % command)
		return self.ssh.exec_command(command, **kwargs)

	def restart(self, container=None):
		assert container is not None, "container is not defined."
		print("[host][debug] Restarting...")
		stdin, stdout, stderr = self.run_command("docker restart %s" % container)
		print("[host][debug] Restarting %s: %s" % (container, stdout.channel.recv_exit_status()))
		stdin, stdout, stderr = self.run_command("docker exec -d %s bash /root/app/kick_start.sh" % container)
		print("[host][debug] Executing kick_start.sh: %s" % stdout.channel.recv_exit_status())
		print("[host][debug] Started!")
		