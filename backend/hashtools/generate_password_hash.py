import getpass
import hashlib
import os

print
print "Use this to generate the salt and hash. Copy/paste to the 'users' database."
print

while True:
    pw1 = getpass.getpass('Choose your password  : ')
    pw2 = getpass.getpass('Type again to confirm : ')
    if pw1 == pw2:
        break
    else:
        print 'No match, try again.'

salt = os.urandom(32).encode("hex")

password_hash = hashlib.sha256(salt+pw1)

print 'salt = ' + salt
print 'hash = ' + password_hash.hexdigest()
