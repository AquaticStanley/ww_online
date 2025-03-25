from .memory_access import read_from_ram, write_to_ram
from .ram import ram_map, constants_map

def set_player_max_hp(hp_value):
	print(f'Setting max hp to {hp_value}')
	# Set max hp
	write_to_ram(ram_map()['player_status']['max_hp'], hp_value)

	# Set current hp
	write_to_ram(ram_map()['player_status']['current_hp'], hp_value)

	# Modify the player hp by 1 this frame
	write_to_ram(ram_map()['player_status']['hp_modify_this_frame'], 1.0)

def get_player_max_hp():
	return int(read_from_ram(ram_map()['player_status']['max_hp']))

def set_player_rupees(rupees):
	write_to_ram(ram_map()['player_status']['rupee_modify_this_frame'], rupees)

def get_player_equipped_sword():
	print(f"[get_player_equipped_sword] - current owned sword value is {read_from_ram(ram_map()['player_inventory']['owned_items']['Sword'])}")
	return read_from_ram(ram_map()['player_status']['equipped_sword'])

def set_player_equipped_sword(value):
	# Set currently equipped sword
	write_to_ram(ram_map()['player_status']['equipped_sword'], int(value, 16))

	# Set owned sword on pause screen
	write_to_ram(ram_map()['player_inventory']['owned_items']['Sword'], sword_equipped_value_to_owned_item_value(int(value, 16)))

def sword_equipped_value_to_owned_item_value(equipped_value) -> int:
	# NOTE - it seems that the documentation on the constants map is messed up/off by one
	# This has been corrected in the constants map and the scope may be limited to bitfield data types alone
	mapping = {
		0xFF: constants_map()['owned_item_indicator']['sword']['no_sword'],
		0x38: constants_map()['owned_item_indicator']['sword']['hero_sword'],
		0x39: constants_map()['owned_item_indicator']['sword']['master_sword_powerless'],
		0x3A: constants_map()['owned_item_indicator']['sword']['master_sword_half_power'],
		0x3E: constants_map()['owned_item_indicator']['sword']['master_sword_full_power'],
	}
	owned_item_val = int(mapping[equipped_value], 16)
	return int(mapping[equipped_value], 16)

def set_player_status_field(player_status_field, value):
	print(f'Attempting to write {player_status_field} -> {value}')
	write_to_ram(ram_map()['player_status'][player_status_field], value)

def build_player_status_state():
	return  {
		'max_hp': get_player_max_hp(),
		'equipped_sword': get_player_equipped_sword(),
	}
