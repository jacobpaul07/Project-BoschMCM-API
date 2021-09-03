import threading
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from App.GeneralUtilities import timestamp
from App.Json_Class.COMProperties_dto import COMPORTProperties
from App.Json_Class.COMDevices_dto import *
from App.Json_Class.SerialPortSetting_dto import SerialPortSettings
from datetime import datetime

def ReadRTU(settings: SerialPortSettings, ComDevices: COMdevice,comProperties:COMPORTProperties,threadsCount, callback,com):
    success = True
    datasList = []

    if ComDevices.properties.Enable == "True":
        c = ModbusClient(method=settings.Method, port=settings.Port, timeout=int(settings.Timeout), stopbits=int(settings.StopBit), bytesize=int(settings.DataBit), parity=settings.Parity,
                         baudrate=int(settings.BaudRate))

        # open or reconnect TCP to server
        if not c.connect():
            print("unable to connect to", settings.Port)
        # if open() is ok, read register
        try:
            if c.connect():
                # read 8 registers at address 0, store result in regs list

                for tags in ComDevices.IOTags:
                    register_data = c.read_input_registers(address=int(tags.Address),
                                                           count=1,
                                                           unit=int(ComDevices.properties.UnitNumber))
                    registerValue = register_data.registers
                    timestamp = datetime.now().strftime("%Y-%m-%dT%I:%M:%S_%p")

                    data = {
                        "deviceID": ComDevices.properties.Name,
                        "channel": com,
                        "tagName": tags.Name,
                        "value": registerValue[0] / 10,
                        "timestamp": timestamp
                    }
                    datasList.append(data)

                c.close()
        except:
            success = False
            print("Device is not Connected")

        thread = threading.Thread(
            target=callback,
            args=(settings, ComDevices,comProperties, threadsCount, datasList, success,com)
        )
        thread.start()

    return datasList