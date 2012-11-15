# To test, run backend.py in the background and this test program in the foreground.

import json
import zmq

def Test(request):
    out_stream = json.JSONEncoder().encode(request)
    socket.send (out_stream)

    in_stream = socket.recv()
    rep = json.loads(in_stream)
    print json.dumps(rep, indent=4)

# Main
context = zmq.Context()
socket = context.socket(zmq.REQ)

print "Connecting to backend server (subscriber)..."
socket.connect ("tcp://localhost:1390")

################################################################################
# Test login with invalid username/password.
Test( {
        "method":"login",
        "request": {
            "username":"admin",
            "password":"frootloops",
            "ip_address":"192.168.007.010" } } )

################################################################################
# Test login with valid username/password.
Test( {
        "method":"login",
        "request": {
            "username":"emt",
            "password":"password",
            "ip_address":"192.168.007.010" } } )

################################################################################
# Test getprofile for unknown patient.
login_hash = raw_input("Enter login_hash above to test getprofile: ")
Test( {
	"method":"getprofile",
	"auth_data":{
            "username":"emt",
            "ip_address":"192.168.007.010",
            "login_hash":login_hash
	},
        "request":{
            "firstname":"Mister",
            "lastname":"Unknown" } } )

################################################################################
# Test getprofile for valid patient.
login_hash = raw_input("Enter login_hash above to test getprofile: ")
Test( {
	"method":"getprofile",
	"auth_data":{
            "username":"emt",
            "ip_address":"192.168.007.010",
            "login_hash":login_hash
	},
        "request":{
            "firstname":"Nolan",
            "lastname":"Ryan" } } )
