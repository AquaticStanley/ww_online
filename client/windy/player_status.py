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

def build_player_status_state():
	return  {
		'max_hp': get_player_max_hp()
	}
