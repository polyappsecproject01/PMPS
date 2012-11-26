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
from hash_utilities import * # JV
import MySQLdb
import string

# Initialize Database Connection
dbinfodata = getdbinfo() # Retrieve db info from local file
PMPSDatabase = MySQLdb.connect(user=dbinfodata[0], passwd=dbinfodata[1], db=dbinfodata[2])

# Initialize Logs
ErrorLog = open("errorlog.log", 'a')
DebugLog = open("debuglog.log", 'a')
ActivityLog = open("activitylog.log", 'a')
LoginLog = open("loginlog.log", 'a')

# Global Constants
global TimeOutValue
TimeOutValue = datetime.timedelta(minutes=15) # Login timeout value
global ValidUserLevels
ValidUserLevels = ['readonly', 'readwrite', 'admin'] # Define the Valid User Levels (e.g. corresponding to EMT, Doctor, Admin)
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

# This function is a universal handler for input strings from the frontend
# Though it may be redundant, it prevents attacks where the adversary writes
# their own frontend and attempts to interact with the backend directly
# Note:  The Python SQL API escapes all %s, (var) when in this format, 
# so injection is protected against.

# Valid Inputs
        # UserName = 15 alphanum
        # Password = 30 char
        # Patient*Name = 30 alpha
        # LoginHash = 64 hex
        # PatientBloodType = O+, O-, A+, A-, B+, B-, AB+, AB-
        # PatientAllergies = 500 char
        # *Phone= 16 int
        # PatientNotes = 5000 char
        # NewAccessLevel = readonly, readwrite, admin


def ValidateInput(CheckThisInput, MaxStringLength, AllowedCharacters, FixInputAutomatically):
	# Initialize input status as unacceptable
	InputAcceptable = 0

	# Ensure an acceptable type has been passed to the function.  This cannot be automatically corrected.
	if (type(CheckThisInput) not in [int, str]):
		ReturnDict = dict(InputAcceptable = 0)
		return (ReturnDict)
	
	# Convert an int input to a string type
	CheckThisInput = str(CheckThisInput)

	# Check the length of the string
	InitialInputLength = len(CheckThisInput)
	if (InitialInputLength > MaxStringLength):
		if (FixInputAutomatically == 1): 
			# If it is too long, and the input is set to be automatically corrected, truncate it
			CheckThisInput = CheckThisInput[0:MaxStringLength]
		else: # If the input shouldn't be autocorrected
			ReturnDict = dict(InputAcceptable = 0)
			return (ReturnDict)
	
	# If the length is ok or corrected, check for allowable characters in the string
	for character in CheckThisInput:
		if (character not in (AllowedCharacters)):
			if (FixInputAutomatically == 1):
				# Rather than simply raising an error, remove all bad characters from the 
				# input and provide an acceptable string for use.
				CheckThisInput = string.replace(CheckThisInput, character, '')
			else: # If the input shouldn't be autocorrected
				ReturnDict = dict(InputAcceptable = 0)
				return (ReturnDict)		

	# Either the input was initially ok, or it was corrected to be acceptable and can be returned
	ReturnDict = dict(AcceptableValue = CheckThisInput, InputAcceptable = 1)
	return (ReturnDict)

def AuthenticateUser(UserName, Password): # JV - (AC removed IP_Address until frontend can reliably generate this, added timestamp refresh on successful login, added logging, added lockout code, added validation)

	# Validate Inputs
	ValidatedUserName = ValidateInput(UserName, 15, (string.ascii_letters + string.digits), 0)
	if ValidatedUserName['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AuthenticateUser Failed: User Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPassword = ValidateInput(Password, 30, (string.ascii_letters + string.digits + string.punctuation), 0) # Since this gets hashed before being stored, there is no risk of SQL injection regardless
	if ValidatedPassword['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AuthenticateUser Failed: Password entered with invalid characters','\n'
                return (ReturnDict)
	
        # Connect to SQL DB and Retrieve Information
        DBPosition = PMPSDatabase.cursor()
        DBPosition.execute("""SELECT password_salt, password_hash, accesslevel FROM users WHERE username = %s""", (UserName))
        row = DBPosition.fetchone()
        if row == None:
		ReturnDict = dict(Message = 'User name and/or password invalid!', SuccessfulQuery = 0) # Purposely inspecific
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AuthenticateUser Failed: User Name does not exist','\n'
                return (ReturnDict)
	
	# Check for lockout, and if true, do not try to authenticate
	DBPosition = PMPSDatabase.cursor()
	DBPosition.execute("""SELECT lockout_counter FROM users WHERE username = %s""", (UserName))
	CurrentCount = DBPosition.fetchone()
 	if CurrentCount[0] == 'Locked':
		ReturnDict = dict(Message = 'This account is locked due to multiple unsuccessful login attempts, please contact an Administrator!', SuccessfulQuery = 0) # Purposely inspecific
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AuthenticateUser Failed: Account is locked.','\n'
		return (ReturnDict)

	salt, expected_hash, accesslevel = row

        this_hash = CalcHash(salt, Password)

        if this_hash == expected_hash:
                login_hash = GenRandomHash()

                DBPosition.execute("""UPDATE users SET login_hash = %s WHERE username = %s""",
                                   (login_hash, UserName))
		UpdateTimestamp(UserName, login_hash) # Added to complete validation of the new session

		DBPosition = PMPSDatabase.cursor() # Need to reset the lockout counter to 0
		DBPosition.execute("""UPDATE users SET lockout_counter = %s WHERE username = %s""", (0,UserName))
		CurrentCount = DBPosition.fetchone()

 		ReturnDict = {"LoginHash":login_hash,"SuccessfulQuery":1,"accesslevel":accesslevel}
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AuthenticateUser',UserName,'Successful!','\n'
		return (ReturnDict)
        
	else:
		
		ReturnDict = dict(Message = 'User name and/or password invalid!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AuthenticateUser Failed: Password incorrect','\n'
                # Increment the user lockout counter due to incorrect password entry
		DBPosition = PMPSDatabase.cursor()
		DBPosition.execute("""SELECT lockout_counter FROM users WHERE username = %s""", (UserName))
		CurrentCount = DBPosition.fetchone()
		if (CurrentCount[0] <> 'Locked'):
			CurrentCount = int(CurrentCount[0])
			NewCount = CurrentCount+1
			DBPosition = PMPSDatabase.cursor()
			DBPosition.execute("""UPDATE users SET lockout_counter = %s WHERE username = %s""", (NewCount, UserName))		
			# If the count is 5 or more (somehow) then lock the account
			if (NewCount > 4):
				LockedAccount = 'Locked'
				DBPosition = PMPSDatabase.cursor()
				DBPosition.execute("""UPDATE users SET lockout_counter = %s WHERE username = %s""", (LockedAccount, UserName))		
				print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'User',UserName,'account is locked due to five consecutive incorrect password attempts.','\n'
		return(ReturnDict)

def RetrievePatientInfo(PatientLastName, PatientFirstName, LoginHash):

	# Validate Inputs
	ValidatedPatientLastName = ValidateInput(PatientLastName, 30, (string.ascii_letters), 0)
	if ValidatedPatientLastName['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RetrievePatientInfo Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientFirstName = ValidateInput(PatientFirstName, 30, (string.ascii_letters), 0)
	if ValidatedPatientFirstName['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RetrievePatientInfo Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedLoginHash = ValidateInput(LoginHash, 64, (string.hexdigits), 0)
	if ValidatedLoginHash['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RetrievePatientInfo Failed: Login Hash contains invalid characters','\n'
                return (ReturnDict)
	
	# Ensure the LoginHash is valid and has the proper permissions associated with it.
	# All valid user levels may use this function	
	PermissionsOKList = ValidUserLevels 
	ValidLogins = RequestValidLogins() # Returns the valid logins tuple 
	# Tuple form: [(username, login_hash, accesslevel)] 
	
	print ValidLogins # Trace Entry
	
	# Check the corresponding Login Hash (Session ID) and check the user's permission level
	SuccessfulQuery = 0 # Variable to check if the query returns anything
	for UserHashLevel in ValidLogins:  
		print UserHashLevel[1]
		if ((UserHashLevel[1] == LoginHash) & (UserHashLevel[2] in PermissionsOKList)): # if the hashes match and the user has permission
			# Connect to SQL DB and Retrieve Information
			DBPosition = PMPSDatabase.cursor() 
			DBPosition.execute("""SELECT * FROM medical_profiles WHERE lastname = %s AND firstname = %s""", (PatientLastName, PatientFirstName))
			QueryResult = DBPosition.fetchone()
			if (QueryResult <> None): # If there is a result found
				# Keep track of query in the activity log
				print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RetrievePatientInfo by',UserHashLevel[0],'\n'
				# Store the result as a dict for return
				ReturnDict = dict(PatientLastName = QueryResult[2], PatientFirstName = QueryResult[1], PatientBloodType = QueryResult[3], PatientAllergies = QueryResult[4], PatientICELastName = QueryResult[6], PatientICEFirstName = QueryResult[5], PatientICEPhone = QueryResult[7], PatientPCPLastName = QueryResult[9], PatientPCPFirstName = QueryResult[8], PatientPCPPhone = QueryResult[10], PatientNotes = QueryResult[11], SuccessfulQuery = 1)
				SuccessfulQuery = 1
				# On successful request, update the timestamp 
				UpdateTimestamp(UserHashLevel[0], UserHashLevel[1])
	if  (SuccessfulQuery == 0):
		ReturnDict = dict(Message = 'Failed to retrieve patient information!', SuccessfulQuery = 0)
	return(ReturnDict)

def AddNewPatient(PatientLastName, PatientFirstName, LoginHash):
		
	# Validate Inputs
	ValidatedPatientLastName = ValidateInput(PatientLastName, 30, (string.ascii_letters), 0)
	if ValidatedPatientLastName['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewPatientInfo Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientFirstName = ValidateInput(PatientFirstName, 30, (string.ascii_letters), 0)
	if ValidatedPatientFirstName['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewPatientInfo Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedLoginHash = ValidateInput(LoginHash, 64, (string.hexdigits), 0)
	if ValidatedLoginHash['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewPatientInfo Failed: Login Hash contains invalid characters','\n'
                return (ReturnDict)

	# Ensure the LoginHash is valid and has the proper permissions associated with it.
	# Only those with write permissions can access this (Doctors and Admins)	
	PermissionsOKList = ValidUserLevels[1:]
	ValidLogins = RequestValidLogins() # Returns the valid logins tuple 
	# Tuple form: [(username, login_hash, accesslevel)] 
	
	print ValidLogins # Trace Entry
	
	# Check the corresponding Login Hash (Session ID) and check the user's permission level
	SuccessfulQuery = 0 # Variable to check if the query returns anything
	for UserHashLevel in ValidLogins:  
		print UserHashLevel[1]
		if ((UserHashLevel[1] == LoginHash) & (UserHashLevel[2] in PermissionsOKList)): # if the hashes match and the user has permission
			# Ensure the patient name does not already exist 
			DBPosition = PMPSDatabase.cursor()
			DBPosition.execute("""SELECT * FROM medical_profiles WHERE lastname = %s AND firstname = %s""", (PatientLastName, PatientFirstName))
			DuplicateUsers = DBPosition.fetchone()
			if (DuplicateUsers == None):
				# Connect to the SQL DB and Add New Patient
				DBPosition = PMPSDatabase.cursor() 
				DBPosition.execute("""INSERT INTO medical_profiles (lastname, firstname) VALUES (%s, %s)""", (PatientLastName, PatientFirstName))
				# Keep track of query in the activity log
				print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewPatient by',UserHashLevel[0],'\n'
				# Store the result as a dict for return
				ReturnDict = dict(StatusMessage = 'New patient has been successfully added!', SuccessfulQuery = 1)
				SuccessfulQuery = 1
				# On successful request, update the timestamp 
				UpdateTimestamp(UserHashLevel[0], UserHashLevel[1])
	if  (SuccessfulQuery == 0):
		ReturnDict = dict(Message = 'Failed to add new patient information!', SuccessfulQuery = 0)
	return(ReturnDict)

def RemovePatient(PatientLastName, PatientFirstName, LoginHash):

	# Validate Inputs
	ValidatedPatientLastName = ValidateInput(PatientLastName, 30, (string.ascii_letters), 0)
	if ValidatedPatientLastName['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RemovePatient Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientFirstName = ValidateInput(PatientFirstName, 30, (string.ascii_letters), 0)
	if ValidatedPatientFirstName['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RemovePatient Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedLoginHash = ValidateInput(LoginHash, 64, (string.hexdigits), 0)
	if ValidatedLoginHash['InputAcceptable'] == 0:
		ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RemovePatient Failed: Login Hash contains invalid characters','\n'
                return (ReturnDict)
	
	# Ensure the LoginHash is valid and has the proper permissions associated with it.
	# Only those with admin permissions can access this (Admins only)	
	PermissionsOKList = ValidUserLevels[2:]
	ValidLogins = RequestValidLogins() # Returns the valid logins tuple 
	# Tuple form: [(username, login_hash, accesslevel)] 
	
	print ValidLogins # Trace Entry
	
	# Check the corresponding Login Hash (Session ID) and check the user's permission level
	SuccessfulQuery = 0 # Variable to check if the query returns anything
	for UserHashLevel in ValidLogins:  
		print UserHashLevel[1]
		if ((UserHashLevel[1] == LoginHash) & (UserHashLevel[2] in PermissionsOKList)): # if the hashes match and the user has permission
			# Connect to the SQL DB and Remove Patient
			DBPosition = PMPSDatabase.cursor() 
			DBPosition.execute("""DELETE FROM medical_profiles WHERE lastname = %s AND firstname = %s""", (PatientLastName, PatientFirstName))
			# Keep track of query in the activity log
			print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RemovePatient by',UserHashLevel[0],'\n'
			# Store the result as a dict for return
			ReturnDict = dict(StatusMessage = 'Patient has been successfully removed!', SuccessfulQuery = 1)
			SuccessfulQuery = 1
			# On successful request, update the timestamp 
			UpdateTimestamp(UserHashLevel[0], UserHashLevel[1])
	if  (SuccessfulQuery == 0):
		ReturnDict = dict(Message = 'Failed to remove patient information!', SuccessfulQuery = 0)
	return(ReturnDict)

def ModifyPatientName(PatientLastNameCurrent, PatientFirstNameCurrent, PatientLastNameNew, PatientFirstNameNew, LoginHash):
	
	# Validate Inputs
	ValidatedPatientLastNameCurrent = ValidateInput(PatientLastNameCurrent, 30, (string.ascii_letters), 0)
	if ValidatedPatientLastNameCurrent['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientName Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)
	
	ValidatedPatientFirstNameCurrent = ValidateInput(PatientFirstNameCurrent, 30, (string.ascii_letters), 0)
	if ValidatedPatientFirstNameCurrent['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientName Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientLastNameNew = ValidateInput(PatientLastNameNew, 30, (string.ascii_letters), 0)
	if ValidatedPatientLastNameNew['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientName Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientFirstNameNew = ValidateInput(PatientFirstNameNew, 30, (string.ascii_letters), 0)
	if ValidatedPatientFirstNameNew['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientName Failed: Patient Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedLoginHash = ValidateInput(LoginHash, 64, (string.hexdigits), 0)
	if ValidatedLoginHash['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientName Failed: Login Hash contains invalid characters','\n'
                return (ReturnDict)

	# Ensure the LoginHash is valid and has the proper permissions associated with it.
	# Only those with admin permissions can access this (Admins only)	
	PermissionsOKList = ValidUserLevels[2:]
	ValidLogins = RequestValidLogins() # Returns the valid logins tuple 
	# Tuple form: [(username, login_hash, accesslevel)] 
	
	print ValidLogins # Trace Entry
	
	# Check the corresponding Login Hash (Session ID) and check the user's permission level
	SuccessfulQuery = 0 # Variable to check if the query returns anything
	for UserHashLevel in ValidLogins:  
		print UserHashLevel[1]
		if ((UserHashLevel[1] == LoginHash) & (UserHashLevel[2] in PermissionsOKList)): # if the hashes match and the user has permission
			# Ensure the patient name does not already exist 
			DBPosition = PMPSDatabase.cursor()
			DBPosition.execute("""SELECT * FROM medical_profiles WHERE lastname = %s AND firstname = %s""", (PatientLastNameNew, PatientFirstNameNew))
			DuplicateUsers = DBPosition.fetchone()
			if (DuplicateUsers == None):
				# Connect to the SQL DB and Modify Patient Name
				DBPosition = PMPSDatabase.cursor() 
				DBPosition.execute("""UPDATE medical_profiles SET lastname = %s, firstname = %s WHERE lastname = %s AND firstname = %s""", (PatientLastNameNew, PatientFirstNameNew, PatientLastNameCurrent, PatientFirstNameCurrent))
				# Keep track of query in the activity log
				print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientName by',UserHashLevel[0],'\n'
				# Store the result as a dict for return
				ReturnDict = dict(StatusMessage = 'Patient name has been successfully updated!', SuccessfulQuery = 1)
				SuccessfulQuery = 1
				# On successful request, update the timestamp 
				UpdateTimestamp(UserHashLevel[0], UserHashLevel[1])
	if  (SuccessfulQuery == 0):
		ReturnDict = dict(Message = 'Failed to modify patient name!', SuccessfulQuery = 0)
	return(ReturnDict)

def ModifyPatientInfo(PatientLastName, PatientFirstName, PatientBloodType, PatientAllergies, PatientICELastName, PatientICEFirstName, PatientICEPhone, PatientPCPLastName, PatientPCPFirstName, PatientPCPPhone, PatientNotes, LoginHash):

	# Validate Inputs
	
	ValidatedPatientLastName = ValidateInput(PatientLastName, 30, (string.ascii_letters), 0)
	if ValidatedPatientLastName['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient Last Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientFirstName = ValidateInput(PatientFirstName, 30, (string.ascii_letters), 0)
	if ValidatedPatientFirstName['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient First Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidBloodTypes = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
	ValidatedPatientBloodType = ValidateInput(PatientBloodType, 3, ValidBloodTypes, 0)
	if ValidatedPatientBloodType['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient Bloodtype entered with invalid characters','\n'
                return (ReturnDict)
	
	ValidatedPatientAllergies = ValidateInput(PatientAllergies, 500, (string.ascii_letters + string.digits + string.whitespace), 1)
	if ValidatedPatientAllergies['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient Allergies entered with invalid characters','\n'
                return (ReturnDict)
	PatientAllergies = ValidatedPatientAllergies['AcceptableValue']

	ValidatedPatientICELastName = ValidateInput(PatientICELastName, 30, (string.ascii_letters), 0)
	if ValidatedPatientICELastName['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient ICE Last Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientICEFirstName = ValidateInput(PatientICEFirstName, 30, (string.ascii_letters), 0)
	if ValidatedPatientICEFirstName['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient ICE First Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientICEPhone = ValidateInput(PatientICEPhone, 16, (string.digits), 1)
	if ValidatedPatientICEPhone['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient ICE Phone entered with invalid characters','\n'
                return (ReturnDict)
	PatientICEPhone = ValidatedPatientICEPhone['AcceptableValue']

	ValidatedPatientPCPLastName = ValidateInput(PatientPCPLastName, 30, (string.ascii_letters), 0)
	if ValidatedPatientPCPLastName['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient PCP Last Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientPCPFirstName = ValidateInput(PatientPCPFirstName, 30, (string.ascii_letters), 0)
	if ValidatedPatientPCPFirstName['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient PCP First Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedPatientPCPPhone = ValidateInput(PatientPCPPhone, 16, (string.digits), 1)
	if ValidatedPatientPCPPhone['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient PCP Phone entered with invalid characters','\n'
                return (ReturnDict)
	PatientPCPPhone = ValidatedPatientPCPPhone['AcceptableValue']
	
	ValidatedPatientNotes = ValidateInput(PatientNotes, 5000, (string.ascii_letters + string.digits + string.whitespace), 1)
	if ValidatedPatientNotes['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Patient Notes entered with invalid characters','\n'
                return (ReturnDict)
	PatientNotes = ValidatedPatientNotes['AcceptableValue']
	
	ValidatedLoginHash = ValidateInput(LoginHash, 64, (string.hexdigits), 0)
	if ValidatedLoginHash['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo Failed: Login Hash contains invalid characters','\n'
                return (ReturnDict)
	
	# Ensure the LoginHash is valid and has the proper permissions associated with it.
	# Only those with write permissions can access this (Admins and Doctors only)	
	PermissionsOKList = ValidUserLevels[1:]
	ValidLogins = RequestValidLogins() # Returns the valid logins tuple 
	# Tuple form: [(username, login_hash, accesslevel)] 
	
	print ValidLogins # Trace Entry
	
	# Check the corresponding Login Hash (Session ID) and check the user's permission level
	SuccessfulQuery = 0 # Variable to check if the query returns anything
	for UserHashLevel in ValidLogins:  
		print UserHashLevel[1]
		if ((UserHashLevel[1] == LoginHash) & (UserHashLevel[2] in PermissionsOKList)): # if the hashes match and the user has permission
			# Connect to the SQL DB and Modify Patient Name
			DBPosition = PMPSDatabase.cursor() 
			DBPosition.execute("""UPDATE medical_profiles SET bloodtype = %s, allergies = %s, ICE_lastname = %s, ICE_firstname = %s,  ICE_phone = %s,  PCP_lastname = %s, PCP_firstname = %s, PCP_phone = %s, notes = %s WHERE lastname = %s AND firstname = %s""", (PatientBloodType, PatientAllergies, PatientICELastName, PatientICEFirstName, PatientICEPhone, PatientPCPFirstName, PatientPCPLastName, PatientPCPPhone, PatientNotes, PatientLastName, PatientFirstName))
			# Keep track of query in the activity log
			print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'ModifyPatientInfo by',UserHashLevel[0],'\n'
			# Store the result as a dict for return
			ReturnDict = dict(StatusMessage = 'Patient information has been successfully modified!', SuccessfulQuery = 1)
			SuccessfulQuery = 1
			# On successful request, update the timestamp 
			UpdateTimestamp(UserHashLevel[0], UserHashLevel[1])
	if  (SuccessfulQuery == 0):
		ReturnDict = dict(Message = 'Failed to modify patient information!', SuccessfulQuery = 0)
	return(ReturnDict)

def AddNewUser(NewUserName, NewUserAccessLevel, NewUserPass, LoginHash):

	# Validate Inputs
	ValidatedNewUserName = ValidateInput(NewUserName, 15, (string.ascii_letters + string.digits), 0)
	if ValidatedNewUserName['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser Failed: New User Name entered with invalid characters','\n'
                return (ReturnDict)

	ValidatedNewUserAccessLevel = ValidateInput(NewUserAccessLevel, 9, string.ascii_letters, 0)
	if ValidatedNewUserAccessLevel['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser Failed: New User Access Level entered with invalid characters','\n'
                return (ReturnDict)
	
	ValidatedNewUserPass = ValidateInput(NewUserPass, 30, (string.ascii_letters + string.digits + string.punctuation), 0) # Since this gets hashed before being stored, there is no risk of SQL injection regardless
	if ValidatedNewUserPass['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser Failed: New User Password entered with invalid characters','\n'
                return (ReturnDict)
	
	ValidatedLoginHash = ValidateInput(LoginHash, 64, (string.hexdigits), 0)
	if ValidatedLoginHash['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser Failed: Login Hash contains invalid characters','\n'
                return (ReturnDict)

	# Ensure the LoginHash is valid and has the proper permissions associated with it.
	# Only those with admin permissions can access this (Admins only)	
	PermissionsOKList = ValidUserLevels[2:]
	ValidLogins = RequestValidLogins() # Returns the valid logins tuple 
	# Tuple form: [(username, login_hash, accesslevel)] 
	
	print ValidLogins # Trace Entry
	
	# Check the corresponding Login Hash (Session ID) and check the user's permission level
	SuccessfulQuery = 0 # Variable to check if the query returns anything
	# First ensure that the access level assigned is valid
	if (NewUserAccessLevel in ValidUserLevels):
		print "Passwords match, valid access level requested." # Trace
		if (ValidLogins == ()):
			ReturnDict = dict(Message = 'No valid sessions are active!  Please log in and try again.', SuccessfulQuery = 0)
			print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser Failed:',ReturnDict['Message'],'\n'
			SuccessfulQuery = 39 # Arbitrary value so that ReturnDict is not reassigned by the final if statement below.	
		for UserHashLevel in ValidLogins:  			
			if ((UserHashLevel[1] == LoginHash) & (UserHashLevel[2] in PermissionsOKList)): # if the hashes match and the user has permission
				print "Valid hash with proper permissions found!", UserHashLevel[1] # Trace
				# Ensure the user name does not already exist 
				DBPosition = PMPSDatabase.cursor()
				DBPosition.execute("""SELECT username FROM users WHERE username = %s""", (NewUserName))
				DuplicateUsers = DBPosition.fetchone()
				print "Current List of Duplicate Users:", DuplicateUsers
				if (DuplicateUsers == None): # if current user does not exist
					# Calculate the salt and hash for storage
					PasswordSalt = GenRandomHash()
					PasswordHash = CalcHash(PasswordSalt, NewUserPass)
					DBPosition = PMPSDatabase.cursor() 
					# Add new user
					DBPosition.execute("""INSERT INTO users (username, password_salt, password_hash, accesslevel) VALUES (%s, %s, %s, %s)""", (NewUserName, PasswordSalt, PasswordHash, NewUserAccessLevel))
					# Keep track of query in the activity log
					print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser by',UserHashLevel[0],'(Successful)','\n'
					# Store the result as a dict for return
					ReturnDict = dict(StatusMessage = 'New user has been successfully added!', SuccessfulQuery = 1)
					SuccessfulQuery = 1
					# On successful request, update the timestamp 
					UpdateTimestamp(UserHashLevel[0], UserHashLevel[1])
				else:
					ReturnDict = dict(Message = 'User already exists!', SuccessfulQuery = 0)
					print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser by',UserHashLevel[0],'Failed:',ReturnDict['Message'],'\n'
					SuccessfulQuery = 39 # Arbitrary value so that ReturnDict is not reassigned by the final if statement below.	
			else: 
				ReturnDict = dict(Message = 'Invalid User Hash (Session ID) or User Permissions do not allow this operation!', SuccessfulQuery = 0)
				print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser by',UserHashLevel[0],'Failed:',ReturnDict['Message'],'\n'
				SuccessfulQuery = 39 # Arbitrary value so that ReturnDict is not reassigned by the final if statement below.	
	else:
		ReturnDict = dict(Message = 'The passwords selected for the new user did not match or the requested access level is invalid!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser Failed:',ReturnDict['Message'],'\n'
		SuccessfulQuery = 39 # Arbitrary value so that ReturnDict is not reassigned by the final if statement below.
	if  (SuccessfulQuery == 0):
		ReturnDict = dict(Message = 'Failed to add new user!', SuccessfulQuery = 0)
	return(ReturnDict)	

def RemoveUser(UserName, LoginHash):
	
	# Validate Inputs
	ValidatedUserName = ValidateInput(UserName, 15, (string.ascii_letters + string.digits), 0)
	if ValidatedNewUserName['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'AddNewUser Failed: User Name entered with invalid characters','\n'
                return (ReturnDict)
	
	ValidatedLoginHash = ValidateInput(LoginHash, 64, (string.hexdigits), 0)
	if ValidatedLoginHash['InputAcceptable'] == 0:
                ReturnDict = dict(Message = 'Invalid characters entered or input too long!', SuccessfulQuery = 0)
		print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RemoveUser Failed: Login Hash contains invalid characters','\n'
                return (ReturnDict)
	
	# Ensure the LoginHash is valid and has the proper permissions associated with it.
	# Only those with admin permissions can access this (Admins only)	
	PermissionsOKList = ValidUserLevels[2:]
	ValidLogins = RequestValidLogins() # Returns the valid logins tuple 
	# Tuple form: [(username, login_hash, accesslevel)] 
	
	print ValidLogins # Trace Entry
	
	# Check the corresponding Login Hash (Session ID) and check the user's permission level
	SuccessfulQuery = 0 # Variable to check if the query returns anything
	# First ensure that the two passwords entered for the new user match (NewUserPass1, 2)
	for UserHashLevel in ValidLogins:  
		print UserHashLevel[1]
		if ((UserHashLevel[1] == LoginHash) & (UserHashLevel[2] in PermissionsOKList)): # if the hashes match and the user has permission
			# And the specified username is not the same as the user requesting the removal (user cannot remove his/herself)
			if (UserHashLevel[0] <> UserName):
				# Then remove the specified user
				DBPosition = PMPSDatabase.cursor()
				DBPosition.execute("""DELETE FROM users WHERE username = %s""", (UserName))
				print >> ActivityLog, 'Timestamp:',datetime.datetime.now(),'\n', 'RemoveUser by',UserHashLevel[0],'\n'
				# Store the result as a dict for return
				ReturnDict = dict(StatusMessage = 'User has been successfully removed!', SuccessfulQuery = 1)
				SuccessfulQuery = 1
				# On successful request, update the timestamp 
				UpdateTimestamp(UserHashLevel[0], UserHashLevel[1])
	if  (SuccessfulQuery == 0):
		ReturnDict = dict(Message = 'Failed to remove user!', SuccessfulQuery = 0)
	return(ReturnDict)	
