# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

# Complete project details at https://RandomNerdTutorials.com

try:
  import usocket as socket
except:
  import socket

import machine
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

# Initializa connection for Wi-Fi.
ssid = 'IZZI-74E0'
password = '748A0DEA74E0'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

# ADC pin config
adc_pin = machine.Pin(34)
adc = machine.ADC(adc_pin)
adc.atten(machine.ADC.ATTN_11DB)
