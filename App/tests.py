from django.test import TestCase

# Create your tests here.


from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

client = ModbusClient(method='rtu', port='COM5', timeout=1, stopbits=1, bytesize=8, parity='N', baudrate=9600)
client.connect()

tempc = client.read_input_registers(address=8, count=1, unit=2)
tc = tempc.registers[0] / 10
print(tc)
tempd = client.read_input_registers(address=0, count=12, unit=2)
print(tempd.registers)
reg = client.read_holding_registers(address=0, count=24, unit=2)
aa = reg.registers
client.write_register(address=23, value=0, unit=2)
print(aa)
reg = client.read_holding_registers(address=0, count=24, unit=2)
regd = client.read_coils(address=0, count=1, unit=2)
regdw = client.write_coil(address=0, value=0, unit=2)
aa = reg.registers
print(aa)
