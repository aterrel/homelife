from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class TestTokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    test_token = 'test-token-1234'

    def authenticate(self, request):
        logger.debug("Starting test authentication")
        
        auth = get_authorization_header(request).decode('utf-8')
        logger.debug(f"Raw auth header: {auth}")
        
        if not auth:
            logger.debug("No auth header found")
            return None
            
        parts = auth.split()
        
        if len(parts) == 0:
            logger.debug("Empty auth header")
            return None
            
        # Get the last part as the token, whether it has 'Bearer' or not
        token = parts[-1].strip()
        logger.debug(f"Extracted token: {token}")
        
        if token == self.test_token:
            logger.debug("Test token matched")
            user, _ = User.objects.get_or_create(
                username='test_user',
                defaults={
                    'email': 'test@example.com',
                    'is_active': True,
                    'is_staff': True,
                }
            )
            return (user, token)
            
        logger.debug("Test token did not match")
        return None

    def authenticate_header(self, request):
        return 'Bearer'
