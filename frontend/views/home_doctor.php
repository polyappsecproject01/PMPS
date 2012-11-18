<?php
require_once('./validation.php');

session_start();
sessionAuthenticateDoctor();

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
         </form>
        </table>
        <br />
        <h3>Add Patient with Medical Profile</h3><br />
        <form action="addPat.php" method="POST">
        <table class="tab">
            <tr><td>First Name:<input type="text" maxlength="30" name="patFirstName" onchange="validFirstName(this,'addPatError')" /></td><td>Last Name:<input type="text" maxlength="30" name="patLastName" onchange="validLastName(this,'addPatError')" /></td></tr>
            <tr><td>Patient Blood Type:<select name="patBloodType"><option value="O+">O+</option><option value="O-">O-</option><option value="A+">A+</option><option value="A-">A-</option><option value="B+">B+</option><option value="B-">B-</option><option value="AB+">AB+</option><option value="AB-">AB-</option></select></td><td>Allergies:<input type="text" name="patAllergies" maxlength="500" onchange="validAllergies(this,'addPatError')" /></td><td>ICELastName:<input type="text" maxlength="30" name="patICELastName" onchange="validICELastName(this,'addPatError')" /></td><td>ICEFirstName:<input type="text" maxlength="30" name="patICEFirstName" onchange="validICEFirstName(this,'addPatError')" /></td></tr>
            <tr><td>ICEPhone:<input type="text" maxlength="16" name="patICEPhone" onchange="validICEPhone(this,'addPatError')" /></td><td>PCPLastName:<input type="text" maxlength="30" name="patPCPLastName" onchange="validPCPLastName(this,'addPatError')" /></td><td>PCPFirstName:<input type="text" maxlength="30" name="patPCPFirstName" onchange="validPCPFirstName(this,'addPatError')" /></td><td>PCPPhone:<input type="text" maxlength="16" name="patPCPPhone" onchange="validPCPPhone(this,'addPatError')" /></td></tr>
            </table>
            <h5>Notes:</h5><br /><textarea name="patNotes" maxlength="5000" cols="40" rows="3" onchange="validNotes(this,'addPatError')"></textarea>
            <br />
            <input type="submit" value="Add Patient"><div id="addPatError"></div>
         </form>
        <br />
        <h3>Append Patient Info</h3><br />
        <form action="modPatInfo.php" method="POST">
        <table class="tab">
            <tr><td>First Name:<input type="text" maxlength="30" name="patFirstName" onchange="validFirstName(this,'modPatInfoError')" /></td><td>Last Name:<input type="text" maxlength="30" name="patLastName" onchange="validLastName(this,'modPatInfoError')" /></td></tr>
            <tr><td>Patient Blood Type:<select name="patBloodType"><option value="O+">O+</option><option value="O-">O-</option><option value="A+">A+</option><option value="A-">A-</option><option value="B+">B+</option><option value="B-">B-</option><option value="AB+">AB+</option><option value="AB-">AB-</option></select></td><td>Allergies:<input type="text" name="patAllergies" maxlength="500" onchange="validAllergies(this,'modPatInfoError')" /></td><td>ICELastName:<input type="text" maxlength="30" name="patICELastName" onchange="validICELastName(this,'modPatInfoError')" /></td><td>ICEFirstName:<input type="text" maxlength="30" name="patICEFirstName" onchange="validICEFirstName(this,'modPatInfoError')" /></td></tr>
            <tr><td>ICEPhone:<input type="text" maxlength="16" name="patICEPhone" onchange="validICEPhone(this,'modPatInfoError')" /></td><td>PCPLastName:<input type="text" maxlength="30" name="patPCPLastName" onchange="validPCPLastName(this,'modPatInfoError')" /></td><td>PCPFirstName:<input type="text" maxlength="30" name="patPCPFirstName" onchange="validPCPFirstName(this,'patPCPFirstName')" /></td><td>PCPPhone:<input type="text" maxlength="16" name="patPCPPhone" onchange="validPCPPhone(this,'patPCPPhone')" /></td></tr>
            </table>
            <h5>Notes:</h5><br /><textarea name="patNotes" maxlength="5000" cols="40" rows="3" onchange="validNotes(this,'modPatInfoError')"></textarea>
            <br />
            <input type="submit" value="Append Patient Info"><div id="modPatInfoError"></div>
         </form>
        </div> <!-- END OF DIV main !-->
	<div id="results">
	</div> <!-- END OF DIV results !-->
    <footer>
    <p>Copyright © Team PMPS</p>
    </footer>
</div>
</body> 
</html> 