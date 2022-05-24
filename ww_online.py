#!/usr/bin/env python3

import sys
import json
from windy import memory_access, inventory
import dme

class WWOnline:
	def __init__(self):
		dme.DolphinAccessor.init()
		dme.DolphinAccessor.hook()

		with open('ww_ram_map.json') as ww_ram_map:
			self.ram_map = json.load(ww_ram_map)

		with open('ww_constants.json') as ww_constants:
			self.constants_map = json.load(ww_constants)

	def run(self):
		if dme.DolphinAccessor.get_status() != dme.DolphinStatus.hooked:
			print('Failed to hook to emulator')
			sys.exit(0)

		print('Hooked to emulator successfully!')

		if inventory.player_has_item(self.ram_map, self.constants_map, 'Telescope'):
			print('Player has Telescope!')
		else:
			print('Player does not have Telescope!')


if __name__ == '__main__':
	ww_online = WWOnline()
	ww_online.run()