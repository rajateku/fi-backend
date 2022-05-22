import unittest
import app
import handlers2
# from app import test
import download_save_playstore_data

class TestStringMethods(unittest.TestCase):

    def test_server(self):
        print(handlers2.test_handlers())
        # print(app.test())
        self.assertEqual(handlers2.test_handlers(), 'server working with git push')

    def test_playstore_data(self):
        self.assertTrue(len(download_save_playstore_data.test_scrape("com.roundpier.roundpier"))>1)
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()