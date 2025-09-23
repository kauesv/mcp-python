from mcp.server.auth.provider import AccessToken, TokenVerifier
from logs.logging import get_logger

logger = get_logger("token_verifier")


class StaticTokenVerifier(TokenVerifier):
    """Simple token verifier that checks against a static API key."""
    
    def __init__(self, token: str, client_id: str = "static-client", scopes: list[str] | None = None):
        """Initialize the static token verifier.
        
        Args:
            token: The valid API key token
            client_id: Client identifier for the token
            scopes: List of scopes granted to this token
        """
        self.valid_token = token
        self.client_id = client_id
        self.scopes = scopes or ["read", "write"]
        logger.info(f"StaticTokenVerifier initialized for client: {client_id}")
    
    async def verify_token(self, token: str) -> AccessToken | None:
        """Verify the provided token against the static API key.
        
        Args:
            token: The token to verify
            
        Returns:
            AccessToken if valid, None otherwise
        """
        if token == self.valid_token:
            logger.debug(f"Token verification successful for client: {self.client_id}")
            return AccessToken(
                token=token,
                client_id=self.client_id,
                scopes=self.scopes,
                expires_at=None  # No expiration for static tokens
            )
        
        logger.warning("Token verification failed: invalid token provided")
        return None
