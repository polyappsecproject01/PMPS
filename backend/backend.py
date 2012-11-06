import json
import os
import sqlreferencemonitor as refmon
import time
import zmq

def LoginUser(request):
    login_hash, authenticated = refmon.AuthenticateUser(request["username"],request["password"],request["ip_address"])
    return {"authenticated":authenticated,"login_hash":login_hash}

def GetProfile(auth_data,request):
    
    profile = refmon.RetrievePatientInfo(request["lastname"],request["firstname"],auth_data["login_hash"])
    response = dict (
                   retrieved = profile["SuccessfulQuery"],
                   firstname = profile["PatientFirstName"],
                   lastname  = profile["PatientLastName"],
                   bloodtype = profile["PatientBloodType"],
                   allergies = profile["PatientAllergies"],
                   ICEcontact = dict (
                                    firstname = profile["PatientICEFirstName"],
                                    lastname  = profile["PatientICELastName"],
                                    phone     = profile["PatientICEPhone"] ),
                   PCP = dict (
                             firstname = profile["PatientPCPFirstName"],
                             lastname  = profile["PatientPCPLastName"],
                             phone     = profile["PatientPCPPhone"] ),
                   notes = profile["PatientNotes"] )

    return response

def UpdateProfile(auth_data,request):
    result = refmon.ModifyPatientInfo(
                 request["lastname"],
                 request["firstname"],
                 request["bloodtype"],
                 request["allergies"],
                 request["ICEcontact"]["lastname"],
                 request["ICEcontact"]["firstname"],
                 request["ICEcontact"]["phone"],
                 request["PCP"]["lastname"],
                 request["PCP"]["firstname"],
                 request["PCP"]["phone"],
                 request["notes"],
                 auth_data["login_hash"])

    if not result["SuccessfulQuery"]:
        result = refmon.AppendPatientInfo(
                     request["lastname"],
                     request["firstname"],
                     request["bloodtype"],
                     request["allergies"],
                     request["ICEcontact"]["lastname"],
                     request["ICEcontact"]["firstname"],
                     request["ICEcontact"]["phone"],
                     request["PCP"]["lastname"],
                     request["PCP"]["firstname"],
                     request["PCP"]["phone"],
                     request["notes"],
                     auth_data["login_hash"])

    return {"updated":result["SuccessfulQuery"]}

def LogoutUser(auth_data):
    result = refmon.LogoutSession(auth_data["login_hash"])
    return {"logged_out":result[1]}
    
# Main
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:1390")

while True:
    in_stream = socket.recv()

    req = json.loads(in_stream)

    # Debug (remove later)
    print
    print json.dumps(req, indent=4)
    print

    method = req["method"]

    if method == "login":
        response = LoginUser(req["request"])
    elif method == "getprofile":
        response = GetProfile(req["auth_data"],req["request"])
    elif method == "updateprofile":
        response = UpdateProfile(req["auth_data"],req["request"])
    elif method == "logout":
        response = LogoutUser(req["auth_data"])

    rep = {"method":method,"response":response}
    out_stream = json.JSONEncoder().encode(rep)
    socket.send(out_stream)
