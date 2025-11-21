from typing import Any
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

    def add_connection(self, req):
        print(f"Called add_connection with request={req}")
    
    def delete_connection(self, connection_id: int) -> None:
        """
        Makes a DELETE request to /api/1/connections/{id} to delete a connection.
        
        Args:
            connection_id: ID of the connection to delete
        """
        pass

    def get_roles(self) -> list[dict[str, Any]]:
        """
        Makes a GET request to /api/2/rolesets to fetch the list of rolesets.
        
        Returns:
            List of rolesets as dictionaries
        """
        return []
            
    def add_roles(self, request: RolesAddRequest) -> None:
        """
        Makes a POST request to /api/2/rolesets/create to add new roles.
        
        Args:
            request: RolesAddRequest object containing the role details
            
        Raises:
            requests.RequestException: If the HTTP request fails
        """
        pass

    def delete_role(self, roleset_id: int) -> None:
        """
        Makes a DELETE request to /api/2/rolesets/{id} to delete a role.
        
        Args:
            roleset_id: ID of the roleset to delete
        """
        pass

    def get_keysets(self) -> list[dict[str, Any]]:
        """
        Makes a GET request to /api/2/keysets to fetch the list of keysets.
        
        Returns:
            List of keysets as dictionaries
        """
        return []

    def get_role_channel_assignments(self, role_name):
        print(f"Called get_role_channel_assignments with role_name={role_name}")
        return []

    def set_role_channel_assignments(self, role_name: str, channel_names: list[str], is_latchings: list[bool]) -> None:
        print(f"Called set_role_channel_assignments with role_name={role_name}, channel_names={channel_names}, is_latchings={is_latchings}")
        pass


    def close(self):
        """Close the HTTP session."""
        pass
