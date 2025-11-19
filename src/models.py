from enum import Enum

class ConnectionType(Enum):
    PARTYLINE = "partyline"
    GROUP = "group"
    FIXED_GROUP = "fixedGroup"
    DIRECT = "direct"

class ConnectionsAddRequest:
    def __init__(self, type:ConnectionType, label:str = None):
        self.type = type
        self.label = label

class ConnectionsAddResponse:
    def __init__(self, id:str, gid:str, label:str, res:str, type:ConnectionType, helixnetEnabled:bool):
        self.id = id
        self.gid = gid
        self.label = label
        self.res = res
        self.type = type
        self.helixnetEnabled = helixnetEnabled