PMPS
=====

Patient Medical Profile System

--------------------------------------------------------------------------
Useful Configuration and Administration Information (Linux VM) 
--------------------------------------------------------------------------
** Can also be found at Useful Configuration and Administration Information.pdf under Project_Documentation

## Main Website
https://pmps.poly.edu   
https://pmps.poly.edu/phpmyadmin  

## Packages Installed
0MQ (but not used)  
Apache 2.2.15  
MySQL 5.1.x  
MySQL Server 5.1.x  
PHP 5.3.x  
php-mcrypt  
PHP-MySQL 5.3.x  
MySQL-python 1.2.3-x  
phpMyAdmin  
pyDes-2.0.1  
setools-console-3.3.7-4.e16.x86_64  

## Important Files and Directories
iptables → /etc/sysconfig/iptables  
Apache config → /etc/httpd/conf/httpd.conf  
Apache SSL config → /etc/httpd/conf.d/ssl.conf  
Host directory (default) → /var/www/html/ (also PMPS frontend)  
PMPS backend → /var/backend/

## Application Daemons
### Apache, MySQL Server, and Backend
The Apache webserver is automatically run upon startup. To restart, type:  
sudo service httpd restart

### MySQL
The MySQL database server is automatically run upon startup. To restart, type:  
sudo /etc/init.d/mysqld restart

### PMPS Backend
The PMPS backend program currently does not run upon startup. To start, type:  
sudo nohup /var/backend/start_pmps  
[Note: Try to get /etc/init.d/pmpsd to work.]

## Logins for Test Purposes
EMT Permission: emt/Medicinerules1120*  
Doctor Permission: doctor/Medicinerules1120*  
Admin Permission: admin/Medicinerules1120*

## Allow PHP to connect to Python socket
semanage port -a -t http_port_t -p tcp 1390  
$/usr/sbin/setsebool httpd_can_network_connect=1

## SELinux Notes
http://blog.domb.net/?p=89

## Installing php-mcrypt
sudo rpm -ivh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-7.noarch.rpm  
sudo yum install libmcrypt  
sudo yum install php-mcrypt (not just “mcrypt”!)  
sudo updatedb  
/etc/php.d/mcrypt.ini - create with line “extensions = mcrypt.so”  
sudo reboot

-------------------------------------------------------------------
Front-End General Information and Security Mechanisms 
-------------------------------------------------------------------
** Can also be found at PMPS_Front_End_Readme.pdf under Project_Documentation

Front-End General Information and Structure

Login Process and Interface
- index.php
Login Authentication
- auth.php
JavaScript Validation:
- initialValidation.js
PHP Validation
- validation.php
Restricted Views:
- home_emt.php
- home_doctor.php
- home_admin.php
Logout Interface
- logout.php
Additional API Functions
- retPatInfo.php
- addPat.php
- modPatInfo.php
- modPatName
- remPat.php
Design Elements
- style.css
- jquery.placeholder.js


Security Mechanisms:

JavaScript-based Data-Validation
- Validating user inputs at real-time
- Indicating and removing invalid inputs from forms
- Preventing invalid inputs from being sent to further processing pages
- Invalid inputs also include injection attack string

PHP-based API Functions
- Data-validation layer
- Transmitting encrypted Login JSON request over TCP port to Back-End
- Receiving, decrypting ,validating and authenticating Login JSON response
- Encoding a JSON request per an API function
- Transmitting encrypted JSON request over TCP port to Back-End
- Receiving  encrypted JSON response which matches the request
- Decrypting and validating JSON response attributes and setting session variables accordingly
- Print retrieved data on a specific webpage
- Each API function is being processed independently of other functions (unique .php file)

PHP-based Restricted Views
- Access to restricted views is based on session variables and additional authentication mechanisms
- An additional data-validation layer
- Access to relevant API functionality presented is restricted base on type of permission


-----------------------------------------------------------
Additional Related Files under Project_Documents
------------------------------------------------------------

BugTracker-PMPS.pdf
- Contains bug-related issues and keeps track of known issues

JSON.pdf
- Information about the JSON commincation requests and responses for each of the API functions

Restricted Database Call API.pdf
- Contains information about the restricted database call API

Databases.pdf
- Information about the structure of the SQL-based database

Application Security Notes and Discussions.pdf
- General security notes about PMPS

Application Security Project Proposal
- The proposal of the project

Concept of Operations
- Explaination about the operation of PMPS
