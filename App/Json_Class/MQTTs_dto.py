from dataclasses import dataclass
from App.Json_Class.DtoUtilities import *


@dataclass
class mqtts:
    Enable: str
    
    @staticmethod
    def from_dict(obj: Any) -> 'mqtts':
        assert isinstance(obj, dict)
        Enable = from_str(obj.get("Enable"))
        return mqtts(Enable)

    def to_dict(self) -> dict:
        result: dict = {"Enable": from_str(self.Enable)}
        return result
