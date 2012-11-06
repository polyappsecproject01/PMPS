# CS9163 Application Security Group Project - Patient Medical Profile System (PMPS)
# Python Reference Monitor Between Frontend and SQL Database
# This module handles all requests from the frontend to the SQL DB 
# All requests are parsed and validated by individual character.
# All requests utilize the session ID to verify privledge level of the request being made.
# The code for this portion of the assignment was written by Anthony C. (acanda01) (10/2012).
# Some portions of this module were written by Jeffrey Valino and will be commented with "JV"
# This code was tested successfully on Python 2.6.6, on the provided Linux VM at pmps.poly.edu.

'''
~~~~~~******SESSION VALIDATION******~~~~~~
This portion of the code will validate each session user level as properly logged in.  It will set the login hash (session 
id) to a 64 bit hex number = 0 and represented as string ('0'*64) after logout or timeout.  A timeout is currently defined
as 15 minutes without user activity.

'''

# Module Imports
from dbinfo import *
import datetime
import hash_utilities # JV
import MySQLdb

# Initialize Database Connection
dbinfodata = getdbinfo() # Retrive db info from local file
PMPSDatabase = MySQLdb.connect(user=dbinfodata[0], passwd=dbinfodata[1], db=dbinfodata[2])

# Initialize Logs
ErrorLog = open("errorlog.log", 'a')
DebugLog = open("debuglog.log", 'a')
LoginLog = open("loginlog.log", 'a')

# Global Constants
global TimeOutValue
TimeOutValue = datetime.timedelta(minutes=15) # Login timeout value
global ValidUserLevels
ValidUserLevels = ['EMT', 'Doctor', 'Admin'] # Define the Valid User Levels
global LoggedOutHash 
LoggedOutHash = '0'*64 # If the user is logged out the hash will read all zeros

# Timeout Functions
# Disallows the processing of requests from session IDs/ login hashes if the
# previous request was made more than 15 minutes prior.
# If the request is made within 15 minutes of the previous one, then the 
# session ID / login hash timestamp is refreshed.
# For EVERY database request made by a user, this function must be called.

# Check the time of the last request for a specific user and logout if > 15 min.
def CheckForTimeoutUser(UserName):
	# Retrieve a tuple consisting of the user if logged in (non-zero hashes) and their last access time (time of last request)
	DBPosition = PMPSDatabase.cursor()
	DBPosition.execute("""SELECT username, login_hash, last_access FROM users WHERE username = %s AND login_hash <> %s""", (UserName,LoggedOutHash))
	UserHashLastAccessTuple = DBPosition.fetchone()
	# Parse the time of last request and compare it with the current time
	TimeOfLastRequest = datetime.datetime.strptime(UserHashTimeAccessTuple[2], '%Y-%m-%d %H:%M:%S')
	print TimeOfLastRequest # Trace Entry
	CurrentTime = datetime.datetime.now()
	TimeDifference = CurrentTime - TimeOfLastRequest
	# If the time difference is greater than 15 call the logout function for this user	
	if (TimeDifference > TimeOutValue):
		LogoutSession(UserHashLastAccessTuple[1])
	print UserHashLastAccessTuple # Trace Entry

# Check the time of last requests for all users and logout if > 15 min.
def CheckForTimeoutAll():
	# Retrieve a tuple consisting of all logged in users (non-zero hashes) and their last access time (time of last request)
	DBPosition = PMPSDatabase.cursor()
	DBPosition.execute("""SELECT username, login_hash, last_access FROM users WHERE login_hash <> %s""", (LoggedOutHash))
	UserHashLastAccessTuple = DBPosition.fetchall()	
	print UserHashLastAccessTuple # Trace Entry
	# Check each user entry for timeout
	for UserHashTime in UserHashLastAccessTuple:
		TimeOfLastRequest = datetime.datetime.strptime(UserHashTime[2], '%Y-%m-%d %H:%M:%S')
		print TimeOfLastRequest
		CurrentTime = datetime.datetime.now()
		TimeDifference = CurrentTime - TimeOfLastRequest
		# If the time difference is greater than 15 call the logout function for this user
		if (TimeDifference > TimeOutValue):
			LogoutSession(UserHashTime[1])

# Request a list of currently valid logins
def RequestValidLogins():
	# Check to ensure that the corresponding sessions are not timed out
	# If it is, the function will set the hash to zero (log the user out)
	CheckForTimeoutAll()
	# Query the database and form a list of all logins with remaining active sessions
	DBPosition = PMPSDatabase.cursor()
	DBPosition.execute("""SELECT username, login_hash, accesslevel FROM users WHERE login_hash <> %s""", (LoggedOutHash))
	ValidLogins = DBPosition.fetchall()
	print "Valid Login List:", ValidLogins # Trace Entry
	return (ValidLogins)

# Update the timestamp (last_access) for a given user and login hash (session ID)
def UpdateTimestamp (UserName, LoginHash):
	NewTimestamp = datetime.datetime.now()
	DBPosition = PMPSDatabase.cursor()
	DBPosition.execute("""UPDATE users SET last_access = %s WHERE username = %s AND login_hash = %s""", (NewTimestamp, UserName, LoginHash))
		
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

def AuthenticateUser(UserName, Password, IP_Address): # JV
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
        
	ValidLogins = RequestValidLogins() # Returns the valid logins tuple 
	# Tuple form: [(username, login_hash, accesslevel)] 
	print ValidLogins # Trace Entry
	
	#for UserHashLevel in ValidLogins:
	#	if (ValidLogins[1] == LoginHash):
		#	if  # continue working here


               #                  print >> ErrorLog, 'Timestamp:',datetime.datetime.now(),'\n','User (',UserName,') Already Logged In.\n'
                #         if (NameLevelHashTime[2] == LoginHash): # Check for already used hash value / session ID
                 #               AlreadyLoggedIn = 1
                  #              print >> ErrorLog, 'Timestamp:',datetime.datetime.now(),'\n','User (',NameLevelHashTime[0],') is Already Using the Session

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
