import os, json, subprocess, sys
from .dispatch import dispatch_cmd

CONFIG_FILE_NAME = '.gu_config'

class Configs:
	def __init__(self, current_user, users_list):
		self.current_user = current_user
		self.users_list = users_list

class Gu:
	def __init__(self, parser):
		args = parser.parse_args()
		self.parser = parser
		self.cmd = args.cmd[0]
		self.args = args.cmd[1:]
		self.glob = args.glob
		self.validate_args()
		self.open_configs()
	
	def object_decoder(self, obj):
		if '__type__' in obj and obj['__type__'] == 'Configs':
			return Configs(obj['current_user'], obj['users_list'])
		return obj

	def write_configs(self):
		config_dict = self.data.__dict__
		config_dict['__type__'] = 'Configs'
		json_string = json.dumps(config_dict, indent=4)
		with open(self.config_file, "w+") as f:
			f.write(json_string)

	def open_configs(self):
		'''open_configs opens and returns a confguration file. creates a new file if one doesnt exist'''
		try:
			self.config_file = os.path.join(os.environ['DEV_CONFIG_DIR'], CONFIG_FILE_NAME)
		except KeyError:
			self.config_file = os.path.join(os.path.expanduser('~'), CONFIG_FILE_NAME)
		except:
			print("failed to get environ var")
			sys.exit(1)

		if not os.path.exists(self.config_file):
			self.write_configs(Configs("", {}), config_file)
			
		with open(self.config_file) as json_file:
			self.data = json.load(json_file, object_hook=self.object_decoder)

	def validate_args(self):
		valid = ['use', 'add', 'list', 'ls']
		if self.cmd not in valid:
			print("nope")
			sys.exit(1)

def gu(parser):
	dispatch_cmd(Gu(parser))
