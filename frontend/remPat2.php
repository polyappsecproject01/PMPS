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
			  if ($_SESSION["access"] == "admin") {
					require_once 'validation2.php';
					
					$patFirstName = cleanData(trim($_POST["patFirstName"]));
					$patLastName = cleanData(trim($_POST["patLastName"]));
					
					if ( (!empty($patFirstName)) && (!empty($patLastName)) ) {
					
						$auth_dataArr = array('username' => $_SESSION["username"], 'ip_address' => $_SERVER['REMOTE_ADDR'], 'login_hash' => $_SESSION["loginHash"]);
						$requestArr = array('firstname' => $patFirstName, 'lastname' => $patLastName);
						$arr = array('method' => 'removeprofile', 'auth_data' => $auth_dataArr,'request' => $requestArr );
					
						$requestJSON = json_encode($arr);
						$requestJSONEnc = mcrypt_encrypt(MCRYPT_3DES,$ks,$requestJSON,MCRYPT_MODE_ECB);
						$responseJSONEnc = sendJSONgetJSON($requestJSONEnc);
						$responseJSON = mcrypt_decrypt(MCRYPT_3DES,$ks,$responseJSONEnc,MCRYPT_MODE_ECB);
						// Encryption/Decryption algorithm is adding padding to conform to the block-size. Null-characters are needed to be removed from the end by rtrim function
						$responseArr = json_decode(rtrim($responseJSON, "\0"),true);
						$method = $responseArr["method"];
						$authNum = $responseArr["response"]["removed"];
						$timeout = $responseArr["response"]["timeout"];
						if ($method == "removeprofile")  {
							if ($authNum === 1) {
								print ("<i>$patFirstName $patLastName</i> was successfuly removed from the system.");
							} else if ($authNum === 0){
								if($timeout===1){
									print ("Your session is timeout, you need relogin.");
								}else{
									print ("Error: Could not remove <i>$patFirstName $patLastName</i> from the system.");	
								}
								

							}
								
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
		if ($timeout===1)
				print '<p><a href="index2.php">Return to Login Page</a></p>';
		else if ($_SESSION["access"] == "readonly")
			   print '<p><a href="home_emt2.php">Return to Home Page</a></p>';
		else if ($_SESSION["access"] == "readwrite")
			   print '<p><a href="home_doctor2.php">Return to Home Page</a></p>';	
		else if ($_SESSION["access"] == "admin")
			   print '<p><a href="home_admin2.php">Return to Home Page</a></p>';					 
	?>

 
	</section>
   	<footer>
    	<p>Copyright © Team PMPS</p>
    </footer>
</div>
</body>
</html>
