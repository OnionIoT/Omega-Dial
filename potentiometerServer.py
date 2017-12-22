import os, sys, getopt, json
import paho.mqtt.client as mqtt
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer

position = 0

class PotentiometerHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        if self.path == '/position':
                print "GET request: returning position %d"%(position)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                response = {"position":position}
                self.wfile.write(json.dumps(response))
                return

        elif self.path == '/':
                f = open('index.html')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

        elif self.path.endswith('.js'):
                f = open(self.path[1:])
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
              
def __main__():

    #Setup MQTT
    mqttc = mqtt.Client()

    ## Define the MQTT Callbacks
    # The callback for when the client receives a response from the Server
    def on_connect(client, userdata, flags, rc):
        #print("Connected with result code "+str(rc))
        mqttc.subscribe("potentiometerPosition")

    # Subscribe to the MQTT Topic
    def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
        # The callback when a publish message is received from the Server
    def on_message(client, userdata, msg):
        if msg.payload:
            global position
            position = int(msg.payload)

    # The callback to disconnect and update the user
    def on_disconnect(client, userdata, rc):
        print("Disconnect From Server")

    #Assign the callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.on_disconnect = on_disconnect
    #Connects directly to the Omega
    mqttc.connect('127.0.0.1', 1883)

    # start the mqtt network loop (in the background through threading)
    mqttc.loop_start()


    print "This will accept GET requests and respond with the potentiometer position"
    PORT = 8080
    server = SocketServer.TCPServer(('', PORT), PotentiometerHTTPHandler)

    print "Serving at port", PORT, "."
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    mqttc.loop_stop()
    print "HTTP server is closed"


if __name__ == '__main__':
    __main__()
