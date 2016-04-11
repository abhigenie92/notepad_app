from twisted.internet.protocol import DatagramProtocol

# Here's a UDP version of the simplest possible protocol
class AudioEchoUDP(DatagramProtocol):	
	echoers = []
	def startProtocol(self):
		print "Audio server started"

	def datagramReceived(self, datagram, address):
		print address
		if address not in self.echoers:
			self.echoers.append(address)
		for echoer in self.echoers:
			if echoer!=address:
				self.transport.write(datagram, address)

	def connectionRefused(self):
		print self,dir(self)
		pass

def main():
	from twisted.internet import reactor
	port = reactor.listenUDP(0, AudioEchoUDP())
	audio_port=port.getHost().port
	print audio_port
	reactor.run()

if __name__ == '__main__':
	main()