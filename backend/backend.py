import json
import os
import sqlreferencemonitor as refmon
import time
import zmq

def LoginUser(request):
    login_hash = refmon.AuthenticateUser(request)
    authenticated = login_hash != 0
    return {"authenticated":authenticated,"login_hash":login_hash}

def GetProfile(request):
    return refmon.RetrievePatientInfo(login_hash,request)

def UpdateProfile(login_hash,request):
    updated = refmon.ModifyPatientInfo(login_hash,request) or refmon.AppendPatientInfo(login_hash.request)
    return {"updated":updated}

def LogoutUser(login_hash):
    logged_out = refmon.LogoutSession(login_hash)
    return {"logged_out":logged_out}
    
# Main
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:1390")

while True:
    in_stream = socket.recv()

    req = json.loads(in_stream)

    # Debug (remove later)
    print
    print json.dumps(msg, indent=4)
    print

    method = req["method"]

    if method == "login":
        response = LoginUser(req["request"])
    elif method == "getprofile":
        response = GetProfile(req["login_hash"],req["request"])
    elif method == "updateprofile":
        response = UpdateProfile(req["login_hash"],req["request"])
    elif method == "logout":
        response = LogoutUser(req["login_hash"])

    rep = {"method":method,"response":response}
    out_stream = json.JSONEncoder().encode(rep)
    socket.send(out_stream)
