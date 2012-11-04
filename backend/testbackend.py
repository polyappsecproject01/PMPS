# To test, run backend.py in the background and this test program in the foreground.

import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)

print "Connecting to backend server (subscriber)..."
socket.connect ("tcp://localhost:1390")

out_stream = json.JSONEncoder().encode ( {
                 "method":"login",
                 "request": {
                     "username":"admin",
                     "password":"frootloops",
                     "ip_address":"192.168.007.010" } } )

socket.send (out_stream)

in_stream = socket.recv()
rep = json.loads(in_stream)
print json.dumps(rep, indent=4)
