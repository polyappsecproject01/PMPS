<?php
require_once('./validation.php');

session_start();
sessionAuthenticateEMT();

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<title>Patient Medical Profile System - EMT View</title> 
<script type="text/javascript" src="initialValidation.js"></script>
<link href='https://fonts.googleapis.com/css?family=Raleway' rel='stylesheet' type='text/css'>
<link rel="stylesheet" href="style.css" />
</head> 
<body> 
<div id="container">
	<header>
    	<img id="logoPic" src="logo_pmpsc.png" onmouseover="this.src='logo_pmpsc_on.png';" onmouseout="this.src='logo_pmpsc.png'"/><br /><br />
	</header>
	<div id="userView">
   		<form method="POST" action="logout.php">
        <h3>Status:</h3><h4><?php  if (isset($_SESSION["username"])) echo "Logged in as <b>".$_SESSION["username"]."</b>";  ?></h4>
        <input type="submit" value="Logout">
        </form>
        
        <br />
        <br />
        <h3>Retrieve Patient Info:</h3><br />
        <table>
        <form action="retPatInfo.php" method="POST">
            <tr>
            <td>
            <h4>First Name:</h4><input type="text" maxlength="30" name="patFirstName" onchange="validFirstName(this,'retPatError')" />
            <h4>Last Name:</h4><input type="text" maxlength="30" name="patLastName" onchange="validLastName(this,'retPatError')" />
            <input type="submit" value="Find Patient"><td id="retPatError"></td>
            </td>
            </tr>
            <tr><td><p id="vResults"></p></td></tr>
         </form>
        </table>
        </div> <!-- END OF DIV main !-->
	<div id="results">
	</div> <!-- END OF DIV results !-->
    <footer>
    <p>Copyright © Team PMPS</p>
    </footer>
</div>
</body> 
</html> 