<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Patient Medical Profile System</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<!-- Google Customized Web Fonts !-->
<link href='https://fonts.googleapis.com/css?family=Raleway:200' rel='stylesheet' type='text/css'>
<link href='https://fonts.googleapis.com/css?family=Candal' rel='stylesheet' type='text/css'>

<link rel="stylesheet" href="style.css" />
</head>
<body>
<script type="text/javascript">
function whenHover(p) {
	p.src="logo_pmpsc_on.png";
}

function afterHover(p) {
	p.src="logo_pmpsc.png";
}
</script>
<div id="container">
    <header>
       <img id="logoPic" src="logo_pmpsc.png" onmouseover="whenHover(this)" onmouseout="afterHover(this)"/>
    </header>
	<section id="processInfo">
    <br />
	<?php
		  session_start();
		
		  if (!empty($_SESSION["access"]))
		  {
			  if (($_SESSION["access"] == "readonly") || ($_SESSION["access"] == "readwrite") || ($_SESSION["access"] == "admin")) {
					require_once 'validation.php';
		
					$initialPatFirstName = $_POST["patFirstName"];
					$initialPatLastName= $_POST["patLastName"];
					
					$patFirstName = cleanData(trim($initialPatFirstName));
					$patLastName = cleanData(trim($initialPatLastName));
					
					if ( (!empty($patFirstName)) && (!empty($patLastName)) ) {
					
						$auth_dataArr = array('username' => $_SESSION["username"], 'ip_address' => $_SERVER['REMOTE_ADDR'], 'login_hash' => $_SESSION["loginHash"]);
						$requestArr = array('firstname' => $patFirstName, 'lastname' => $patLastName);
						$arr = array('method' => 'getprofile', 'auth_data' => $auth_dataArr,'request' => $requestArr );
					
						$requestJSON = json_encode($arr);
						$requestJSONEnc = mcrypt_encrypt(MCRYPT_3DES,$ks,$requestJSON,MCRYPT_MODE_ECB);
						$responseJSONEnc = sendJSONgetJSON($requestJSONEnc);
						$responseJSON = mcrypt_decrypt(MCRYPT_3DES,$ks,$responseJSONEnc,MCRYPT_MODE_ECB);
						// Encryption/Decryption algorithm is adding padding to conform to the block-size. Null-characters are needed to be removed from the end by rtrim function
						$responseArr = json_decode(rtrim($responseJSON, "\0"),true);
						$method = $responseArr["method"];
						$authNum = $responseArr["response"]["retrieved"];
						
						if ($method == "getprofile")  {
							if ($authNum === 1) {
								$firstname = $responseArr["response"]["firstname"];	
								$lastname = $responseArr["response"]["lastname"];	
								$bloodtype = $responseArr["response"]["bloodtype"];	
								$allergies = $responseArr["response"]["allergies"];	
								$ICEcontactFirstName = $responseArr["response"]["ICEcontact"]["firstname"];
								$ICEcontactLastName = $responseArr["response"]["ICEcontact"]["lastname"];
								$ICEcontactPhone = $responseArr["response"]["ICEcontact"]["phone"];	
								$PCPFirstName = $responseArr["response"]["PCP"]["firstname"];	
								$PCPLastName = $responseArr["response"]["PCP"]["lastname"];	
								$PCPPhone = $responseArr["response"]["PCP"]["phone"];	
								$notes = $responseArr["response"]["notes"];	
								
								print '<table id="tableResults">';
								print "<tr><td><b>First Name</b></td><td><b>Last Name</b></td><td><b>Blood Type</b></td><td><b>Allergies</b></td><td><b>ICE Contact: First Name</b></td><td><b>ICE Contact: Last Name</b></td><td><b>ICE Contact: Phone</b></td><td><b>PCP Contact: First Name</b></td><td><b>PCP Contact: Last Name</b></td><td><b>PCP Contact: Phone</b></td></tr>";
								print ("<tr><td> $firstname</td><td> $lastname</td><td> $bloodtype</td><td> $allergies</td><td> $ICEcontactFirstName</td><td> $ICEcontactLastName</td><td> $ICEcontactPhone</td><td> $PCPFirstName</td><td> $PCPLastName</td><td> $PCPPhone</td></tr>");
								print '</table>';
								if (!empty($notes)) {
									print '<br /><table id="notesResults">';
									print ("<tr><td><b><u>Notes</u></b></td></tr><tr><td> $notes</td></tr>");
									print '</table><br />';
								}
							} else if ($authNum === 0)
								print ("Could not find <i>$patFirstName $patLastName</i> in the system's records.");
						} else print("Error: JSON Response");
					} else print "Please enter valid first and last names.";
			  }
			  else {
				  	if (!empty($_SESSION["errorMsgLogout"]))
						print '<p style="color:#BE2C07;">'.$_SESSION["errorMsgLogout"].'</p>';
						
					 print "{$_SESSION["username"]}: You are not autherized to use this function. Logging of for security purposes.";
					 session_unset();
					 session_destroy();
			  }
		  }
		  else print "You need to login first before using the system.";
		  
		if ($_SESSION["access"] == "readonly")
			   print '<p><a href="home_emt.php">Return to Home Page</a></p>';
		else if ($_SESSION["access"] == "readwrite")
			   print '<p><a href="home_doctor.php">Return to Home Page</a></p>';	
		else if ($_SESSION["access"] == "admin")
			   print '<p><a href="home_admin.php">Return to Home Page</a></p>';					 
	?>

 
	</section>
   	<footer>
    	<p>Copyright © Team PMPS</p>
    </footer>
</div>
</body>
</html>
