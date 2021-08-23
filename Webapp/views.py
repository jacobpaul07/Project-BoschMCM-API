import json
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from App.Json_Class import index as config, Edge, TCPdevice_dto
from typing import Any, List, Optional, TypeVar, Type, cast, Callable

from App.Json_Class.EdgeDeviceProperties_dto import EdgeDeviceProperties
from App.PPMP.PPMP_Services import start_ppmp_post
from App.RTUReaders.modbus_rtu import modbus_rtu
from App.TCPReaders.modbus_tcp import modbus_tcp
import App.globalsettings as appsetting


# Create your views here.
class ConfigIpChange(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        requestData = json.loads(data)
        ip: str = requestData["ip"]
        port: str = requestData["port"]
        deviceName: str = requestData["deviceName"]

        jsonData: Edge = config.read_setting()
        for tcpDevice in jsonData.edgedevice.DataCenter.TCP.devices:
            if tcpDevice.properties.Name == deviceName:
                tcpDevice.properties.TCPIP.IPAdress = ip
                tcpDevice.properties.TCPIP.PortNumber = port
        print(jsonData)
        updated_json_data = jsonData.to_dict()
        print(updated_json_data)
        config.write_setting(updated_json_data)

        return HttpResponse('success', "application/json")


class StartTcpService(APIView):

    def post(self, request):
        appsetting.startTcpService = True
        modbus_tcp()
        return HttpResponse('success', "application/json")


class StopTcpService(APIView):

    def post(self, request):
        appsetting.startTcpService = False
        modbus_tcp()
        return HttpResponse('success', "application/json")


class StartRtuService(APIView):

    def post(self, request):
        appsetting.startRtuService = True
        modbus_rtu()
        return HttpResponse('success', "application/json")


class StopRtuService(APIView):

    def post(self, request):
        appsetting.startRtuService = False
        modbus_rtu()
        return HttpResponse('success', "application/json")


class StartPpmpService(APIView):

    def post(self, request):
        appsetting.startPpmpService = True
        start_ppmp_post()
        return HttpResponse('success', "application/json")


class StopPpmpService(APIView):
    def post(self, request):
        appsetting.startPpmpService = False
        start_ppmp_post()
        return HttpResponse('success', "application/json")


class ConfigGatewayProperties(APIView):

    def post(self, request):
        data = request.body.decode("UTF-8")
        requestData = json.loads(data)
        jsonData: Edge = config.read_setting()

        edgeDeviceProperties = jsonData.edgedevice.properties.to_dict()
        for key in requestData:
            value = requestData[key]
            for objectKey in edgeDeviceProperties:
                # for device_key in properties:
                if objectKey == key:
                    edgeDeviceProperties[key] = value

        jsonData.edgedevice.properties = EdgeDeviceProperties.from_dict(edgeDeviceProperties)
        updated_json_data = jsonData.to_dict()
        print(updated_json_data)
        config.write_setting(updated_json_data)

        return HttpResponse('success', "application/json")


class ReadDeviceSettings(APIView):

    def get(self, request):
        jsonData: Edge = config.read_setting()
        jsonResponse = json.dumps(jsonData.to_dict(), indent=4)
        return HttpResponse(jsonResponse, "application/json")
