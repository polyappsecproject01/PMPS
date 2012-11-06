import getpass
import hashlib
import os

print
print "Use this to authenticate a salt/pw pair."
print

while True:
    password_hash = raw_input('Enter expected password_hash: ')
    salt = raw_input('Enter salt: ')
    pw = getpass.getpass('Enter password: ')

    if password_hash == hashlib.sha256(salt+pw).hexdigest():
        print 'Authenticated!'
        break
    else:
        print 'No match, try again.'
