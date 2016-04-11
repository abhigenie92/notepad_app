import sockets
class Audio_Thread_Tcp(object):
	"""docstring for Audio_Thread_Tcp"""
	#audio parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
	def __init__(self, **kwargs):
		self.port = kwargs['port']
		self.server_ip=kwargs['server_ip']
		self.sock_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock_audio.bind(('0.0.0.0',0)) # 0.0.0.0 will allow all connections
        audio_port=self.sock_audio.getsockname()[1]
        
		