#PORT COM4 -> SENDER
import socket
import espnow
import time
import json
from _thread import start_new_thread

################################# GLOBAL #################################
def get_sensor_value():
    analog_value = adc.read()
    response_data = {
        "analog_value": analog_value
    }
    return json.dumps(response_data)


############# 1. Servidor en ESP32 para lectura de datos #################

# @Description Initialize a server
def init_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    
    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            handle_client(conn)
        except Exception as e:
            print('Error:', e)
        

def handle_client(client):
    response = get_sensor_value()
    print("response:", response)
        
    client.send('HTTP/1.1 200 OK\r\n')
    client.send('Content-Type: application/json\r\n')
    client.send('Access-Control-Allow-Origin: *\r\n')
    client.send('Connection: close\r\n\r\n')
    client.sendall(response)
    client.close()
        
############# 2. Control de LED con ESPNOW #############################

# @descrption Add MAC addres from receiver.
# @return ESPNow environment object initializaded.
def init_p2p_network():
    e_now = espnow.ESPNow()
    e_now.active(True)
    return e_now

# @Description Send adc value to receiver peer
def send_peer(peer_mac, e):
    while True:
        # get analog value from sensor EMG AD8832
        sensor_value = adc.read()
        
        # send value to receiver peer as a message
        msg = str(sensor_value)
        e.send(peer_mac, msg)
        print('Sent value:', sensor_value)
        time.sleep(5)

################################### MAIN ##############################
def main():    
    e_now = init_p2p_network()
    peer_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF'
    e_now.add_peer(peer_mac)
    
    # Start server in a new thread so we can run p2p at same time.
    start_new_thread(send_peer, (peer_mac, e_now))
    # Star sending data to peer.
    init_server()
        
if __name__ == '__main__':
    main()