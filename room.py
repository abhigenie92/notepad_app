class room(object):
	"""this class contains all rooms available for audio and video chat"""
	server_protocol_stroke=''
	server_protocol_audio=''
	connected_protocols_audio=set()
	connected_protocols_stroke=set()
	send_protocols_audio=set()
	send_protocols_stroke=set()
	request_audio_clients=[]
	request_stroke_clients=[]
	request_pending_clients=[]

	def __init__(self, **kwargs):
		self.server_username = kwargs['server_username'] # stores the username of the client that created
														 # the created the server
	
	def specify_factories(self,**kwargs):
		self.audio_factory=kwargs['audio_factory']
		self.stroke_factory=kwargs['stroke_factory']
		
	def get_all_connected_clients(self):
		audio_clients=self.audio_factory.get_all_connected_clients()
		stroke_clients=self.stroke_factory.get_all_connected_clients()
		return (audio_clients,stroke_clients)

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



