from twisted.application import internet, service
from twisted.internet import reactor
from twisted.python import log
import twisted
import sys
sys.path.append('/opt/cassandra-dns')
from cassandradns import protocol, factory

application = twisted.application.service.Application('Cassandra DNS')

logfile = twisted.python.logfile.DailyLogFile('cassandradns.log', '/var/log/cassandradns')
logfile.shouldRotate()
application.setComponent(twisted.python.log.ILogObserver, twisted.python.log.FileLogObserver(logfile).emit)

server = internet.UDPServer(53, protocol)
server.setServiceParent(application)
server = internet.TCPServer(53, factory)
server.setServiceParent(application)
