# Project-BoschMCM-API

Run python manage.py runserver 

API POST commands:
  1. To change IP and Port
    $ curl --data "{"ip" : "192.168.1.40","port" : "502","deviceName" : "TCPdevice01"}" http://127.0.0.1:8000/api/changetcpip
  2. To START ModbusTCP
    $ curl --data "" http://127.0.0.1:8000/api/starttcp
  3. To STOP ModbusTCP
    $ curl --data "" http://127.0.0.1:8000/api/stoptcp
  4. To START PPMP Service
    $ curl --data "" http://127.0.0.1:8000/api/startppmp
  5. To STOP PPMP Service
    $ curl --data "" http://127.0.0.1:8000/api/stopppmp
    
    
API Data format:
 {
    "ip" : "192.168.1.40",
    "port" : "502",
    "deviceName" : "TCPdevice01" 
}


Docker container ls:
  Format:
  docker exec -it (CONTAINER ID) /bin/bash  
  Example:
  docker exec -it c2c727b2624e /bin/bash
