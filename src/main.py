from fastmcp import FastMCP
import random
from typing import Optional, Dict, Any
from pydantic import BaseModel
from docs import *
from models import *

# Swap these around to flip between mock and real calls

#from device_client import DeviceClient
from mock_client import DeviceClient


mcp = FastMCP("ClearCom MCP Server")
client = DeviceClient(base_url="http://10.50.16.99", username="admin", password="admin")

@mcp.tool(name="getRoles", description=GET_ROLES_DOC)
def getRoles() -> list[str]:
    return client.get_role_names()

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


@mcp.tool(description=GET_CHANNELS_DOC)
def getChannels() -> list[str]:
    response: ConnectionsGetResponse = client.get_connections()
    channel_labels = [conn.label for conn in response.connections if conn.type == ConnectionType.PARTYLINE]
    return channel_labels

@mcp.tool(name="addChannel", description=ADD_CHANNEL_DOC)
def addChannel(
    label: str,
) -> bool:

    # Create the channel object
    req = ConnectionsAddRequest(type=ConnectionType.PARTYLINE, label=label)
    response = client.add_connection(req)

    return True

@mcp.tool(description=ASSIGN_CHANNEL_TO_ROLE_DOC)
def assignChannelToRole(
    roleLabel: str,
    channelLabel: str,
    isLatching: bool
) -> bool:
    
    client.assign_channel_to_role(channel_name=channelLabel, role_name=roleLabel, is_latching=isLatching)

    return True


if __name__ == "__main__":
    mcp.run()
