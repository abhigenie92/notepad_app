from twisted.internet.protocol import DatagramProtocol

# Here's a UDP version of the simplest possible protocol
class AudioEchoUDP(DatagramProtocol):
	def __init__(self, factory):
		self.echoers = []
	def connectionMade(self):
		self.factory.echoers.append(self)

	def datagramReceived(self, datagram, address):
		for echoer in self.factory.echoers:
			if not self:
				self.transport.write(datagram, address)

	def connectionLost(self, reason):
		self.factory.echoers.remove(self)
