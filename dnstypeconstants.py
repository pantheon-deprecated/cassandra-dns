# Shamelessly ripped from Twisted's dns.py
(A, NS, MD, MF, CNAME, SOA, MB, MG, MR, NULL, WKS, PTR, HINFO, MINFO, MX, TXT,
 RP, AFSDB) = range(1, 19)
AAAA = 28
SRV = 33
NAPTR = 35
A6 = 38
DNAME = 39
SPF = 99

QUERY_TYPES = {
    A: 'A',
    NS: 'NS',
    MD: 'MD',
    MF: 'MF',
    CNAME: 'CNAME',
    SOA: 'SOA',
    MB: 'MB',
    MG: 'MG',
    MR: 'MR',
    NULL: 'NULL',
    WKS: 'WKS',
    PTR: 'PTR',
    HINFO: 'HINFO',
    MINFO: 'MINFO',
    MX: 'MX',
    TXT: 'TXT',
    RP: 'RP',
    AFSDB: 'AFSDB',

    # 19 through 27?  Eh, I'll get to 'em.

    AAAA: 'AAAA',
    SRV: 'SRV',
    NAPTR: 'NAPTR',
    A6: 'A6',
    DNAME: 'DNAME',
    SPF: 'SPF'
}

IXFR, AXFR, MAILB, MAILA, ALL_RECORDS = range(251, 256)

# "Extended" queries (Hey, half of these are deprecated, good job)
EXT_QUERIES = {
    IXFR: 'IXFR',
    AXFR: 'AXFR',
    MAILB: 'MAILB',
    MAILA: 'MAILA',
    ALL_RECORDS: 'ALL_RECORDS'
}

REV_TYPES = dict([
    (v, k) for (k, v) in QUERY_TYPES.items() + EXT_QUERIES.items()
])

IN, CS, CH, HS = range(1, 5)
ANY = 255

QUERY_CLASSES = {
    IN: 'IN',
    CS: 'CS',
    CH: 'CH',
    HS: 'HS',
    ANY: 'ANY'
}
REV_CLASSES = dict([
    (v, k) for (k, v) in QUERY_CLASSES.items()
])


# Opcodes
OP_QUERY, OP_INVERSE, OP_STATUS = range(3)
OP_NOTIFY = 4 # RFC 1996
OP_UPDATE = 5 # RFC 2136


# Response Codes
OK, EFORMAT, ESERVER, ENAME, ENOTIMP, EREFUSED = range(6)
