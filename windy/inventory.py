from .memory_access import read_from_ram, write_to_ram
from .ram import ram_map, constants_map

def player_has_item(item_name):
	read = read_from_ram(ram_map()['player_inventory']['pause_screen'][item_name])
	return read == str(constants_map()['items'][item_name]['id'])

def give_player_item(item_name):
	if item_name in ram_map()['player_inventory']['pause_screen'] and item_name in constants_map()['items']:
		success = write_to_ram(ram_map()['player_inventory']['pause_screen'][item_name], int(constants_map()['items'][item_name]['id'], 16))
