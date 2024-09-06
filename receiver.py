#PORT COM5 -> RECEIVER

import network
import espnow
import ubinascii
import time
from machine import Pin

############# 2. Control de LED con ESPNOW #############################

# Board integrated LED pinout.
board_led = Pin(2, Pin.OUT)

# @descrption Add MAC addres from receiver.
# @return ESPNow environment object initializaded.
def init_p2p_network():
    e_now = espnow.ESPNow()
    e_now.active(True)
    return e_now

# @descrption Initializa connection for Wi-Fi.
def init_wifi_connection():
    SSID = 'IZZI-74E0'
    PASSWORD = '748A0DEA74E0'
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        time.sleep(1)

    print('IP:', wlan.ifconfig()[0])
    
# @description Turn on or off depengin on signal parameter.
def handle_signal_to_led(signal):
    turn_on = 1
    turn_off = 0
    
    led_state = turn_on if signal > 638 else turn_off
    
    board_led.value(led_state)

# @description Print sender event info.
def handle_p2p_receive(mac, msg):
    print('Received from', ubinascii.hexlify(mac), ':', int(msg))


################################### MAIN ##############################
def main():
    init_wifi_connection()
    e = init_p2p_network()
    
    while True:
        mac, msg = e.recv()
        
        handle_p2p_receive(mac, msg)
        handle_signal_to_led(int(msg))
        
        time.sleep(1)
        
if __name__ == '__main__':
    main()