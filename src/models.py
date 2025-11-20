from enum import Enum

class ConnectionType(str, Enum):
    PARTYLINE = "partyline"
    GROUP = "group"
    FIXED_GROUP = "fixedGroup"
    DIRECT = "direct"

class ConnectionInfo:
    def __init__(self, id:str, gid:str, label:str, res:str, type:ConnectionType, helixnetEnabled:bool):
        self.id = id
        self.gid = gid
        self.label = label
        self.res = res
        self.type = type
        self.helixnetEnabled = helixnetEnabled

class ConnectionsGetResponse:
    def __init__(self, connections:list[ConnectionInfo]):
        self.connections = connections

class ConnectionsAddRequest:
    def __init__(self, type:ConnectionType, label:str = None):
        self.type = type
        self.label = label

class ConnectionsAddResponse:
    def __init__(self, newConnection:ConnectionInfo):
        self.newConnection = newConnection

class RoleSessionType(str, Enum):
    FREESPEAK_4KEY = "B.FSII"
    FREESPEAK_8KEY = "B.EDGE"
    HELIXNET_BP = "B.HBP"
    HELIXNET_RM = "B.HRM"
    HELIXNET_KB = "B.HKB"
    KEYPANEL_12KEY = "P.V12"
    KEYPANEL_24KEY = "P.V24"
    KEYPANEL_32KEY = "P.V32"

class RolesAddRequest:
    def __init__(self, label:str, quantity:int, sessions:list[RoleSessionType], singleKeysetPerType:bool = False):
        if len(label) > 10 or len(label) == 0:
            raise ValueError("Label must be between 1 and 10 characters long.")
        if quantity < 1 or quantity > 99:
            raise ValueError("Quantity must be between 1 and 99.")
        self.label = label
        self.quantity = quantity
        self.sessions = sessions
        self.singleKeysetPerType = singleKeysetPerType