import cassandranames
import dns.zone
import sys
import pprint
from dnstypeconstants import *

def import_zone(zone):
    names = cassandranames.CassandraNames()
    for (fqdn, ttl, rdata) in zone.iterate_rdatas():
        fqdn = str(fqdn).rstrip(".")
        data = None
        preference = None
        if rdata.rdtype == A:
            data = rdata.address
        elif rdata.rdtype == MX:
            data = str(rdata.exchange)
            preference = rdata.preference
        elif rdata.rdtype == CNAME:
            data = str(rdata.target)
        elif rdata.rdtype == NS:
            data = str(rdata.target)
        if data is not None:
            names.insert(fqdn, rdata.rdtype, data, ttl=ttl, preference=preference)
        

zone = dns.zone.from_file(sys.stdin, relativize=False)
import_zone(zone)
