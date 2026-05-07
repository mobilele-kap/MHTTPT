from app.exceptions import APPError

class SocketServerError(APPError):
    """Socket Server Error"""

class ClientNotFound(SocketServerError):
    """Client Not Found"""