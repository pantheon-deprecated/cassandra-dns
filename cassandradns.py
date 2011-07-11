from zope.interface import implements
from twisted.python import failure, log
from twisted.internet import interfaces, reactor, defer
from twisted.names import common, dns, resolve
from twisted.names.server import DNSServerFactory
from dnstypeconstants import *
import cassandranames
import sys
import pprint

class CassandraNamesResolver(common.ResolverBase):
    implements(interfaces.IResolver)
    
    def __init__(self):
        self.names = cassandranames.CassandraNames()
        common.ResolverBase.__init__(self)

    def _lookup(self, name, cls, type, timeout):
        log.msg("Looking up type %s records for hostname: %s" % (type, name))
        all_types = self.names.lookup(name, type)

        results = []
        authority = []
        additional = []

        if len(all_types) > 0:
            log.msg("Got results.")
        else:
            log.msg("No results.")

        for type, records in all_types.items():
            for data, metadata in records.items():
                if type == A:
                    payload = dns.Record_A(data)
                elif type == CNAME:  
                    payload = dns.Record_CNAME(data)
                elif type == MX:                    
                    payload = dns.Record_MX(metadata["preference"], data)
                elif type == NS:
                    payload = dns.Record_NS(data)
                header = dns.RRHeader(name, type=type, payload=payload, ttl=metadata["ttl"], auth=True)
                results.append(header)

        return defer.succeed((results, authority, additional))
        #return defer.fail(failure.Failure(dns.DomainError(name)))

authorities = [CassandraNamesResolver()]
factory = DNSServerFactory(authorities, verbose=True)
protocol = dns.DNSDatagramProtocol(factory)

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    reactor.listenUDP(1053, protocol)
    reactor.listenTCP(1053, factory)
    reactor.run()
