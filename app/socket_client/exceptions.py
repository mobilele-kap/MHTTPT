from app.exceptions import APPError

class SocketClientError(APPError):
    """Socket Client Error"""

class ConnectionsOverflow(SocketClientError):
    """Exceeding the connection limit"""

class ConnectionsNotFound(SocketClientError):
    """Exceeding the connection limit"""