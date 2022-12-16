#!/usr/bin/env python3

import sys
from windy import memory_access, inventory, ram, player_status
import dme
import asyncio
import argparse
import aiohttp
import json

class WWOnlineClient:
	def __init__(self, player_name: str, server_hostname: str):
		self.player_name = player_name
		self.server_hostname = server_hostname
		self.ws = None

	def init(self):
		dme.DolphinAccessor.init()
		dme.DolphinAccessor.hook()

		if dme.DolphinAccessor.get_status() != dme.DolphinStatus.hooked:
			print('Failed to hook to emulator')
			sys.exit(0)

		print('Hooked to emulator successfully!')

		with open('ww_ram_map.json') as ww_ram_map:
			ram.initialize_ram_map(ww_ram_map)

		with open('ww_constants.json') as ww_constants:
			ram.initialize_constants_map(ww_constants)

	def get_login_json(self, player_name, room_name, password):
		return {
			'message_type': 'player_login_request',
			'player_login_request': {
				'player_id': player_name,
				'room_name': room_name,
				'password': password,
			}
		}

	async def connect_to_server(self, room_name, password):
		reconnect_interval = 5.0
		while True:
			async with aiohttp.ClientSession() as session:
				try:
					async with session.ws_connect(f'http://{self.server_hostname}:8080/ws') as ws:
						self.ws = ws
						await ws.send_json(self.get_login_json(self.player_name, room_name, password))
						async for msg in ws:
							if msg.type == aiohttp.WSMsgType.TEXT:
								if msg.data == 'close cmd':
									await ws.close()
									break

								server_message = json.loads(msg.data)
								if server_message['message_type'] == 'player_obtained_item':
									await self.handle_player_obtained_item(server_message['player_obtained_item'])

								elif server_message['message_type'] == 'player_status_updated':
									await self.handle_player_status_updated(server_message['player_status_updated'])

							elif msg.type == aiohttp.WSMsgType.ERROR:
								break
				except Exception as e:
					print(e)

			self.ws = None
			print(f'Disconnected from server - retrying in {reconnect_interval} seconds')
			await asyncio.sleep(reconnect_interval)

	async def handle_player_obtained_item(self, player_obtained_item_message):
		print(f"Player {player_obtained_item_message['originating_player_id']} obtained item {player_obtained_item_message['item_id']} - adding to our inventory.")
		inventory.give_player_item_by_id(player_obtained_item_message['item_slot'], player_obtained_item_message['item_id'])

	async def handle_player_status_updated(self, player_status_updated_message):
		print(f"Player {player_status_updated_message['originating_player_id']} updated their {player_status_updated_message['player_status_field']} to {player_status_updated_message['player_status_value']}")
		# Special case for hp, possibly rupees and other values?
		if player_status_updated_message['player_status_field'] == 'max_hp':
			player_status.set_player_max_hp(player_status_updated_message['player_status_value'])

	def get_player_state_json(self, player_state):
		return {
			'message_type': 'player_state',
			'player_state': player_state,
		}

	async def send_current_state(self):
		while True:
			if self.ws:
				player_state = {
					'player_id': self.player_name,
					'inventory': inventory.build_inventory_state(),
					'player_stats': player_status.build_player_status_state(),
				}

				await self.ws.send_json(self.get_player_state_json(player_state))

			await asyncio.sleep(1.)


async def main(args):
	client = WWOnlineClient(player_name=args.player_name, server_hostname=args.server_hostname)
	client.init()

	connect_to_server_task = [asyncio.create_task(client.connect_to_server(args.room_name, args.room_password))]
	send_current_state_task = [asyncio.create_task(client.send_current_state())]
	tasks = connect_to_server_task + send_current_state_task

	await asyncio.gather(*tasks)


if __name__ == '__main__':
	parser = argparse.ArgumentParser('Wind Waker Online Client')
	parser.add_argument('--server-hostname', help='Hostname of server to connect to', required=True)
	parser.add_argument('--player-name', help='Player name to connect as. Required.', required=True)
	parser.add_argument('--room-name', help='Room name to connect to', required=True)
	parser.add_argument('--room-password', help='Room password. Optional.', default='')
	args = parser.parse_args()

	loop = asyncio.new_event_loop()
	loop.run_until_complete(main(args))