#!/usr/bin/env python3

import asyncio
from aiohttp import web, WSMsgType
import argparse
import json
from room import Room

class WWOnlineServer:
	def __init__(self):
		self.rooms: dict[str, Room] = {}
		self.app = web.Application()
		self.app.add_routes([web.get('/ws', self.handle_client)])
		web.run_app(self.app)

	async def handle_login_request(self, client, login_message):
		if login_message['room_name'] not in self.rooms:
			self.rooms[login_message['room_name']] = Room(login_message['room_name'], login_message['password'])

		if login_message['password'] == self.rooms[login_message['room_name']].password:
			print(f"Adding client {login_message['player_id']} to room {login_message['room_name']}")
			await self.rooms[login_message['room_name']].add_client(client, login_message['player_id'])


	async def handle_client(self, request):
		ws = web.WebSocketResponse()
		await ws.prepare(request)

		async for msg in ws:
			if msg.type == WSMsgType.TEXT:
				if msg.data == 'close':
					await ws.close()

				client_message = json.loads(msg.data)
				print(client_message)
				if client_message['message_type'] == 'player_login_request':
					print('handling login request!')
					await self.handle_login_request(ws, client_message['player_login_request'])
			elif msg.type == WSMsgType.ERROR:
				print(f'ws connection closed with exception {ws.exception()}')

		print('websocket connection closed')

		return ws


async def main(args):
	server = WWOnlineServer()
	await asyncio.gather(*tasks)

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Wind Waker Online Server')
	args = parser.parse_args()

	server = WWOnlineServer()

	# loop = asyncio.get_event_loop()
	# loop.run_until_complete(main(args))

	# app.add_routes([web.get('/ws', websocket_handler)])