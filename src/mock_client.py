from models import ConnectionsAddRequest, ConnectionsAddResponse, ConnectionType

class MockDeviceClient:
    def __init__(self, base_url:str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = "mock-token"

    def add_connection(self, request: ConnectionsAddRequest) -> ConnectionsAddResponse:
        """ Create a mock channel """
        
        return ConnectionsAddResponse(
            id="mock-id",
            gid="mock-gid",
            label=request.label if request.label else "mock-label",
            res="mock-res",
            type=request.type,
            helixnetEnabled=True
        )

    def close(self):
        # Simulate closing the session
        pass
