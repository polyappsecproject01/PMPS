from binascii import hexlify
import os

print
print "Use this to generate a random key of any length."
print

keylength = raw_input('Enter number of bytes for keylength: ')

the_key = os.urandom(int(keylength))

print 'key (hexified) = ' + hexlify(the_key)
