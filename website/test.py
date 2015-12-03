from hello import app

import os
import unittest

class Test(unittest.TestCase):
    def setUp(self):
	self.app = app.test_client()

    def test_index(self):
	rv = self.app.get('/')
	self.assertEqual(200, rv.status_code)

    def test_send(self):
	rv = self.app.post('/send', data=dict(message= 'message'))
	self.assertEqual(400, rv.status_code)
    
    def test_send_message(self):
	rv = self.app.post('/send', data=dict(message='testing'))
	self.assertTrue(rv.data, 'testing') 

    def test_time(self):
	rv = self.app.post('/timeset', data=dict(timeset='B100T000C'))
	self.assertTrue(rv.data, '100') 

    def test_time_deleted(self):
	rv = self.app.post('/timeset', data=dict(timeset='B100T000C'))
	self.assertNotEqual(rv.data, '000')

if __name__ == '__main__':
    unittest.main()
