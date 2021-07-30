from dataclasses import dataclass
from typing import List, Any, Optional
from App.Json_Class.EdgeDeviceProperties_dto import EdgeDeviceProperties
from App.Json_Class.DtoUtilities import *
from App.Json_Class.DataCenter_dto import DataCenters
from App.Json_Class.DataService_dto import DataServices

@dataclass
class EdgeDevice:
    properties: EdgeDeviceProperties
    DataCenter: DataCenters
    DataService: DataServices

    @staticmethod
    def from_dict(obj: Any) -> 'EdgeDevice':
        assert isinstance(obj, dict)
        properties = EdgeDeviceProperties.from_dict(obj.get("properties"))
        DataCenter = DataCenters.from_dict(obj.get("DataCenter"))
        DataService = DataServices.from_dict(obj.get("DataService"))
        return EdgeDevice(properties, DataCenter, DataService)

    def to_dict(self) -> dict:
        result: dict = {}
        result["properties"] = to_class(EdgeDeviceProperties, self.properties)
        result["DataCenter"] = to_class(DataCenters, self.DataCenter)
        result["DataService"] = to_class(DataServices, self.DataService)
        return result