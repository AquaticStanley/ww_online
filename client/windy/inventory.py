from .memory_access import read_from_ram, write_to_ram
from .ram import ram_map, constants_map

def player_has_item(item_slot_name, item_name=None):
	if item_name is None:
		item_name = item_slot_name
	return item_in_slot(item_slot_name) == str(constants_map()['items'][item_name]['id'])

def give_player_item_by_name(item_slot_name, item_name=None):
	if item_name is None:
		item_name = item_slot_name
	if item_slot_name not in ram_map()['player_inventory']['pause_screen'] or item_name not in constants_map()['items']:
		raise RuntimeError('Item not found!')
	return give_player_item_by_id(item_slot_name, constants_map()['items'][item_name]['id'])

def give_player_item_by_id(item_slot_name, item_id):
	if item_slot_name not in ram_map()['player_inventory']['pause_screen']:
		raise RuntimeError('Item not found!')
	return write_to_ram(ram_map()['player_inventory']['pause_screen'][item_slot_name], int(item_id, 16))

def item_in_slot(item_slot_name):
	if item_slot_name not in ram_map()['player_inventory']['pause_screen']:
		raise RuntimeError('Item slot not found!')
	read = read_from_ram(ram_map()['player_inventory']['pause_screen'][item_slot_name])
	return read

def build_inventory_state():
	inventory_state = {}
	for item_slot_name, item_slot_contents in ram_map()['player_inventory']['pause_screen'].items():
		inventory_state[item_slot_name] = item_in_slot(item_slot_name)
	return inventory_state

def build_player_stats_state():
	pass

def build_equipment_state():
	pass
