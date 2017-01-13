import pyytcast
import mock
import unittest


class TestPyYtcast(unittest.TestCase):
    def test_get_channel_ids(self):
        test_result = pyytcast.get_channel_ids()

        expected = ['test_id', 'another_test_id', 'test_with_strip']
        self.assertEqual(expected, test_result)

    @mock.patch('os.listdir')
    @mock.patch('os.remove')
    def test_cleanup_old_files(self, mock_os_listdir_call, mock_remove_call):
        mocked_directory = ['test.mp3', 'test2.mp3', 'test3.mp3']
        mock_os_listdir_call.return_value = mocked_directory

        test_params = mocked_directory
        test_params.pop(0)  # remove first element
        pyytcast.cleanup_old_files(test_params)

        self.assertTrue(mock_remove_call.called_once_with(mocked_directory[0]))
