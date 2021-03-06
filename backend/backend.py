from binascii import unhexlify as unhex
from config import shared_key
from pyDes import *
import json
import os
import socket
import sqlreferencemonitor as refmon
import time
# import zmq

def AddNewUser (auth_data,request):
    result = refmon.AddNewUser(request["username"],request["accesslevel"],request["password"],auth_data["login_hash"])
    return {"added":result["SuccessfulQuery"]}

def CreateProfile (auth_data,request):
    result = refmon.AddNewPatient(request["lastname"],request["firstname"],auth_data["login_hash"])

    if result["SuccessfulQuery"]:
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

    return {"created":result["SuccessfulQuery"]}

def GetProfile (auth_data,request):
    profile = refmon.RetrievePatientInfo(request["lastname"],request["firstname"],auth_data["login_hash"])

    if profile["SuccessfulQuery"]:
        result = dict(
                     retrieved = profile["SuccessfulQuery"],
                     firstname = profile["PatientFirstName"],
                     lastname  = profile["PatientLastName"],
                     bloodtype = profile["PatientBloodType"],
                     allergies = profile["PatientAllergies"],
                     ICEcontact = dict(
                                      firstname = profile["PatientICEFirstName"],
                                      lastname  = profile["PatientICELastName"],
                                      phone     = profile["PatientICEPhone"]),
                     PCP = dict(
                               firstname = profile["PatientPCPFirstName"],
                               lastname  = profile["PatientPCPLastName"],
                               phone     = profile["PatientPCPPhone"]),
                     notes = profile["PatientNotes"])
    else:
        result = dict(retrieved=profile["SuccessfulQuery"])

    return result

def LoginUser (request):
    result = refmon.AuthenticateUser(request["username"],request["password"])

    if result["SuccessfulQuery"]:
        login_hash  = result["LoginHash"]
        accesslevel = result["accesslevel"]
    else:
        login_hash  = 0
        accesslevel = "readonly"

    return {"authenticated":result["SuccessfulQuery"],"login_hash":login_hash,"accesslevel":accesslevel}

def LogoutUser (auth_data):
    result = refmon.LogoutSession(auth_data["login_hash"])
    return {"logged_out":result["SuccessfulQuery"]}

def ModifyPatientName (auth_data,request):
    result = refmon.ModifyPatientName(
                 request["lastname"],
                 request["firstname"],
                 request["newlastname"],
                 request["newfirstname"],
                 auth_data["login_hash"])
    return {"modified":result["SuccessfulQuery"]}
    
def RemoveProfile (auth_data,request):
    result = refmon.RemovePatient(request["lastname"],request["firstname"],auth_data["login_hash"])
    return {"removed":result["SuccessfulQuery"]}

def UpdateProfile (auth_data,request):
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

    return {"updated":result["SuccessfulQuery"]}

def TDES_Decrypt (the_stream):
    tdes = triple_des(unhex(shared_key))
    return tdes.decrypt(the_stream,pad="\0")

def TDES_Encrypt (the_stream):
    tdes = triple_des(unhex(shared_key))
    return tdes.encrypt(the_stream,pad="\0")

# Main

HOST = ''
PORT = 1390

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))

while True:
    s.listen(1)
    print "Listening..."

    conn, addr = s.accept()
    print 'Connected by', addr

    previous_timeout = conn.gettimeout()
    conn.settimeout(5.0)
    in_stream = conn.recv(1024)
    conn.settimeout(previous_timeout)

    decrypted_instream = TDES_Decrypt(in_stream)

    try:
        req = json.loads(decrypted_instream)
    except ValueError:
        req = {"method":"error"}

    #--DEBUG
    print "Received:"
    print json.dumps(req, indent=4)
    print

    method = req["method"]

    if method == "createprofile":
        response = CreateProfile(req["auth_data"],req["request"])
    elif method == "getprofile":
        response = GetProfile(req["auth_data"],req["request"])
    elif method == "login":
        response = LoginUser(req["request"])
    elif method == "logout":
        response = LogoutUser(req["auth_data"])
    elif method == "modifypatientname":
        response = ModifyPatientName(req["auth_data"],req["request"])
    elif method == "removeprofile":
        response = RemoveProfile(req["auth_data"],req["request"])
    elif method == "updateprofile":
        response = UpdateProfile(req["auth_data"],req["request"])
    else:
        response = {}

    rep = {"method":method,"response":response}

    #--DEBUG
    print "Sending:"
    print json.dumps(rep, indent=4)

    out_stream = json.JSONEncoder().encode(rep)

    encrypted_outstream = TDES_Encrypt(out_stream)

    conn.sendall(encrypted_outstream)
    conn.close()
