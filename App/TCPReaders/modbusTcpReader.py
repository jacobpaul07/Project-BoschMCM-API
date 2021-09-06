import threading
from pyModbusTCP.client import ModbusClient

from App.GeneralUtilities import timestamp
from App.Json_Class.TCPProperties_dto import TCPProperties
from App.Json_Class.TCPdevice_dto import TCPdevice
from datetime import datetime


def ReadTCPSingleTag(TCPMessurementTags: object, finalData: []):
    result: object = {}
    tcpDeviceEnabled: bool = bool(str(TCPMessurementTags["Enabled"]))
    SERVER_HOST: str = TCPMessurementTags["IP"]
    SERVER_PORT: int = int(str(TCPMessurementTags["PORT"]))
    TimeOutms: int = int(str(TCPMessurementTags["TimeOutms"]))
    tagName: str = TCPMessurementTags["tagName"]
    tagAddress: int = int(str(TCPMessurementTags["tagAddress"]))

    if tcpDeviceEnabled:
        c = ModbusClient()
        c.host(SERVER_HOST)
        c.port(SERVER_PORT)
        scan_timeout = TimeOutms / 1000
        c.timeout(scan_timeout)

        if not c.is_open():
            if not c.open():
                print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

        try:
            if c.is_open():
                # read 8 registers at address 0, store result in regs list
                mulvalue = float(10 / 65535)

                registerValue = c.read_input_registers(tagAddress, 1)
                result = {
                    "tagName": tagName,
                    "value": round(registerValue[0] * mulvalue, 3)

                }

            for idx, currentObject in enumerate(finalData):
                if currentObject["tagName"] == tagName:
                    finalData[idx] = result
                    break
        except:
            print("Device is not Connected")

    return result


def ReadTCP(SERVER_HOST, SERVER_PORT, tcpDevices: TCPdevice, tcpProperties: TCPProperties, threadsCount, callback):
    success = True
    datasList = []
    if tcpDevices.properties.Enable == "true":
        c = ModbusClient()
        # uncomment this line to see debug message
        # c.debug(True)
        # define modbus server host, port
        c.host(SERVER_HOST)
        c.port(SERVER_PORT)

        scan_timeout = int(tcpProperties.TimeOutms) / 1000
        c.timeout(scan_timeout)

        # open or reconnect TCP to server
        if not c.is_open():
            if not c.open():
                print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
                success = False
        # if open() is ok, read register
        try:
            if c.is_open():
                # read 8 registers at address 0, store result in regs list
                for tags in tcpDevices.IOTags:
                    registerValue = c.read_input_registers(int(tags.Address), 1)
                    inputValue = float(registerValue[0])
                    spanHigh = float(tags.SpanHigh)
                    spanLow = float(tags.SpanLow)
                    unitHigh = float(tags.UnitHigh)
                    unitLow = float(tags.UnitLow)

                    # Applying Formula
                    regDiff = (inputValue - spanLow)
                    spanDiff = (spanHigh - spanLow)
                    unitDiff = (unitHigh - unitLow)
                    diffCal = (regDiff / spanDiff) * unitDiff
                    finalCal = unitLow + diffCal
                    timestamp = datetime.now().strftime("%Y-%m-%dT%I:%M:%S_%p")
                    deviceID = tcpDevices.properties.Name
                    data = {
                        "deviceID": deviceID,
                        "channel": "TCP",
                        "tagName": tags.Name,
                        "value": round(finalCal, 3),
                        "timestamp": timestamp
                    }
                    datasList.append(data)

                # if success display registers
                if datasList:
                    print(tcpDevices.properties.Name + str(datasList))
        except:
            success = False
            print("Device is not Connected")

        thread = threading.Thread(
            target=callback,
            args=(SERVER_HOST, SERVER_PORT, tcpDevices, tcpProperties, threadsCount, datasList, success)
        )
        thread.start()
    return datasList
