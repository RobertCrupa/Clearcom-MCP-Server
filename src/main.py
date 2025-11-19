from fastmcp import FastMCP
import random
from typing import Optional, Dict, Any
from pydantic import BaseModel
from docs import CREATE_ROLE_DOC
from docs import ADD_PARTYLINE_DOC

# Define the request and response models
class CreateRoleRequest(BaseModel):
    label: str
    type: str
    description: Optional[str] = None
    isDefault: Optional[bool] = None
    settings: Optional[Dict[str, Any]] = None


class Role(BaseModel):
    id: int
    res: str
    label: str
    type: str
    description: str
    isDefault: bool
    settings: Dict[str, Any]


class CreateRoleResponse(BaseModel):
    ok: bool
    roleId: int
    role: Role


mcp = FastMCP("ClearCom MCP Server")



@mcp.tool
def createRole(
    label: str,
    role_type: str,
    description: Optional[str] = None,
    isDefault: Optional[bool] = None,
    settings: Optional[Dict[str, Any]] = None,
) -> CreateRoleResponse:

    
    # Generate a random ID like in the original TypeScript code
    generated_id = random.randint(1, 10000)

    # Create the role object
    role = Role(
        id=generated_id,
        res=f"/api/2/keysets/{generated_id}",
        label=label,
        type=role_type,
        description=description or "",
        isDefault=isDefault or False,
        settings=settings or {},
    )

    # Return the response
    return CreateRoleResponse(ok=True, roleId=generated_id, role=role)




class addPartylineResponse(BaseModel):
    ok: bool
    gidResponse: int


@mcp.tool
def addPartyLine(
    label: str,
) -> addPartylineResponse:
    ADD_PARTYLINE_DOC
    # Create a Partyline 
    # Generate a string ID (simulate unique identifier)
   
    return addPartylineResponse(ok=True, gidResponse=7)


class addGroupResponse(BaseModel):
    ok: bool
    gidResponse:str

@mcp.tool
def addGroup(
     label:str,
) -> addGroupResponse:
    ADD_GROUP_DOC
    # create a Group
    return True

class addFixedGroupResponse(BaseModel):
    ok: bool
    gidResponse:str

@mcp.tool
def addFixedGroup(
    label:str,
) -> addFixedGroupResponse:
    ADD_FIXED_GROUP_DOC
    # create a Fixed Group
    return True


class addDirectResponse(BaseModel):
    ok: bool
    gidResponse:str
    
@mcp.tool
def addDirect(
    label:str,
    type: str,  # 4-Wire, DANTE, AES67 or IVC
) -> addDirectResponse:
    ADD_DIRECT_DOC
    # create a Fixed Group
    return addDirectResponse(ok=True,gidResponse=1)


if __name__ == "__main__":
    mcp.run()
