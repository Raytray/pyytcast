import pyytcast
import unittest


class TestPyYtcast(unittest.TestCase):
    def test_get_channel_ids(self):
        test_result = pyytcast.get_channel_ids(config_name='test_feeds.conf')

        expected = ['test_id', 'another_test_id', 'test_with_strip']
        self.assertEqual(expected, test_result)
