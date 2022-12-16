import json

_ram_map = None
_constants_map = None

def initialize_ram_map(ram_json_file):
	global ram_map
	ram_map = json.load(ram_json_file)

def initialize_constants_map(constants_json_file):
	global constants_map
	constants_map = json.load(constants_json_file)

def ram_map():
	global ram_map
	return ram_map

def constants_map():
	global constants_map
	return constants_map