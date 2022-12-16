#!/usr/bin/env python3

import sys
import asyncio
import argparse
import aiohttp
import json
from datetime import datetime, timedelta

class MockClient:
	def __init__(self, player_name: str, server_hostname: str):
		self.player_name = player_name
		self.server_hostname = server_hostname
		self.ws = None
		self.start_time = datetime.now()

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

							elif msg.type == aiohttp.WSMsgType.ERROR:
								break
				except:
					pass

			self.ws = None
			print(f'Disconnected from server - retrying in {reconnect_interval} seconds')
			await asyncio.sleep(reconnect_interval)

	async def handle_player_obtained_item(self, player_obtained_item_message):
		print(f"Player {player_obtained_item_message['originating_player_id']} obtained item {player_obtained_item_message['item_id']} - adding to our inventory.")

	def get_player_state_json(self, player_state):
		return {
			'message_type': 'player_state',
			'player_state': player_state
		}

	def get_initial_inventory(self):
		return {
			'Telescope': '20',
			'Sail': 'FF',
			'Wind Waker': 'FF',
			'Grappling Hook': 'FF',
			'Spoils Bag': 'FF',
			'Boomerang': 'FF',
			'Deku Leaf': 'FF',
			'Tingle Tuner': 'FF',
			'Picto Box': 'FF',
			'Iron Boots': 'FF',
			'Magic Armor': 'FF',
			'Bait Bag': 'FF',
			'Bow': 'FF',
			'Bombs': 'FF',
			'Bottle 1': 'FF',
			'Bottle 2': 'FF',
			'Bottle 3': 'FF',
			'Bottle 4': 'FF',
			'Delivery Bag': 'FF',
			'Hookshot': 'FF',
			'Skull Hammer': 'FF',
		}

	def get_final_inventory(self):
		print('Getting final inventory!')
		return {
			'Telescope': '20',
			'Sail': 'FF',
			'Wind Waker': 'FF',
			'Grappling Hook': '25',
			'Spoils Bag': 'FF',
			'Boomerang': 'FF',
			'Deku Leaf': 'FF',
			'Tingle Tuner': 'FF',
			'Picto Box': 'FF',
			'Iron Boots': 'FF',
			'Magic Armor': 'FF',
			'Bait Bag': 'FF',
			'Bow': 'FF',
			'Bombs': 'FF',
			'Bottle 1': 'FF',
			'Bottle 2': 'FF',
			'Bottle 3': 'FF',
			'Bottle 4': 'FF',
			'Delivery Bag': 'FF',
			'Hookshot': 'FF',
			'Skull Hammer': 'FF',
		}

	async def send_current_state(self):
		while True:
			if self.ws:
				player_state = {
					'player_id': self.player_name,
					'inventory': self.get_initial_inventory() if self.start_time + timedelta(0, 10) > datetime.now() else self.get_final_inventory(),
				}

				await self.ws.send_json(self.get_player_state_json(player_state))

			await asyncio.sleep(1.)


async def main(args):
	client = MockClient(player_name=args.player_name, server_hostname=args.server_hostname)

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