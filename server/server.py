#!/usr/bin/env python3

import asyncio
from aiohttp import web, WSMsgType
import argparse
import json
from room import Room

class WWOnlineServer:
	def __init__(self):
		self.rooms: dict[str, Room] = {}		

	async def handle_login_request(self, client, login_message):
		if login_message['room_name'] not in self.rooms:
			self.rooms[login_message['room_name']] = Room(login_message['room_name'], login_message['password'])

		if login_message['password'] == self.rooms[login_message['room_name']].password:
			print(f"Adding client {login_message['player_id']} to room {login_message['room_name']}")
			await self.rooms[login_message['room_name']].add_client(client, login_message['player_id'])

	async def handle_client(self, request):
		ws = web.WebSocketResponse()
		await ws.prepare(request)

		room_name = None
		async for msg in ws:
			if msg.type == WSMsgType.TEXT:
				if msg.data == 'close':
					await ws.close()

				client_message = json.loads(msg.data)
				if client_message['message_type'] == 'player_login_request':
					room_name = client_message['player_login_request']['room_name']
					await self.handle_login_request(ws, client_message['player_login_request'])

				elif client_message['message_type'] == 'player_state':
					await self.rooms[room_name].handle_player_state_update(ws, client_message['player_state'])

		print(f'Client disconnected (belonged to room {room_name})')
		if room_name and room_name in self.rooms:
			await self.rooms[room_name].remove_client(ws)

		return ws

	async def purge_unused_rooms(self):
		while True:
			rooms_to_remove = set()
			for room_name, room in self.rooms.items():
				if not room.clients:
					rooms_to_remove.add(room_name)

			for room_name in rooms_to_remove:
				print(f'Purging {room_name} as a room due to no players')
				del self.rooms[room_name]

			await asyncio.sleep(5.)


async def main(args):
	server = WWOnlineServer()

	asyncio.create_task(server.purge_unused_rooms())

	app = web.Application()
	app.add_routes([web.get('/ws', server.handle_client)])
	runner = web.AppRunner(app)
	await runner.setup()
	site = web.TCPSite(runner)
	await site.start()
	print('Server started')

	purge_unused_rooms_task = [asyncio.create_task(server.purge_unused_rooms())]
	tasks = purge_unused_rooms_task

	await asyncio.gather(*tasks)

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Wind Waker Online Server')
	args = parser.parse_args()
	
	loop = asyncio.new_event_loop()
	loop.run_until_complete(main(args))

	# app.add_routes([web.get('/ws', websocket_handler)])