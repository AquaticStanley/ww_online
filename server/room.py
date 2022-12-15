from client_data import ClientData

class Room:
	def __init__(self, name, password):
		self.name = name
		self.password = password
		self.clients = {}

	async def handle_player_state_update(self, ws_client):
		# There are two approaches here - the lazy approach and the smart approach. AFAIK, both seem like they would work, and we'll start with the lazy approach initially.
		# The first approach is as follows:
		# First, diff the old player state and the new player state and see if anything has changed
		# If it has, the player has gained an item and we should broadcast that out to the rest of the clients.
		# If the clients get something they haven't gotten already, they'll update their state, end up here, and we re-broadcast the item once more.
		# Clients that have the item obtained already should not have their state changed at all.

		# The smart approach is as follows:
		# First, diff the old player state and the new player state and see if anything has changed
		# If it has, the player has gained an item. We should intelligently broadcast that out to the clients that have not reported that particular item.
		pass

	async def add_client(self, ws_client, player_id):
		self.clients[ws_client] = ClientData(player_id)

		for ws in self.clients:
			await ws.send_json(self.get_connected_json(player_id))

	async def remove_client(self, ws_client):
		player_id = self.clients[ws_client].player_id
		del self.clients[ws_client]

		for ws, client_data in self.clients.items():
			await ws.send_json(self.get_disconnected_json(player_id))

	def get_connected_json(self, new_player_id):
		return {
			'message_type': 'player_connected',
			'player_connected': {
				'player_id': new_player_id
			}
		}

	def get_disconnected_json(self, old_player_id):
		{
			'message_type': 'player_disconnected',
			'player disconnected': {
				'player_id': old_player_id
			}
		}
