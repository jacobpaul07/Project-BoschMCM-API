from App.Json_Class.COMPort_dto import Comport
from App.Json_Class.COMProperties_dto import COMPORTProperties
from App.Json_Class.COMdeviceProperties_dto import COMdeviceProperties
from App.Json_Class.DtoUtilities import to_class
from App.Json_Class.EdgeDeviceProperties_dto import EdgeDeviceProperties
from App.Json_Class import index as config, Edge, TCPdevice_dto
from typing import Any, List, TypeVar, Type, cast, Callable

from App.Json_Class.TCPProperties_dto import TCPProperties
from App.Json_Class.TCP_dto import TCPs
from App.Json_Class.TCPdeviceProperties_dto import TCPdeviceProperties


def updateGenericdeviceObject(requestData, jsonProperties):
    for key in requestData:
        value = requestData[key]
        for objectKey in jsonProperties:
            # for device_key in properties:
            if objectKey == key:
                jsonProperties[key] = value
    return jsonProperties


def updateConfig(jsonData):
    updated_json_data = jsonData.to_dict()
    print(updated_json_data)
    config.write_setting(updated_json_data)


class ConfigComProperties:

    def updateComPortProperties(self, requestData, portName):
        jsonData: Edge = config.read_setting()
        port: Comport = jsonData.edgedevice.DataCenter.__getattribute__(portName)
        jsonProperties = port.properties.to_dict()
        for key in requestData:
            value = requestData[key]
            if key == "SerialPort Setting":
                jsonProperties[key] = updateGenericdeviceObject(value, jsonProperties[key])
            else:
                for objectKey in jsonProperties:
                    if objectKey == key:
                        jsonProperties[key] = value

        cast(Comport,
             jsonData.edgedevice.DataCenter.__getattribute__(portName)).properties = COMPORTProperties.from_dict(
            jsonProperties)
        updateConfig(jsonData)
        return "success"


class ConfigTcpProperties:

    def updateTcpPortProperties(self, requestData):
        jsonData: Edge = config.read_setting()
        port: TCPs = jsonData.edgedevice.DataCenter.TCP
        jsonProperties = port.properties.to_dict()
        for key in requestData:
            value = requestData[key]
            for objectKey in jsonProperties:
                if objectKey == key:
                    jsonProperties[key] = value
        jsonData.edgedevice.DataCenter.TCP.properties = TCPProperties.from_dict(jsonProperties)
        print(jsonData)
        updateConfig(jsonData)


class ConfigComDevicesProperties:

    def updateComDeviceProperties(self, requestData, portName, deviceName):
        jsonData: Edge = config.read_setting()
        port: Comport = jsonData.edgedevice.DataCenter.__getattribute__(portName)
        comDeviceProperties = None

        for comDevice in port.devices:
            if comDevice.properties.Name == deviceName:
                comDeviceProperties = comDevice.properties.to_dict()

        if comDeviceProperties is not None:
            for key in requestData:
                value = requestData[key]

                if key == "Extention Properties":
                    comDeviceProperties[key] = updateGenericdeviceObject(value, comDeviceProperties[key])

                for propertyKey in comDeviceProperties:
                    if propertyKey == key:
                        comDeviceProperties[key] = value

            for comDevice in port.devices:
                if comDevice.properties.Name == deviceName:
                    comDevice.properties = COMdeviceProperties.from_dict(comDeviceProperties)

            if portName == "COM1":
                jsonData.edgedevice.DataCenter.COM1 = port
            elif portName == "COM2":
                jsonData.edgedevice.DataCenter.COM2 = port

            print(jsonData.edgedevice.DataCenter.COM1.devices)
            updateConfig(jsonData)
            return "success"
        else:
            return "Tcp device not found"


class ConfigTCPDevicesProperties:

    def updateTCPDeviceProperties(self, requestData, deviceName):
        jsonData: Edge = config.read_setting()
        tcpDeviceProperties = None

        for tcpDevice in jsonData.edgedevice.DataCenter.TCP.devices:
            if tcpDevice.properties.Name == deviceName:
                tcpDeviceProperties = tcpDevice.properties.to_dict()

        if tcpDeviceProperties is not None:
            for key in requestData:
                value = requestData[key]

                if key == "Extention Properties" or key == "TCP/IP":
                    tcpDeviceProperties[key] = updateGenericdeviceObject(value, tcpDeviceProperties[key])

                for propertyKey in tcpDeviceProperties:
                    if propertyKey == key:
                        tcpDeviceProperties[key] = value

            for tcpDevice in jsonData.edgedevice.DataCenter.TCP.devices:
                if tcpDevice.properties.Name == deviceName:
                    tcpDevice.properties = TCPdeviceProperties.from_dict(tcpDeviceProperties)

            updateConfig(jsonData)
            return "success"
        else:
            return "Tcp device not found"



