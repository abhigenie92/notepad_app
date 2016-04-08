class room(object):
	"""this class contains all rooms available for audio and video chat"""
	def __init__(self, **kwargs):
		self.server_username = kwargs['server_username'] # stores the username of the client that created
														 # the created the server
		self.connected_clients=set([]) 					 # stores the list of clients connected
		self.allowed_send_clients=set([]) 				 # stores the list of clients allowed to send

	def add_connected_client(self,client_addr):
		'''adds a connected client to send data'''
		self.connected_clients.add(client_addr)

	def remove_connected_client(self,client_addr):
		'''removes a connected client from both lists'''
		self.allowed_send_clients.remove(client_addr)
		self.connected_clients.remove(client_addr)

	def add_allowed_send_client(self,client_addr):
		'''adds to both sets'''
		self.allowed_send_clients.add(client_addr)
		self.connected_clients.add(client_addr)
	
	def remove_allowed_send_client(self,client_addr):
		'''removes the privilege of a connected client to send data'''
		self.allowed_send_clients.remove(client_addr)

