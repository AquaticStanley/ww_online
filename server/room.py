from client_data import ClientData

def item_is_upgrade(existing_item_id, proposed_item_id):
	# Always consider a different bottle an upgrade
	if 50 <= int(proposed_item_id, 16) <= 59:
		return True

	# Never consider nothing an upgrade
	if proposed_item_id == 'FF':
		return False

	# Always consider something an upgrade
	if existing_item_id == 'FF':
		return True

	# Rely on the fact that for upgradable slots, they're increasing as the item gets better
	return int(existing_item_id, 16) < int(proposed_item_id, 16)

class Room:
	def __init__(self, name, password):
		self.name = name
		self.password = password
		self.clients = {}
		self.ws_clients_to_remove = set()

	async def handle_player_state_update(self, ws_client, message):
		# TODO - we probably want to sweep all of the handled inventories on some basis to make sure they're synced.

		this_client_data = self.clients[ws_client]
		if not this_client_data.player_state:
			this_client_data.player_state = message
			return

		# print(f"Client {this_client_data.player_id} has a max hp of {this_client_data.player_state['player_stats']['max_hp']}")
		print(f"{this_client_data.player_id} - {message['player_stats']}")
		for client, client_data in self.clients.items():
			if client != ws_client:
				for item_slot, item_id in message['inventory'].items():
					if client_data.player_state and item_is_upgrade(client_data.player_state['inventory'][item_slot], item_id):
						print('Some player obtained an item!')
						await self.broadcast_message(self.get_obtained_item_json(this_client_data.player_id, item_slot, item_id), {client})

				for player_stat_field, player_stat_value in message['player_stats'].items():
					print(f'{player_stat_field} -> {type(player_stat_value)}')
					if isinstance(player_stat_value, str):
						# Exception for hex values - need an exception both to convert properly and to do our comparison properly
						# We generally replace items with a higher value, but FFFFFF is considered null generally
						# Heuristic for "null" value is going to be length of value replaced by F
						if client_data.player_state:
							null_hex_value = int(''.join(['F' for c in player_stat_value]), 16)
							incoming_stat_hex_value = int(player_stat_value, 16)
							client_stat_hex_value = int(client_data.player_state['player_stats'][player_stat_field], 16)
							if incoming_stat_hex_value != client_stat_hex_value:
								if client_stat_hex_value == null_hex_value or incoming_stat_hex_value > client_stat_hex_value:
									print(f'Some player triggered a hex player stat broadcast! ({player_stat_value} > {client_data.player_state["player_stats"][player_stat_field]})')
									await self.broadcast_message(self.get_player_status_updated_json(this_client_data.player_id, player_stat_field, player_stat_value), {client})

					elif client_data.player_state and player_stat_value > client_data.player_state['player_stats'][player_stat_field]:
						print(f"Some player triggered a player stat broadcast! Field {player_stat_field} ({player_stat_value} > {client_data.player_state['player_stats'][player_stat_field]})")
						await self.broadcast_message(self.get_player_status_updated_json(this_client_data.player_id, player_stat_field, player_stat_value), {client})

		this_client_data.player_state = message

	def get_obtained_item_json(self, player_id, item_slot, item_id):
		return {
			'message_type': 'player_obtained_item',
			'player_obtained_item': {
				'originating_player_id': player_id,
				'item_slot': item_slot,
				'item_id': item_id,
			}
		}

	def get_player_status_updated_json(self, player_id, stat_field, stat_value):
		return {
			'message_type': 'player_status_updated',
			'player_status_updated': {
				'originating_player_id': player_id,
				'player_status_field': stat_field,
				'player_status_value': stat_value,
			}
		}

	async def add_client(self, ws_client, player_id):
		self.clients[ws_client] = ClientData(player_id)

		await self.broadcast_message(self.get_connected_json(player_id))

	async def remove_client(self, ws_client):
		player_id = self.clients[ws_client].player_id
		del self.clients[ws_client]

		await self.broadcast_message(self.get_disconnected_json(player_id))

	async def broadcast_message(self, message, ws_client_set=None):
		if not ws_client_set:
			ws_client_set = self.clients

		ws_clients_to_remove = set()
		for ws in ws_client_set:
			try:
				await ws.send_json(message)
			except:
				self.ws_clients_to_remove.add(ws)


	async def remove_bad_clients(self):
		while True:
			for ws in self.ws_clients_to_remove:
				await self.remove_client(ws)
			self.ws_clients_to_remove.clear()
			await asyncio.sleep(5.)

	def get_connected_json(self, new_player_id):
		return {
			'message_type': 'player_connected',
			'player_connected': {
				'player_id': new_player_id,
			}
		}

	def get_disconnected_json(self, old_player_id):
		{
			'message_type': 'player_disconnected',
			'player disconnected': {
				'player_id': old_player_id,
			}
		}
