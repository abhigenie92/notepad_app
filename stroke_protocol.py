from twisted.internet.protocol import Protocol, Factory
class StrokeEcho(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.echoers.append(self)

    def dataReceived(self, data):
        for echoer in self.factory.echoers:
            if not self:
                echoer.transport.write(data)

    def connectionLost(self, reason):
        self.factory.echoers.remove(self)

class StrokeEchoFactory(Factory):
    def __init__(self):
        self.echoers = []

    def buildProtocol(self, addr):
        return MultiEcho(self)