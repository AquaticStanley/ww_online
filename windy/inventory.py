from .memory_access import read_from_ram, write_to_ram
from .ram import ram_map, constants_map

def player_has_item(item_slot_name, item_name=None):
	if item_name is None:
		item_name = item_slot_name
	if item_slot_name not in ram_map()['player_inventory']['pause_screen'] or item_name not in constants_map()['items']:
		raise RuntimeError('Item not found!')
	read = read_from_ram(ram_map()['player_inventory']['pause_screen'][item_slot_name])
	return read == str(constants_map()['items'][item_name]['id'])

def give_player_item(item_slot_name, item_name=None):
	if item_name is None:
		item_name = item_slot_name
	if item_slot_name not in ram_map()['player_inventory']['pause_screen'] or item_name not in constants_map()['items']:
		raise RuntimeError('Item not found!')
	success = write_to_ram(ram_map()['player_inventory']['pause_screen'][item_slot_name], int(constants_map()['items'][item_name]['id'], 16))
