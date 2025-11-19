import requests
import json
from typing import Optional
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
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse response JSON
            response_json = response.json()
            if (response_json["ok"] != True):
                raise ValueError("Failed to add connection: API returned not ok")

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
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            response_json = response.json()
            if (response_json["ok"] != True):
                raise ValueError("Failed to add roles: API returned not ok")
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to add roles: {e}")

    
    def close(self):
        """Close the HTTP session."""
        self.session.close()

if __name__ == "__main__":
    # Example usage
    client = DeviceClient(base_url="http://10.50.16.99", username="admin", password="admin")
    
    # add_request = ConnectionsAddRequest(type=ConnectionType.PARTYLINE)
    # add_response = client.add_connection(add_request)
    # print(f"Connection added with ID: {add_response.newConnection.id}")

    add_request = RolesAddRequest(label="NewRole", quantity=1, sessions=[RoleSessionType.FREESPEAK_4KEY, RoleSessionType.KEYPANEL_12KEY], singleKeysetPerType=False)
    client.add_roles(add_request)

    client.close()