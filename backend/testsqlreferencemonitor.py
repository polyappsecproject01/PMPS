# Test Code for SQL POPO

from sqlreferencemonitor import *

#AddValidatedSession('Lando','EMT',12345)
#AddValidatedSession('Lando','EMT',12395)
#AddValidatedSession('Antny','EMT',123456)
#AddValidatedSession('John','Hacker',1337)
#AddValidatedSession('Joseph','Doctor',1234567)
AddValidatedSession('Jeremy','Admin',12345678) #This will be called by AuthenticateUser, never directly except for testing
#AddValidatedSession('Mike','Admin',12345678)
#LogoutSession(123456)
#RequestValidLogins()
#print AuthenticateUser('Lando', 'passwordlol')
#print RetrievePatientInfo('Doe', 'John', 12345678)
#print AddNewPatient('Lando', 'Calrissian', '0x12345')
#print RemovePatient('Lando', 'Calrissian', '0x12345')
#print AppendPatientInfo('Lando', 'Calrissian', 'O+', 'Penicillin', 'Kathy', 'Calrissian', '1234567890', 'Charles', 'Xavier', '2345678901', 'This patient is completely insane and a danger to society', '0x12345')
#print ModifyPatientName('Lando', 'Calrissian', 'Fat', 'Tony', '0x12345')
print ModifyPatientInfo('Ryan', 'Nolan', 'O+', 'Penicillin', 'Ryan', 'Julie', '1234567890', 'Charles', 'Xavier', '2345678901', 'This patient is completely insane and a danger to society', '0x12345')
#print AddNewPatient('C','Anthony', 12345)
#print RemovePatient('C','Anthony', 12345)
#print ModifyPatientName('C', 'Anthony', 'Ryan', 'Nolan', 12345)
 
