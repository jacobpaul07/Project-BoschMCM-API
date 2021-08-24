from App.Json_Class.COMPort_dto import Comport
from App.Json_Class.COMProperties_dto import COMPORTProperties
from App.Json_Class.DtoUtilities import to_class
from App.Json_Class.EdgeDeviceProperties_dto import EdgeDeviceProperties
from App.Json_Class import index as config, Edge, TCPdevice_dto
from typing import Any, List, TypeVar, Type, cast, Callable

from App.Json_Class.TCPProperties_dto import TCPProperties
from App.Json_Class.TCP_dto import TCPs


class ConfigComProperties:

    @staticmethod
    def updateSerialPortSettings(requestData, jsonProperties):
        for key in requestData:
            value = requestData[key]
            for objectKey in jsonProperties:
                # for device_key in properties:
                if objectKey == key:
                    jsonProperties[key] = value
        return jsonProperties

    def updateComPortProperties(self, requestData, portName):
        jsonData: Edge = config.read_setting()
        port: Comport = jsonData.edgedevice.DataCenter.__getattribute__(portName)
        jsonProperties = port.properties.to_dict()
        for key in requestData:
            value = requestData[key]
            if key == "SerialPort Setting":
                jsonProperties[key] = self.updateSerialPortSettings(value, jsonProperties[key])
            else:
                for objectKey in jsonProperties:
                    if objectKey == key:
                        jsonProperties[key] = value

        cast(Comport,
             jsonData.edgedevice.DataCenter.__getattribute__(portName)).properties = COMPORTProperties.from_dict(
            jsonProperties)
        self.updateConfig(jsonData)
        return "Success"

    @staticmethod
    def updateConfig(jsonData):
        updated_json_data = jsonData.to_dict()
        print(updated_json_data)
        config.write_setting(updated_json_data)


class ConfigTcpProperties:

    def updateTcpPortProperties(self, requestData):
        jsonData: Edge = config.read_setting()
        port = jsonData.edgedevice.DataCenter.TCP
        jsonProperties = port.properties.to_dict()
        for key in requestData:
            value = requestData[key]
            for objectKey in jsonProperties:
                if objectKey == key:
                    jsonProperties[key] = value
        jsonData.edgedevice.DataCenter.TCP.properties = TCPProperties.from_dict(jsonProperties)
        print(jsonData)
        self.updateConfig(jsonData)

    @staticmethod
    def updateConfig(jsonData):
        updated_json_data = jsonData.to_dict()
        print(updated_json_data)
        config.write_setting(updated_json_data)
