# Project-BoschMCM-API

Run python manage.py runserver

### API POST commands:
  1. To change IP and Port

    API: $ curl --data "{"ip" : "192.168.1.40","port" : "502","deviceName" : "TCPdevice01"}" http://127.0.0.1:8000/api/changetcpip
  2. To START ModbusTCP

    API: $ curl --data "" http://127.0.0.1:8000/api/starttcp
  3. To STOP ModbusTCP

    API: $ curl --data "" http://127.0.0.1:8000/api/stoptcp
  4. To START PPMP Service

    API: $ curl --data "" http://127.0.0.1:8000/api/startppmp
  5. To STOP PPMP Service

    API: $ curl --data "" http://127.0.0.1:8000/api/stopppmp
  6. To START ModbusRTU

    API: $ curl --data "" http://127.0.0.1:8000/api/startrtu
  7. To STOP ModbusRTU

    API: $ curl --data "" http://127.0.0.1:8000/api/stoprtu
  8. To change the EdgeGateway Properties
     
    API: http://localhost:8000/api/changeDataCenterProperties
    BODY:
    {
    "Name": "Edge Device",
    "Mode1": "UNO-2271 Linux",
    "Password": "123456",
    "Identity": "S3-0001",
    "IP Address": "192.168.1.15",
    "Time Zone": "+05:30",
    "Description": "Siqsess Edge gateway Integrate with Bosch Nexeed Platform "
    }

  9. To Change the DataCenter-Port Properties

    API: http://localhost:8000/api/changeDataCenterProperties
    BODY:
    {
    "mode": "update",
    "deviceType": "COM2",
    "data": {
        "Enable": "False",
        "Type": "Serial",
        "Name": "Selec Twix 2",
        "Description": "Built in Serial port RS232/rs422/rs485",
        "Scan Time(ms)": "11000",
        "Time Out(ms)": "13000",
        "Retry Count": "13",
        "Auto Recover Time(s)": "10",
        "SerialPort Setting": {
            "Method": "rtu",
            "Port": "COM",
            "Baud Rate": "9600",
            "Data Bit": "8",
            "Stop Bit": "11",
            "Timeout": "1",
            "Parity": "N",
            "RTS": "False",
            "DTR": "False"
            }
        }
    }
  10. To Change DataCenter-Device Properties

    API: http://localhost:8000/api/changeDataCenterDeviceProperties
    BODY:
    {
    "mode": "update",
    "deviceType": "COM2",
    "deviceName":"COM2-Device-02",
    "data": {
        "Enable": "True",
        "Name": "COM2-Device-02",
        "Device Type": "Modbus RTU",
        "Device Model": "ADAM",
        "Unit Number": "2",
        "Description": "Slave 1",
        "Add device name as prefix to IO Tag": "Enable",
        "Extention Properties": {
            "CheckSum": "Enable",
            "Protocol": "Modbus",
            "ModbusDigital block size": "16",
            "Modbus Analog block Size": "16"
        }
      }
    }

  11. To change DataCenter-Device IOTags  (Sensor Properties)
     
    API: http://localhost:8000/api/changeDataCenterDeviceIOTags
    BODY:
    {
    "mode": "update",
    "deviceType": "COM2",
    "deviceName":"COM2-Device-01",
    "data": [
            {
                "Name": "Temperature",
                "Signal Type": "AI Signal",
                "Conversion": "IEEE Float Point",
                "Address": "6",
                "Span High": "1000",
                "Span Low": "0",
                "Unit High": "0",
                "Unit Low": "10",
                "Initial Value": "0.0",
                "Scan Rate": "1",
                "Read Write": "Read Only",
                "initvalue": "10",
                "Description": "Temperature Sensor"
            },
            {
                "Name": "Pressure",
                "Signal Type": "AI",
                "Conversion": "IEEE Float Point",
                "Address": "1",
                "Span High": "65535",
                "Span Low": "0",
                "Unit High": "10",
                "Unit Low": "0",
                "Initial Value": "0.0",
                "Scan Rate": "1",
                "Read Write": "Read Only",
                "initvalue": "10",
                "Description": "Level 1"
            },
            {
                "Name": "Flow",
                "Signal Type": "AI ",
                "Conversion": "IEEE Float Point",
                "Address": "2",
                "Span High": "65535",
                "Span Low": "0",
                "Unit High": "10",
                "Unit Low": "0",
                "Initial Value": "0.0",
                "Scan Rate": "1",
                "Read Write": "Read Only",
                "initvalue": "10",
                "Description": "Flow 2"
            }
        ]
    }
  12. To Start WebSocket 
  
    API: $ curl --data "" http://127.0.0.1:8000/api/startWebSocket
    
  13. To Stop WebSocket 

    API: $ curl --data "" http://127.0.0.1:8000/api/stopWebSocket

### To Activate Redis 5
    docker run -p 6379:6379 -d redis:5
### API Data format:

    {
        "ip" : "192.168.1.40",
        "port" : "502",
        "deviceName" : "TCPdevice01" 
    }

### Docker Image:
  
    docker pull siqsessjacob/boschmcm_api

### Docker Run:

    docker run -t -p 8000:8000 siqsessjacob/boschmcm_api

### Docker container ls:

    Format:
    docker exec -it (CONTAINER ID) /bin/bash  
    Example:
    docker exec -it c2c727b2624e /bin/bash
