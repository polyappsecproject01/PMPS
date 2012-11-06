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
import datetime
import hash_utilities
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
ValidLogins = [[' ', ' ', ' ', ' ']] # Consists of Username, User Level, Login Hash and Last Access Timestamp

# Definitions and Constants
global TimeOutValue
TimeOutValue = datetime.timedelta(minutes=15) # Login timeout value
global ValidUserLevels
ValidUserLevels = ['EMT', 'Doctor', 'Admin'] # Define the Valid User Levels
global LoggedOutHash 
LoggedOutHash = '0'*64 # If the user is logged out the hash will read all zeros


# Temporary Variable Initialization
AlreadyLoggedIn = 1 # Used in AddValidatedSession

# Timeout Function
# Disallows the processing of requests from session IDs/ login hashes if the
# previous request was made more than 15 minutes prior.
# If the request is made within 15 minutes of the previous one, then the 
# session ID / login hash timestamp is refreshed.
# For EVERY database request made by a user, this function must be called.
def CheckForTimeoutAll():
	# Retrieve a tuple consisting of all logged in users (non-zero hashes) and their last access time (time of last request)
	DBPosition = PMPSDatabase.cursor()
	DBPosition.execute("""SELECT username, login_hash, last_access FROM users WHERE login_hash <> %s""", (LoggedOutHash))
	UserHashLastAccessTuple = DBPosition.fetchall()	
	print UserHashLastAccessTuple
	for UserHashTime in UserHashLastAccessTuple:
		TimeOfLastRequest = datetime.datetime.strptime(UserHashTime[2], '%Y-%m-%d %H:%M:%S')
		print TimeOfLastRequest
		CurrentTime = datetime.datetime.now()
		TimeDifference = CurrentTime - TimeOfLastRequest
		if (TimeDifference > TimeOutValue):
			LogoutSession(UserHashTime[1])

# Request a list of currently valid logins
def RequestValidLogins():
	# Check to ensure that the corresponding sessions are not timed out
	# If it is, the function will set the hash to zero (log the user out)
	CheckForTimeoutAll()
	# Query the database and form a list of all logins with active sessions
	DBPosition = PMPSDatabase.cursor()
	DBPosition.execute("""SELECT * FROM users WHERE login_hash <> %s""", (LoggedOutHash))
	AllActiveLogins = DBPosition.fetchall()
	print "Valid Login List:", AllActiveLogins # Trace
	return (ValidLogins)

# Update the timestamp (last_access) for a given login hash (session ID)
def UpdateTimestamp (LoginHash):
	NewTimestamp = datetime.datetime.now()
	DBPosition = PMPSDatabase.cursor()
	DBPosition.execute("""UPDATE users SET last_access = %s WHERE login_hash = %s""", (NewTimestamp, LoginHash))
		
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
				print >> ErrorLog, 'Timestamp:',datetime.datetime.now(),'\n','User (',UserName,') Already Logged In.\n'
			if (NameLevelHashTime[2] == LoginHash): # Check for already used hash value / session ID
				AlreadyLoggedIn = 1
				print >> ErrorLog, 'Timestamp:',datetime.datetime.now(),'\n','User (',NameLevelHashTime[0],') is Already Using the Session ID Requested for User (',UserName,').\n'
		if (AlreadyLoggedIn==0): 
			print >> LoginLog, 'Timestamp:',datetime.datetime.now(),'\n',UserLevel, '(', UserName, ') successfully logged in.\n'
			ValidLogins+=[[UserName, UserLevel, LoginHash, datetime.datetime.now()]]
			UpdateValidLogins(ValidLogins)
	else:
		print >> ErrorLog, 'Timestamp:',datetime.datetime.now(),'\n','An Invalid User Level (',UserLevel,') was passed to the reference monitor for user',UserName,'.\n'
		
# Logout Function
# Removes the associated session ID / hash value from the relevant user privilege tuple
# The hash is checked so that old session IDs cannot be used with valid users
def LogoutSession(LogoutThisHashValue):
	# Set the requested hash value to LoggedOutHash = '0'*64 to indicate that the user is logged out
	DBPosition = PMPSDatabase.cursor()
	DBPosition.execute("""UPDATE users SET login_hash = %s WHERE login_hash = %s""", (LoggedOutHash, LogoutThisHashValue))
	ReturnDict = dict(StatusMessage = 'User has been successfully logged out!', SuccessfulQuery = 1)
	return(ReturnDict)
			

'''
~~~~~~******REQUEST VALIDATION******~~~~~~
This portion of the code will validate each request made to the SQL database, ensure that it is appropriate for the user's level, retrieve the information from the SQL database, and pass it back to the frontend.
'''

def AuthenticateUser(UserName, Password, IP_Address):
        #missing: Validate UserName.

        # Connect to SQL DB and Retrieve Information
        DBPosition = PMPSDatabase.cursor()
        DBPosition.execute("""SELECT password_salt, password_hash FROM users WHERE username = %s""", (UserName,))

        row = DBPosition.fetchone()
        if row == None:
                return ("",0)

        salt, expected_hash = row

        this_hash = hash_utilities.CalcHash(salt, Password)

        if this_hash == expected_hash:
                login_hash = hash_utilities.GenRandomHash()

                DBPosition.execute("""UPDATE users SET login_hash = %s, ip_address = %s WHERE username = %s""",
                                   (login_hash, IP_Address, UserName))

                return (login_hash,1)
        else:
                return("",0)

def RetrievePatientInfo(PatientLastName, PatientFirstName, LoginHash):
	# Ensure the LoginHash is valid and has the proper permissions associated 
        # with it (all authenticated users may use this function)
        
	#DBPosition = PMPSDatabase.cursor()
        #DBPosition.execute("""SELECT * FROM users WHERE login_hash = %s""", (LoginHash))
        #QueryResult = DBPosition.fetchone()
	
#	if (UserLevel in ValidUserLevels):
 #               for NameLevelHashTime in ValidLogins: # Check for already logged in user
  #                      if (NameLevelHashTime[0] == UserName):
   #                             AlreadyLoggedIn = 1
    #                            print >> ErrorLog, 'Timestamp:',datetime.datetime.now(),'\n','User (',UserName,') Already Logged In.\n'
     #                   if (NameLevelHashTime[2] == LoginHash): # Check for already used hash value / session ID
      #                          AlreadyLoggedIn = 1
       #                         print >> ErrorLog, 'Timestamp:',datetime.datetime.now(),'\n','User (',NameLevelHashTime[0],') is Already Using the Session

	# Connect to SQL DB and Retrieve Information
	DBPosition = PMPSDatabase.cursor() 
	DBPosition.execute("""SELECT * FROM medical_profiles WHERE lastname = %s AND firstname = %s""", (PatientLastName, PatientFirstName))
	QueryResult = DBPosition.fetchone()
	# Store the result as a dict for return
	ReturnDict = dict(PatientLastName = QueryResult[2], PatientFirstName = QueryResult[1], PatientBloodType = QueryResult[3], PatientAllergies = QueryResult[4], PatientICELastName = QueryResult[6], PatientICEFirstName = QueryResult[5], PatientICEPhone = QueryResult[7], PatientPCPLastName = QueryResult[9], PatientPCPFirstName = QueryResult[8], PatientPCPPhone = QueryResult[10], PatientNotes = QueryResult[11], SuccessfulQuery = 1)
	return(ReturnDict)

def AddNewPatient(PatientLastName, PatientFirstName, LoginHash):
	
	# Connect to the SQL DB and Add New Patient
	DBPosition = PMPSDatabase.cursor() 
	DBPosition.execute("""INSERT INTO medical_profiles (lastname, firstname) VALUES (%s, %s)""", (PatientLastName, PatientFirstName))
	# Keep track of query in the debug log
	print >> DebugLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewPatient','\n'
	# Store the result as a dict for return
	ReturnDict = dict(StatusMessage = 'New patient has been successfully added!', SuccessfulQuery = 1)
	return(ReturnDict)

def RemovePatient(PatientLastName, PatientFirstName, LoginHash):
	
	# Connect to the SQL DB and Remove Patient
	DBPosition = PMPSDatabase.cursor() 
	DBPosition.execute("""DELETE FROM medical_profiles WHERE lastname = %s AND firstname = %s""", (PatientLastName, PatientFirstName))
	# Keep track of query in the debug log
	print >> DebugLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RemovePatient','\n'
	# Store the result as a dict for return
	ReturnDict = dict(StatusMessage = 'Patient has been successfully removed!', SuccessfulQuery = 1)
	return(ReturnDict)

def ModifyPatientName(PatientLastNameCurrent, PatientFirstNameCurrent, PatientLastNameNew, PatientFirstNameNew, LoginHash):
	
	# Connect to the SQL DB and Modify Patient Name
	DBPosition = PMPSDatabase.cursor() 
	DBPosition.execute("""UPDATE medical_profiles SET lastname = %s, firstname = %s WHERE lastname = %s AND firstname = %s""", (PatientLastNameNew, PatientFirstNameNew, PatientLastNameCurrent, PatientFirstNameCurrent))
	# Keep track of query in the debug log
	print >> DebugLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientName','\n'
	# Store the result as a dict for return
	ReturnDict = dict(StatusMessage = 'Patient name has been successfully updated!', SuccessfulQuery = 1)
	return(ReturnDict)

def AppendPatientInfo(PatientLastName, PatientFirstName, PatientBloodType, PatientAllergies, PatientICELastName, PatientICEFirstName, PatientICEPhone, PatientPCPLastName, PatientPCPFirstName, PatientPCPPhone, PatientNotes, LoginHash):
	
	# Connect to the SQL DB and Modify Patient Name
	DBPosition = PMPSDatabase.cursor() 
	DBPosition.execute("""UPDATE medical_profiles SET bloodtype = %s, allergies = %s, ICE_lastname = %s, ICE_firstname = %s,  ICE_phone = %s,  PCP_lastname = %s, PCP_firstname = %s, PCP_phone = %s, notes = %s WHERE lastname = %s AND firstname = %s""", (PatientBloodType, PatientAllergies, PatientICELastName, PatientICEFirstName, PatientICEPhone, PatientPCPFirstName, PatientPCPLastName, PatientPCPPhone, PatientNotes, PatientLastName, PatientFirstName))
	# Keep track of query in the debug log
	print >> DebugLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AppendPatientInfo','\n'
	# Store the result as a dict for return
	ReturnDict = dict(StatusMessage = 'Patient information has been successfully appended!', SuccessfulQuery = 1)
	return(ReturnDict)

def ModifyPatientInfo(PatientLastName, PatientFirstName, PatientBloodType, PatientAllergies, PatientICELastName, PatientICEFirstName, PatientICEPhone, PatientPCPLastName, PatientPCPFirstName, PatientPCPPhone, PatientNotes, LoginHash):
	# Connect to the SQL DB and Modify Patient Name
	DBPosition = PMPSDatabase.cursor() 
	DBPosition.execute("""UPDATE medical_profiles SET bloodtype = %s, allergies = %s, ICE_lastname = %s, ICE_firstname = %s,  ICE_phone = %s,  PCP_lastname = %s, PCP_firstname = %s, PCP_phone = %s, notes = %s WHERE lastname = %s AND firstname = %s""", (PatientBloodType, PatientAllergies, PatientICELastName, PatientICEFirstName, PatientICEPhone, PatientPCPFirstName, PatientPCPLastName, PatientPCPPhone, PatientNotes, PatientLastName, PatientFirstName))
	# Keep track of query in the debug log
	print >> DebugLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo','\n'
	# Store the result as a dict for return
	ReturnDict = dict(StatusMessage = 'Patient information has been successfully modified!', SuccessfulQuery = 1)
	return(ReturnDict)
