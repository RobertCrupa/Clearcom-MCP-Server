from fastmcp import FastMCP
import random
from typing import Optional, Dict, Any
from pydantic import BaseModel
from docs import *
from models import *
from device_client import DeviceClient
from mock_client import MockDeviceClient


mcp = FastMCP("ClearCom MCP Server")
#client = DeviceClient(base_url="http://10.50.16.99", username="admin", password="admin")
client = MockDeviceClient(base_url="http://10.50.16.99", username="admin", password="admin")


@mcp.tool(name="createRole", description=CREATE_ROLE_DOC)
def createRole(
    label: str,
    keyset_type: RoleSessionType
) -> bool:

    # Create the role object
    role = RolesAddRequest(label, 1, [RoleSessionType(keyset_type)])
    client.add_roles(role)

    # Return the response
    return True

class addPartylineResponse(BaseModel):
    ok: bool
    gidResponse: int


@mcp.tool(name="addChannel", description=ADD_CHANNEL_DOC)
def addChannel(
    label: str,
) -> bool:
    ADD_CHANNEL_DOC

    # Create the channel object
    req = ConnectionsAddRequest(type=ConnectionType.PARTYLINE, label=label)
    response = client.add_connection(req)

    return True


if __name__ == "__main__":
    mcp.run()
