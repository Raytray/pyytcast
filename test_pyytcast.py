import pyytcast
import unittest


class TestPyYtcast(unittest.TestCase):
    def test_get_feeds(self):
        test_result = pyytcast.get_feeds(config_name='test_feeds.conf')

        expected = {'test': {'channel_id': 'test_id'},
                    'test test': {'channel_id': 'another_test_id'}}

        self.assertEqual(expected, test_result)
