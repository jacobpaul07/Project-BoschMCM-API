from dataclasses import dataclass
from App.Json_Class.DtoUtilities import *
from App.Json_Class.MQTTs_dto import mqtts
from App.Json_Class.PPMP_dto import Ppmps


@dataclass
class DataServices:
    PPMP: Ppmps
    MQTT: mqtts

    @staticmethod
    def from_dict(obj: Any) -> 'DataServices':
        assert isinstance(obj, dict)
        PPMP = Ppmps.from_dict(obj.get("PPMP"))
        MQTT = mqtts.from_dict(obj.get("MQTT"))
        return DataServices(PPMP, MQTT)

    def to_dict(self) -> dict:
        result: dict = {"PPMP": to_class(Ppmps, self.PPMP), "MQTT": to_class(mqtts, self.MQTT)}
        return result
