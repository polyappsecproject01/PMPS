# CS9163 Application Security Group Project - Patient Medical Profile System (PMPS)
# Python Reference Monitor Between Frontend and SQL Database
# This module handles all requests from the frontend to the SQL DB 
# All requests are parsed and validated by individual character.
# All requests utilize the session ID to verify privledge level of the request being made.
# The code for this portion of the assignment was written by Anthony C. (acanda01) (10/2012).
# This code was tested successfully on Python 2.6.6, on the provided Linux VM at pmps.poly.edu.

'''
~~~~~~******SESSION VALIDATION******~~~~~~
This portion of the code will store each session id in an array that 
dictates the user level (emt, doctor, admin).  It must remove the session 
id after logout or timeout.
'''

# Module Imports
from dbinfo import *
from datetime import datetime, timedelta
import MySQLdb

# Initialize Database Connection
dbinfodata = getdbinfo() # Retrive db info from local file
PMPSDatabase = MySQLdb.connect(user=dbinfodata[0], passwd=dbinfodata[1], db=dbinfodata[2])

# Initialize Logs
ErrorLog = open("errorlog.log", 'a')
DebugLog = open("debuglog.log", 'a')
LoginLog = open("loginlog.log", 'a')

# Initialize Session ID Arrays (Login Hashes) on Startup
global ValidLogins
ValidLogins = [[' ',' ',' ',' ']]

# Definitions and Constants
TimeOutValue = timedelta(minutes=15) # Login timeout value
ValidUserLevels = ['EMT', 'Doctor', 'Admin'] # Define the Valid User Levels

# Temporary Variable Initialization
AlreadyLoggedIn = 1 # Used in AddValidatedSession
TimeSinceLastRequest = TimeOutValue # Used in Timeout Function

# Request a list of currently valid logins
def RequestValidLogins():
	print "Valid Login List:", ValidLogins # Trace
	return (ValidLogins)
	
# Updates the list of currently valid logins
def UpdateValidLogins(newValidLoginList):	
	ValidLogins = newValidLoginList
	
# Add Newly Validated Session IDs (Login Hashes)
def AddValidatedSession(UserName, UserLevel, LoginHash):
	# Check for both a valid user level and ensure no duplicate hashes
	# The Session ID/Login Hash is stored along with a login time for timeout use later on (if no request is made for 15 minutes straight, the sessionID will be removed and the user is effectively logged out, since the reference monitor will deny all requests from the corresponding Login Hash)
	
	# Temporary Variable Re-Initialization
	AlreadyLoggedIn = 0 # Assume the user is not logged in. 
	
	# Request current list of valid logins
	ValidLogins = RequestValidLogins()
	
	# Check if the user level passed to the function is valid.
	# Check if the user is already logged in to any of these levels (this 
	# is to prevent the case where authorized logins can flood the system
	# with repeated logins).
	# Trust that the user has been authenticated to the proper level 
	# before this function was called.
	# Additionally, no two identical hashes are allowed
	
	if (UserLevel in ValidUserLevels):
		for NameLevelHashTime in ValidLogins: # Check for already logged in user
			if (NameLevelHashTime[0] == UserName):
				AlreadyLoggedIn = 1
				print >> ErrorLog, 'Timestamp:',datetime.now(),'\n','User (',UserName,') Already Logged In.\n'
			if (NameLevelHashTime[2] == LoginHash): # Check for already used hash value / session ID
				AlreadyLoggedIn = 1
				print >> ErrorLog, 'Timestamp:',datetime.now(),'\n','User (',NameLevelHashTime[0],') is Already Using the Session ID Requested for User (',UserName,').\n'
		if (AlreadyLoggedIn==0): 
			print >> LoginLog, 'Timestamp:',datetime.now(),'\n',UserLevel, '(', UserName, ') successfully logged in.\n'
			ValidLogins+=[[UserName, UserLevel, LoginHash, datetime.now()]]
			UpdateValidLogins(ValidLogins)
	else:
		print >> ErrorLog, 'Timestamp:',datetime.now(),'\n','An Invalid User Level (',UserLevel,') was passed to the reference monitor for user',UserName,'.\n'
		
# Logout Function
# Removes the associated session ID / hash value from the relevant user privilege tuple
# The hash is checked so that old session IDs cannot be used with valid users
def LogoutSession(LogoutThisHashValue):
	ValidLogins = RequestValidLogins()
	for NameLevelHashTime in ValidLogins:
		if (NameLevelHashTime[2] == LogoutThisHashValue):
			ValidLogins.remove(NameLevelHashTime)
			print >> LoginLog, 'Timestamp:',datetime.now(),'\n',NameLevelHashTime[1], '(', NameLevelHashTime[0], ') logged out.\n'
			UpdateValidLogins(ValidLogins)
			return('User successfully logged out!', 1)
			
# Timeout Function
# Disallows the processing of requests from session IDs/ login hashes if the
# previous request was made more than 15 minutes prior.
# If the request is made within 15 minutes of the previous one, then the 
# session ID / login hash timestamp is refreshed.
# For EVERY database request made by a user, this function must be called.
def CheckForTimeout(LoginHash):
	ValidLogins = RequestValidLogins()
	for NameLevelHashTime in ValidLogins:
		if (NameLevelHashTime[2] == HashAssociateWithRequest):
			 TimeOfLastRequest = NameLevelHashTime[3]
			 CurrentTime = datetime.now()
			 TimeDifference = CurrentTime - TimeOfLastRequest 
			 if (TimeDifference > TimeoutValue):
				LogoutSession(LoginHash)
		
'''
~~~~~~******REQUEST VALIDATION******~~~~~~
This portion of the code will validate each request made to the SQL database, ensure that it is appropriate for the user's level, retrieve the information from the SQL database, and pass it back to the frontend.
'''
			
def AuthenticateUser(UserName, Password):

	return('0x12345', 1)

def RetrievePatientInfo(PatientLastName, PatientFirstName, LoginHash):

	# Connect to SQL DB and retrieve information
	DBPosition = PMPSDatabase.cursor() 
	DBPosition.execute("""SELECT * FROM medical_profiles WHERE firstname = "John" """)
	print DBPosition.fetchone()

	return('PatientFirstName', 'PatientLastName', 'PatientBloodType', 'PatientAllergies', 'PatientICELastName', 'PatientICEFirstName', 'PatientICEPhone', 'PatientPCPLastName', 'PatientPCPFirstName', 'PatientPCPPhone', 'PatientNotes', 1)

def AddNewPatient(PatientLastName, PatientFirstName, LoginHash):
	return('New Patient has been successfully added!', 1)

def RemovePatient(PatientLastName, PatientFirstName, LoginHash):
	return('Patient has been successfully removed!', 1)

def ModifyPatientName(PatientLastNameCurrent, PatientFirstNameCurrent, PatientLastNameNew, PatientFirstNameNew, LoginHash):
	return('Patient name has been successfully modified!', 1)	

def AppendPatientInfo(PatientLastName, PatientFirstName, PatientBloodType, PatientAllergies, PatientICELastName, PatientICEFirstName, PatientICEPhone, PatientPCPLastName, PatientPCPFirstName, PatientPCPPhone, PatientNotes, LoginHash):
	return('Patient information has been successfully appended!', 1)

def ModifyPatientInfo(PatientLastName, PatientFirstName, PatientBloodType, PatientAllergies, PatientICELastName, PatientICEFirstName, PatientICEPhone, PatientPCPLastName, PatientPCPFirstName, PatientPCPPhone, PatientNotes, LoginHash):
	return('Patient information has been successfully modified!', 1)
