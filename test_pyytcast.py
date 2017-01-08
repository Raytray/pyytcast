import pyytcast
import mock
import unittest



class TestPyYtcast(unittest.TestCase):
    def test_get_feeds(self):
        test_result = pyytcast.get_feeds(config_name='test_feeds.conf')

        expected = {'test': {'channel_id': 'test_id'},
                    'test test': {'channel_id': 'another_test_id'}}

        self.assertEqual(expected, test_result)


    @mock.patch('feedparser.parse')
    def test_get_latest_entry(self, mock_feedparser_call):
        mocked_feed = Object()
        entry = Object()
        entry.link = 'asdf'
        mocked_feed.entries = [entry]

        mock_feedparser_call.return_value = mocked_feed

        get_latest_entry_param = {'test': {'channel_id': 'id'}}
        test_result = pyytcast.get_latest_entry(get_latest_entry_param)

        self.assertEqual([mocked_feed.entries[0].link], test_result)


class Object(object):
    """Used to create arbitrary objects in test"""
    pass
