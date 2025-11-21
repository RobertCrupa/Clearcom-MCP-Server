import requests
import json
from typing import Any, Optional
from models import *
import base64

class DeviceClient:
    def __init__(self, base_url:str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.authenticate()
    
    def authenticate(self):
        """
        Authenticates with the device and stores the session token.
        
        Raises:
            requests.RequestException: If the HTTP request fails
            ValueError: If authentication fails
        """
        url = f"{self.base_url}/auth/token"

        # Create base64 encoded credentials
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        
        try:
            response = self.session.post(
                url,
                headers={"Content-Type": "application/json", "Authorization": f"Basic {encoded_credentials}"},
                timeout=30
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            response_json = response.json()
            self.token = response_json.get("token")
            
            if not self.token:
                raise ValueError("Authentication failed: No token received")
            
            # Set the Authorization header for future requests
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to authenticate: {e}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Failed to parse authentication response: {e}")

    def get_connections(self) -> ConnectionsGetResponse:
        """
        Makes a GET request to /api/1/connections to fetch the list of connections.
        
        Returns:
            ConnectionsGetResponse object containing the list of connections
            
        Raises:
            requests.RequestException: If the HTTP request fails
            ValueError: If the response cannot be parsed
        """
        url = f"{self.base_url}/api/1/connections"
        
        try:
            response = self.session.get(
                url,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse response JSON
            response_json = response.json()
            connections_data = response_json
            
            # Deserialize response into ConnectionsGetResponse object
            connections = []
            for conn_data in connections_data:
                connection = ConnectionInfo(
                    id=conn_data["id"],
                    gid=conn_data["gid"],
                    label=conn_data["label"],
                    res=conn_data["res"],
                    type=ConnectionType(conn_data["type"]),
                    helixnetEnabled=conn_data.get("helixnetEnabled", False)
                )
                connections.append(connection)
            
            return ConnectionsGetResponse(connections)
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to get connections: {e}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Failed to parse response: {e}")
    
    def add_connection(self, request: ConnectionsAddRequest) -> ConnectionsAddResponse:
        """
        Makes a POST request to /api/1/connections to add a new connection.
        
        Args:
            request: ConnectionsAddRequest object containing the connection details
            
        Returns:
            ConnectionsAddResponse object with the created connection details
            
        Raises:
            requests.RequestException: If the HTTP request fails
            ValueError: If the response cannot be parsed
        """
        url = f"{self.base_url}/api/1/connections"
        
        # Serialize request to JSON
        request_data = {
            "type": request.type.value,
        }
        
        # Add label if provided
        if request.label is not None:
            request_data["label"] = request.label
        
        try:
            response = self.session.post(
                url,
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            # Parse response JSON
            response_json = response.json()
            if (response_json["ok"] != True):
                raise ValueError(f"Failed to add connection: {response_json['message']}")
            
            # Raise an exception for bad status codes
            response.raise_for_status()

            new_connection = response_json["newConnection"]
            
            # Deserialize response into ConnectionsAddResponse object
            return ConnectionsAddResponse(ConnectionInfo(
                id=new_connection["id"],
                gid=new_connection["gid"],
                label=new_connection["label"],
                res=new_connection["res"],
                type=ConnectionType(new_connection["type"]),
                helixnetEnabled=new_connection["helixnetEnabled"]
            ))
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to add connection: {e}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Failed to parse response: {e}")
    
    def delete_connection(self, connection_id: int) -> None:
        """
        Makes a DELETE request to /api/1/connections/{id} to delete a connection.
        
        Args:
            connection_id: ID of the connection to delete
        """
        url = f"{self.base_url}/api/1/connections/{connection_id}"
        
        try:
            response = self.session.delete(
                url,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            response_json = response.json()
            if (response_json["ok"] != True):
                raise ValueError(f"Failed to delete connection: {response_json['message']}")

            # Raise an exception for bad status codes
            response.raise_for_status()
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to delete connection: {e}")
    
    def get_roles(self) -> list[dict[str, Any]]:
        """
        Makes a GET request to /api/2/rolesets to fetch the list of rolesets.
        
        Returns:
            List of rolesets as dictionaries
        """
        url = f"{self.base_url}/api/2/rolesets"
        
        try:
            response = self.session.get(
                url,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse response JSON
            response_json = response.json()
            
            return response_json
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to get rolesets: {e}")
    
    def get_role_names(self) -> list[str]:
        """
        Retrieves the list of role names from the rolesets.
        
        Returns:
            List of role names (str)
        """
        rolesets = self.get_roles()
        role_names = [roleset["label"] for roleset in rolesets]
        return role_names
    
    def add_roles(self, request: RolesAddRequest) -> None:
        """
        Makes a POST request to /api/2/rolesets/create to add new roles.
        
        Args:
            request: RolesAddRequest object containing the role details
            
        Raises:
            requests.RequestException: If the HTTP request fails
        """
        url = f"{self.base_url}/api/2/rolesets/create"
        
        # Serialize request to JSON
        request_data = {
            "label": request.label,
            "quantity": request.quantity,
            "sessions": request.sessions,
            "singleKeysetPerType": request.singleKeysetPerType
        }
        
        try:
            response = self.session.post(
                url,
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            response_json = response.json()
            if (response_json["ok"] != True):
                raise ValueError(f"Failed to add roles: {response_json['message']}")
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to add roles: {e}")
    
    def delete_role(self, roleset_id):
        """
        Makes a DELETE request to /api/2/rolesets/{id} to delete a roleset.
        
        Args:
            roleset_id: ID of the roleset to delete
        """
        url = f"{self.base_url}/api/2/rolesets/{roleset_id}"
        
        try:
            response = self.session.delete(
                url,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            response_json = response.json()
            if (response_json["ok"] != True):
                raise ValueError(f"Failed to delete roleset: {response_json['message']}")

            # Raise an exception for bad status codes
            response.raise_for_status()
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to delete roleset: {e}")
    
    def get_keysets(self) -> list[dict[str, Any]]:
        """
        Makes a GET request to /api/2/keysets to fetch the list of keysets.
        
        Returns:
            List of keysets as dictionaries
        """
        url = f"{self.base_url}/api/2/keysets"
        
        try:
            response = self.session.get(
                url,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse response JSON
            response_json = response.json()
            
            return response_json
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to get keysets: {e}")
    
    def assign_channel_to_role(self, channel_name: str, role_name: str, is_latching: bool) -> None:
        """
        Assigns a channel to a role.
        
        Args:
            channel_name: Name of the channel to assign
            role_name: Name of the role to assign the channel to
            is_latching: Whether the key is latching or not
            
        Raises:
            requests.RequestException: If the HTTP request fails
        """
        
        try:
            connections = self.get_connections()
            this_channel_list = [conn for conn in connections.connections if conn.label == channel_name and conn.type == ConnectionType.PARTYLINE]
            if len(this_channel_list) != 1:
                raise ValueError(f"Channel '{channel_name}' not found or multiple channels with same name exist.")
            this_channel = this_channel_list[0]

            keysets = self.get_keysets()
            this_keyset_list = [ks for ks in keysets if ks["label"] == role_name]
            if len(this_keyset_list) != 1:
                raise ValueError(f"Role '{role_name}' not found or multiple roles with same name exist.")
            this_keyset = this_keyset_list[0]

            for key in this_keyset["settings"]["keysets"]:
                if len(key["entities"]) == 0:
                    key["entities"].append({
                        "gid": this_channel.gid,
                        "res": this_channel.res,
                        "type": 0 # Assuming adding a channel connection
                    })
                    key["talkBtnMode"] = "latching" if is_latching else "non-latching"
                    break
            
            request_data = {
                "settings": this_keyset["settings"],
                "type": this_keyset["type"]
            }

            url = f"{self.base_url}/api/2/keysets/{this_keyset['id']}"
            response = self.session.put(
                url,
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            # Parse response JSON
            response_json = response.json()
            if (response_json["ok"] != True):
                raise ValueError(f"Failed to assign channel to role: {response_json['message']}")
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to assign channel to role: {e}")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()

if __name__ == "__main__":
    # Example usage
    client = DeviceClient(base_url="http://10.50.16.99", username="admin", password="admin")

    # get_response = client.get_connections()
    # print(f"Connections: {', '.join([conn.label for conn in get_response.connections])}")
    
    # add_request = ConnectionsAddRequest(type=ConnectionType.PARTYLINE, label="Production")
    # add_response = client.add_connection(add_request)
    # print(f"Connection added with ID: {add_response.newConnection.id}")

    # client.delete_connection(1)

    # add_request = RolesAddRequest(label="NewRole", quantity=1, sessions=[RoleSessionType.FREESPEAK_4KEY, RoleSessionType.KEYPANEL_12KEY], singleKeysetPerType=False)
    # client.add_roles(add_request)

    # client.delete_role(2)

    # client.assign_channel_to_role(channel_name="Channel 1", role_name="test")

    client.close()