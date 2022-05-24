from .memory_access import read_from_ram

def player_has_item(ram_map, constants_map, item_name):
	read = read_from_ram(ram_map['player_inventory']['pause_screen'][item_name])
	return read == constants_map['items'][item_name]['id']
