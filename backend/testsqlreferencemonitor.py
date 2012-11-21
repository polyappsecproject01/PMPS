from sqlreferencemonitor import *
from hash_utilities import *

SessionID = AuthenticateUser('Anthony','awesomepassword')
# Debug/Intermediate Test code
#AddNewUser ('Jedi','admin', 'Theforce!', '630220da8305f483df95a36a39f368d3d96146a8bd703b32e123646b1922f3b7')
#print SessionID
#print RetrievePatientInfo('Ry982390810283an', 'Nol02389a01293n', SessionID['LoginHash'])
#AuthenticateUser('Der#####p','derpa2938902831i31092839082139081902839012839081290381')
#print AuthenticateUser('Antho!ny','awesomepassword')
print AddNewPatient('Hypochondriac', 'Herman', SessionID['LoginHash'])
print ModifyPatientName('Ryano', 'Nolan', 'Guy', 'Really!sick91', SessionID['LoginHash'])

''' 
Full Demo code below


# User Login (with admin permissions)
# Passwords are stored as hashes along with a unique salt in table users
# A Session ID (a login hash string) is returned on successful login
# All passwords are currently set to "awesomepassword"
# Failed attempts increment a lockout counter, and 5 failures result in a
# locked account for a given user
Session_ID1 = AuthenticateUser('Anthony', 'awesomepassword')
Session_ID2 = AuthenticateUser ('Doctorman', 'awesomepassword')
Session_ID3 = AuthenticateUser ('EMTdude', 'awesomepassword')
Session_IDFailed = AuthenticateUser ('Admin', 'awesomepassword') #fails
Session_IDFailed2 = AuthenticateUser ('Adminguy', 'terriblepassword') #fails

# The valid Session ID is used to make all calls below
# If the last request was made more than 15 minutes prior to the time
# of the current request, the request is denied due to expired session
# Permissions are verified and the request executed if allowed
# All functions work, but the below show examples of permission control

# Reads are allowed by all who are authenticated
print RetrievePatientInfo('Doe', 'John', Session_ID1['LoginHash'])
print RetrievePatientInfo('Doe', 'John', Session_ID2['LoginHash'])
print RetrievePatientInfo('Doe', 'John', Session_ID3['LoginHash'])
print RetrievePatientInfo('Doe', 'John', 12345) #Disallowed

# Only doctors and admins can add a new patient
print AddNewPatient('Skywalker', 'Luke', Session_ID1['LoginHash'])
print AddNewPatient('Skywalker', 'Leia', Session_ID2['LoginHash']) #Allowed
print AddNewPatient('Skywalker', 'Luke', Session_ID3['LoginHash']) #Disallowed
print AddNewPatient('Skywalker', 'Luke', 12345) #Disallowed

# Only admins can remove a patient
print RemovePatient('Skywalker', 'Luke', Session_ID3['LoginHash']) #Disallowed
print RemovePatient('Skywalker', 'Luke', Session_ID2['LoginHash']) #Disallowed
print RemovePatient('Skywalker', 'Leia', Session_ID1['LoginHash']) # Allowed

'''
