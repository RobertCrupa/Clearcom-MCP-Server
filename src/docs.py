"""Documentation and help text for MCP tools."""


# Table for prompt:

"""
# **Instructions**
Using the clearcom MCP server, configure this table.

First begin by creating channels labeled with the columns name.

Secondly create roles using the keyset type for each row.

Finally, assign each channel to each role based on the table, where we use 1 to denote latching and 2 is non-latching.

# **Table to configure**

Role,Keyset,Production,Audio,Lighting,Lighting Spots,Automation,Stage,Ushers,Paging Lobby,Paging Backstage
Stage Manager,V-Series,1,1,1,,1,1,1,2,2
Audio FOH,HXII-RM,2,1,,,,,,,
Lighting FOH,V-Series,2,,1,1,,,,,
Automation,V-Series,2,,,,1,1,,,
Recording,HXII-RM,2,1,,,,,,,
Stage 1,FSIC-BP,2,,,,2,2,,,
Stage 2,FSII-BP,2,,,,2,2,,,
Stage 3,FSII-BP,2,,,,2,2,,,
Stage 4,FSII-BP,2,,,,2,2,,,
Stage 5,FSII-BP,2,,,,2,2,,,
Stage 6,FSII-BP,2,,,,2,2,,,
Stage Manager,FSIC-BP,1,1,1,,1,1,,,
Audio 1,FSIC-BP,2,1,,,,,,,
Audio 2,FSII-BP,2,1,,,,,,,
Lighting 1,FSIC-BP,2,,1,,,,,,
Lighting 2,FSII-BP,2,,1,,,,,,
Lighting 3,FSII-BP,2,,1,,,,,,
Lighting 4,FSII-BP,2,,1,,,,,,
Dresser & Props 1,FSII-BP,2,,,,,,,,
Dresser & Props 2,FSII-BP,2,,,,,,,,
Spots 1,HXII-BP,2,,,2,,,,,
Spots 2,HXII-BP,2,,,2,,,,,
Spots 3,HXII-BP,2,,,2,,,,,
Spots 4,HXII-BP,2,,,2,,,,,
Tech Table 1,HXII-KB,2,1,,,,,,,
Tech Table 2,HXII-KB,2,,1,,,,,,
Tech Table 3,HXII-KB,2,,,,1,,,,
Tech Table 4,HXII-KB,2,,,,,1,,,
Dressing Room 1,HXII-KB,2,,,,,,,,
Dressing Room 2,HXII-KB,2,,,,,,,,
Dressing Room 3,HXII-KB,2,,,,,,,,
Dressing Room 4,HXII-KB,2,,,,,,,,
House Manager 1,HXII-KB,,,,,,,,,2
House Manager 2,HXII-KB,,,,,,,,,2

"""

CREATE_ROLE_DOC = """
Create a mock role to mimic CCM's `POST /api/2/keysets` flow.

REQUIRED PARAMETERS:
  • label (str): Human-readable role name exposed to HelixNet endpoints
  • role_type (str): HelixNet keyset type from supported options:
    - "HRM-4X", "HKB-2X", "HBP-2X" 
    - "HXII-BP", "HXII-BP-4K", "HXII-BP-8K"
    - "HRM-22", "HKB-1X"

OPTIONAL PARAMETERS:
  • description (str): Short summary displayed in UI
  • isDefault (bool): Mark as station default (default: False)
  • settings (dict): Configuration payload mirroring keysets_post_add_2 schema
    - For testing: {"keysets": [], "groups": []}
    - For real data: populate with DB-style entries, volumes, stackedKey flags, etc.

BEHAVIOR:
  • Returns CreateRoleResponse with success status, generated roleId, and role object
  • Generates CCM-style resource URI: /api/2/keysets/{roleId}
  • No persistence or backend calls - pure mock for MCP integration testing
  • Input validation relies on Pydantic models; no runtime errors raised

EXAMPLE USAGE:
  createRole(
    label="Front Desk HRM",
    role_type="HRM-4X", 
    description="Reception default",
    settings={"keysets": [], "groups": []}
  )

RETURNS:
  {
    "ok": true,
    "roleId": 1234,
    "role": {
      "id": 1234,
      "res": "/api/2/keysets/1234",
      "label": "Front Desk HRM",
      "type": "HRM-4X",
      "description": "Reception default",
      "isDefault": false,
      "settings": {"keysets": [], "groups": []}
    }
  }
"""


ADD_PARTYLINE_DOC = """
Create a partyline entity with a Human-readable name

REQUIRED PARAMETERS:
  • label (str): Human-readable name 

OPTIONAL PARAMETERS:
  

BEHAVIOR:

EXAMPLE USAGE:


RETURNS:
  {
    "ok": true,
    "gidResponse": 78293748923789
  }
  
"""
