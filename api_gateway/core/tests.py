from unittest.mock import patch
from django.test import TestCase

from .permissions import get_user_info

class TestTokens(TestCase):
    @patch("core.permissions.jwt.decode")
    def test_tokens(self, mock_jwt_decode):
        # 1: no token
        request = type('Request', (object,), {'headers': {}})
        self.assertIsNone(get_user_info(request))

        # 2: invalid token
        request = type('Request', (object,), {'headers': {'Authorization': ''}})
        self.assertIsNone(get_user_info(request))

        # 3: valid token
        mock_jwt_decode.return_value = {'user_id': '1'}
        request = type('Request', (object,), {'headers': {'Authorization': 'Bearer token'}})
        self.assertEqual(get_user_info(request), {'user_id': '1'})
