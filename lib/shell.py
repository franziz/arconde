from .exceptions import CommandError
import subprocess

class Shell:
	def __init__(self):
		pass

	@staticmethod
	def run_command(command=None):
		assert command is not None, "command is not defined."
		command = command.split(" ") if not type(command) is list else command
		proc    = subprocess.Popen(command, stdout=subprocess.PIPE)
		success = False
		for line in proc.stdout:
			line = line.decode("utf-8")
			if "nothing to commit" in line:
				success = True
		proc.wait()

		exit_code = proc.returncode
		if exit_code != 0 and not success: raise CommandError("Exit: %s" % exit_code)
		return proc.returncode