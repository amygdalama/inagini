import os

from twisted.internet import reactor
from twisted.internet.protocol import Factory, ProcessProtocol, Protocol


class INagini(Protocol):

    def connectionMade(self):
        self.process = INaginiProcess(self)
        reactor.spawnProcess(self.process, 'nagini',
                             args=['nagini'],
                             usePTY=True, env=os.environ)

    def dataReceived(self, stmt):
        self.process.transport.write(stmt)
        self.process.transport.closeStdin()


class INaginiProcess(ProcessProtocol):

    def __init__(self, server):
        self.server = server

    def outReceived(self, out):
        self.server.transport.write(out)

    def errReceived(self, err):
        self.server.transport.write(out)


class INaginiFactory(Factory):

    def buildProtocol(self, addr):
        return INagini()


if __name__ == '__main__':
    reactor.listenTCP(8007, INaginiFactory())
    reactor.run()
