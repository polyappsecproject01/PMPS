PMPS
====

Patient Medical Profile System

Note: Non-technical project information can be find under Project_Documents folder and on our GitHub's Wiki.

--------------------------------------------------------------
Useful Configuration and Administration Information (Linux VM)
--------------------------------------------------------------

Main Website:

https://pmps.poly.edu
https://pmps.poly.edu/phpmyadmin

Packages Installed:

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

Important Files and Directories:

iptables → /etc/sysconfig/iptables
Apache config → /etc/httpd/conf/httpd.conf
Apache SSL config → /etc/httpd/conf.d/ssl.conf
Host directory (default) → /var/www/html/ (also PMPS frontend)
PMPS backend → /var/backend/

Application Daemons and Related Running Instructions:

Apache, MySQL Server, and Backend

The Apache webserver is automatically run upon startup. To restart, type:
sudo service httpd restart

MySQL

The MySQL database server is automatically run upon startup. To restart, type:
sudo /etc/init.d/mysqld restart
PMPS Backend

The PMPS backend program currently does not run upon startup. To start, type:
sudo nohup /var/backend/start_pmps


Login username/password for Testing Purposes:

EMT Permission: emt/Medicinerules1120*
Doctor Permission: doctor/Medicinerules1120*
Admin Permission: admin/Medicinerules1120*


Other Configuration Information:

Allow PHP to connect to Python socket:

semanage port -a -t http_port_t -p tcp 1390
$/usr/sbin/setsebool httpd_can_network_connect=1
SELinux Notes

http://blog.domb.net/?p=89
Installing php-mcrypt

sudo rpm -ivh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-7.noarch.rpm
sudo yum install libmcrypt
sudo yum install php-mcrypt (not just “mcrypt”!)
sudo updatedb
/etc/php.d/mcrypt.ini - create with line “extensions = mcrypt.so”
sudo reboot
