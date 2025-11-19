"""Documentation and help text for MCP tools."""

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
