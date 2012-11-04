import hashlib
import os

def GenRandomHash():
    return hashlib.sha256(os.urandom(32)).hexdigest()

def CalcHash(salt, pw):
    return hashlib.sha256(salt+pw).hexdigest()
