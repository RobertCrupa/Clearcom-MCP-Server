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

GET_ROLE_CHANNEL_ASSIGNMENTS_DOC = """
Retrieve a list of channel labels assigned to a specific role in the ClearCom MCP system.

REQUIRED PARAMETERS:
  • roleLabel (str): The label of the role to fetch channel assignments for.

RETURNS:
  • list[str]: A list of channel labels assigned to the specified role.

Use this tool to see which channels (a.k.a. partylines) are assigned to a specific role.
"""

ASSIGN_CHANNEL_TO_ROLE_DOC = """
Assigns a channel to a role in the ClearCom MCP system.

REQUIRED PARAMETERS:
  • roleLabel (str): The label of the role to assign the channel to.
  • channelLabel (str): The label of the channel to be assigned.
  • isLatching (bool): True if set to latching.

RETURNS:
  • bool: True if the assignment was successful, False otherwise.

Use this tool to link a specific channel (a.k.a. partyline).
"""

GET_ROLES_DOC = """
Retrieve a list of all role labels and corresponding keyset types from the ClearCom MCP system.

RETURNS:
  • list[RoleInfo]: A list of RoleInfo objects containing role labels and keyset types. (see RoleInfo structure below)

RoleInfo Structure:
  • label (str): The human-readable name of the role.
  • keyset_type (RoleSessionType): Role keyset type enum from supported options:
    - RoleSessionType.FREESPEAK_4KEY: FreeSpeak II 4-Key Beltpack
    - RoleSessionType.FREESPEAK_8KEY: FreeSpeak Edge 8-Key Beltpack
    - RoleSessionType.HELIXNET_BP: HelixNet Beltpack
    - RoleSessionType.HELIXNET_RM: HelixNet Remote Station
    - RoleSessionType.HELIXNET_KB: HelixNet Speaker Station
    - RoleSessionType.KEYPANEL_12KEY: V-Series Keypanel 12-Key
    - RoleSessionType.KEYPANEL_24KEY: V-Series Keypanel 24-Key
    - RoleSessionType.KEYPANEL_32KEY: V-Series Keypanel 32-Key
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

DELETE_ROLE_DOC = """
Delete the role with the specified label.

REQUIRED PARAMETERS:
  • label (str): Human-readable name for the role to delete (1-10 characters) (must already exist)

EXAMPLE USAGE:
  deleteRole(
    label="Front Desk HRM"
  )

RETURNS:
  • True if the role was successfully deleted
"""

GET_CHANNELS_DOC = """
Retrieve a list of all partyline channel labels from the ClearCom MCP system.

RETURNS:
  • list[str]: A list of channel labels (str) for all partyline channels."""

ADD_CHANNEL_DOC = """
Create a channel with a label.

REQUIRED PARAMETERS:
  • label (str): Human-readable name for the new channel (1-10 characters) (must be unique)

EXAMPLE USAGE:
  addChannel(
    label="Production"
  )

RETURNS:
  • True if the role was successfully created
  
"""

DELETE_CHANNEL_DOC = """
Delete the channel with the specified label.

REQUIRED PARAMETERS:
  • label (str): Human-readable name for the channel to delete (1-10 characters) (must already exist)

EXAMPLE USAGE:
  deleteChannel(
    label="Production"
  )

RETURNS:
  • True if the channel was successfully deleted
"""