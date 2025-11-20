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
Create a role with a label and keyset type.

REQUIRED PARAMETERS:
  • label (str): Human-readable role name (1-10 characters)
  • keyset_type (RoleSessionType): Role keyset type enum from supported options:
    - RoleSessionType.FREESPEAK_4KEY: FreeSpeak II 4-Key Beltpack
    - RoleSessionType.FREESPEAK_8KEY: FreeSpeak Edge 8-Key Beltpack
    - RoleSessionType.HELIXNET_BP: HelixNet Beltpack
    - RoleSessionType.HELIXNET_RM: HelixNet Remote Station
    - RoleSessionType.HELIXNET_KB: HelixNet Speaker Station
    - RoleSessionType.KEYPANEL_12KEY: V-Series Keypanel 12-Key
    - RoleSessionType.KEYPANEL_24KEY: V-Series Keypanel 24-Key
    - RoleSessionType.KEYPANEL_32KEY: V-Series Keypanel 32-Key

EXAMPLE USAGE:
  createRole(
    label="Front Desk HRM",
    keyset_type=RoleSessionType.HELIXNET_RM
  )

RETURNS:
  • True if the role was successfully created
"""


ADD_CHANNEL_DOC = """
Create a channel with a label.

REQUIRED PARAMETERS:
  • label (str): Human-readable name for the new channel (1-10 characters) (must be unique)

BEHAVIOR:

EXAMPLE USAGE:
  addChannel(
    label="Production"
  )

RETURNS:
  • True if the role was successfully created
  
"""
