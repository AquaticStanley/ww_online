from client_data import ClientData

def item_is_upgrade(existing_item_id, proposed_item_id):
	# Always consider a different bottle an upgrade
	if 50 <= int(proposed_item_id, 16) <= 59:
		return True

	# Never consider nothing an upgrade
	if proposed_item_id == 'FF':
		return False

	# Rely on the fact that for upgradable slots, they're increasing as the item gets better
	return int(existing_item_id, 16) < int(proposed_item_id, 16)

class Room:
	def __init__(self, name, password):
		self.name = name
		self.password = password
		self.clients = {}

	async def handle_player_state_update(self, ws_client, message):
		# There are two approaches here - the lazy approach and the smart approach. AFAIK, both seem like they would work, and we'll start with the lazy approach initially.
		# The first approach is as follows:
		# First, diff the old player state and the new player state and see if anything has changed
		# If it has, the player has gained an item and we should broadcast that out to the rest of the clients.
		# If the clients get something they haven't gotten already, they'll update their state, end up here, and we re-broadcast the item once more.
		# Clients that have the item obtained already should not have their state changed at all.

		# The smart approach is as follows:
		# First, diff the old player state and the new player state and see if anything has changed
		# If it has, the player has gained an item. We should intelligently broadcast that out to the clients that have not reported that particular item.
		# current_client_data.previous_player_state = current_client_data.current_player_state
		# current_client_data.current_player_state = message.player_state

		# Additional: on the first update, we likely want to actually overwrite the state of all clients with any of the other clients (which should all be the same)

		# TODO - we probably want to sweep all of the handled inventories on some basis to make sure they're synced.

		this_client_data = self.clients[ws_client]
		if not this_client_data.player_state:
			this_client_data.player_state = message
			return

		for client, client_state in self.clients.items():
			if client != ws_client:
				for item_slot, item_id in message['inventory'].items():
					if item_is_upgrade(client.player_state['inventory'][item_slot], item_id):
						await self.broadcast_message(self.get_obtained_item_json(this_client_data.player_id, item_slot, item_id), {client})

	def get_obtained_item_json(self, player_id, item_slot, item_id):
		return {
			'message_type': 'player_obtained_item',
			'player_obtained_item': {
				'originating_player_id': player_id,
				'item_slot': item_slot,
				'item_id': item_id,
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
				ws_clients_to_remove.add(ws)

		for ws in ws_clients_to_remove:
			await self.remove_client(ws)

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
