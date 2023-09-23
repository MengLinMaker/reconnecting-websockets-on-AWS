import unittest
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import index

class testIndexHandler(unittest.TestCase):

  def test_no_connection_id(self):
    event = {}
    output = index.handler(event, None)
    expected = index.response(400, 'Request requestContext.connectionId does not exist')
    self.assertEqual(output, expected)

  def test_has_connection_id(self):
    event = {
      'requestContext': {
        'connectionId': '1'
      }
    }
    output = index.handler(event, None)
    expected = index.response(400, 'Handler failed to execute')
    self.assertEqual(output, expected)

if __name__ == '__main__':
  unittest.main()