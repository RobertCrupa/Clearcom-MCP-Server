from models import *

class DeviceClient:
    def __init__(self, base_url:str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password


    def authenticate(self) -> None:
        pass

    def get_connections(self) -> ConnectionsGetResponse:
        """
        Makes a GET request to /api/1/connections to fetch the list of connections.
        
        Returns:
            ConnectionsGetResponse object containing the list of connections
            
        Raises:
            requests.RequestException: If the HTTP request fails
            ValueError: If the response cannot be parsed
        """

        return ConnectionsGetResponse(connections=[])
            
    def add_roles(self, request: RolesAddRequest) -> None:
        """
        Makes a POST request to /api/2/rolesets/create to add new roles.
        
        Args:
            request: RolesAddRequest object containing the role details
            
        Raises:
            requests.RequestException: If the HTTP request fails
        """
        pass


    def close(self):
        """Close the HTTP session."""
        pass
