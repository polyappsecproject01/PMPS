import hashlib
import os

def GenRandomHash():
    return os.urandom(32).encode("hex")

def CalcHash(salt, pw):
    return hashlib.sha256(salt+pw).hexdigest()
