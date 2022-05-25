#!/usr/bin/env python3

import sys

from windy import memory_access, inventory, ram, player_status
import dme

class WWOnline:
	def __init__(self):
		dme.DolphinAccessor.init()
		dme.DolphinAccessor.hook()

	def run(self):
		if dme.DolphinAccessor.get_status() != dme.DolphinStatus.hooked:
			print('Failed to hook to emulator')
			sys.exit(0)

		print('Hooked to emulator successfully!')

		player_status.set_player_max_hp(36)
		player_status.set_player_rupees(120)
		item_slot_to_give = 'Bottle 1'
		item_name = 'Forest Firefly'
		if inventory.player_has_item(item_slot_to_give, item_name):
			print(f'Player has {item_slot_to_give}!')
		else:
			print(f'Player does not have {item_slot_to_give}!')
			inventory.give_player_item(item_slot_to_give, item_name)
			if inventory.player_has_item(item_slot_to_give, item_name):
				print(f'Gave player the {item_slot_to_give}!')


if __name__ == '__main__':
	with open('ww_ram_map.json') as ww_ram_map:
		ram.initialize_ram_map(ww_ram_map)

	with open('ww_constants.json') as ww_constants:
		ram.initialize_constants_map(ww_constants)

	ww_online = WWOnline()
	ww_online.run()
