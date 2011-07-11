import unittest
import cassandranames

# Running this *will destroy* data in Cassandra.

class TestCassandraNames(unittest.TestCase):

    def setUp(self):
        cassandranames.install_schema(drop_first=True, rf=1)
        self.names = cassandranames.CassandraNames()

    def test_names(self):
        # Verify behavior on an initial, empty set.
        data = self.names.lookup("pantheon.example.com")
        self.assertEqual(data, {})
        data = self.names.lookup("pantheon.example.com", "A")
        self.assertEqual(data, {})

        # Add an "A" record.
        self.names.insert("pantheon.example.com", "A", "192.168.0.1")

        # Verify that the "A" records appears in lookups.
        data = self.names.lookup("pantheon.example.com")
        self.assertEqual(data, {"A": {"192.168.0.1": {"ttl": 900}}})
        data = self.names.lookup("pantheon.example.com", "A")
        self.assertEqual(data, {"A": {"192.168.0.1": {"ttl": 900}}})
        data = self.names.lookup("pantheon.example.com", "MX")
        self.assertEqual(data, {})

        # Add another "A" record, this time with an explicit TTL.
        self.names.insert("pantheon.example.com", "A", "192.168.0.2", 60)

        # Verify that both "A" records appear in results.
        data = self.names.lookup("pantheon.example.com")
        a_records = {"192.168.0.1": {"ttl": 900}, "192.168.0.2": {"ttl": 60}}
        self.assertEqual(data, {"A": a_records})
        data = self.names.lookup("pantheon.example.com", "A")
        self.assertEqual(data, {"A": a_records})
        data = self.names.lookup("pantheon.example.com", "MX")
        self.assertEqual(data, {})

        # Add an MX record.
        self.names.insert("pantheon.example.com", "MX", "192.168.0.3", priority=10)

        # Verify the MX record.
        data = self.names.lookup("pantheon.example.com")
        self.assertEqual(data, {"A": a_records, "MX": {"192.168.0.3": {"priority": 10, "ttl": 900}}})
        data = self.names.lookup("pantheon.example.com", "MX")
        self.assertEqual(data, {"MX": {"192.168.0.3": {"priority": 10, "ttl": 900}}})

        # Delete the A record for 192.168.0.1.
        self.names.remove("pantheon.example.com", "A", "192.168.0.1")

        # Verify the other "A" record and the "MX" record still exists.
        data = self.names.lookup("pantheon.example.com", "A")
        self.assertEqual(data, {"A": {"192.168.0.2": {"ttl": 60}}})
        data = self.names.lookup("pantheon.example.com", "MX")
        self.assertEqual(data, {"MX": {"192.168.0.3": {"priority": 10, "ttl": 900}}})

        # Delete all "MX" records and verify the deletion.
        self.names.remove("pantheon.example.com", "MX")
        data = self.names.lookup("pantheon.example.com", "MX")
        self.assertEqual(data, {})
        data = self.names.lookup("pantheon.example.com", "A")
        self.assertEqual(data, {"A": {"192.168.0.2": {"ttl": 60}}})

        # Delete all records for the domain and verify deletion.
        self.names.remove("pantheon.example.com")
        data = self.names.lookup("pantheon.example.com")
        self.assertEqual(data, {})

if __name__ == '__main__':
    unittest.main()
