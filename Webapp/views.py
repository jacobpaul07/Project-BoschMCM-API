import datetime
import json
import time

from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseBadRequest
from App.Json_Class import index as config, Edge
from typing import Any, List, Optional, TypeVar, Type, cast, Callable

from App.Json_Class.EdgeDeviceProperties_dto import EdgeDeviceProperties
from App.PPMP.PPMP_Services import start_ppmp_post
from App.RTUReaders.modbus_rtu import modbus_rtu
from App.TCPReaders.modbus_tcp import modbus_tcp
from App.Websockets.AppSocket import AppSocket
import App.globalsettings as appsetting
import threading
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.
from Webapp.configHelper import ConfigComProperties, ConfigTcpProperties, ConfigComDevicesProperties,ConfigTCPDevicesProperties


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


class ConfigDataCenterProperties(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        requestData = json.loads(data)
        payLoadData = requestData["data"]
        deviceType: str = requestData["deviceType"]
        print("DeviceType:", deviceType)
        if deviceType == "COM1" or deviceType == "COM2":
            ConfigComProperties().updateComPortProperties(requestData=payLoadData, portName=deviceType)
        if deviceType == "TCP":
            ConfigTcpProperties().updateTcpPortProperties(requestData=payLoadData)

        return HttpResponse("Success", "application/json")


class ConfigDataCenterDeviceProperties(APIView):

    def post(self, request):
        data = request.body.decode("utf-8")
        requestData = json.loads(data)
        payLoadData = requestData["data"]
        deviceType: str = requestData["deviceType"]
        deviceName: str = requestData["deviceName"]
        print("DeviceType:", deviceType)
        if deviceType == "COM1" or deviceType == "COM2":
            response = ConfigComDevicesProperties().updateComDeviceProperties(payLoadData, deviceType, deviceName)
            if response == 'success':
                return HttpResponse(response, "application/json")
            else:
                return HttpResponseBadRequest(response)

        if deviceType == "TCP":
            response = ConfigTCPDevicesProperties().updateTCPDeviceProperties(payLoadData, deviceName)
            if response == 'success':
                return HttpResponse(response, "application/json")
            else:
                return HttpResponseBadRequest(response)


class ReadDeviceSettings(APIView):

    def get(self, request):
        jsonData: Edge = config.read_setting()
        jsonResponse = json.dumps(jsonData.to_dict(), indent=4)

        return HttpResponse(jsonResponse, "application/json")


class startWebSocket(APIView):

    def post(self, request):
        appsetting.runWebSocket = True
        # thread = threading.Thread(
        #     target=sendDataToWebSocket,
        #     args=())

        # Starting the Thread
        # thread.start()
        return HttpResponse('success', "application/json")


class stopWebSocket(APIView):

    def post(self, request):
        appsetting.runWebSocket = False

        return HttpResponse('success', "application/json")


def sendDataToWebSocket():
    while appsetting.runWebSocket:
        text_data = str(datetime.datetime.now())

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("notificationGroup", {
            "type": "chat_message",
            "message": text_data
        })
        time.sleep(10)
