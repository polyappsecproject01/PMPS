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
					require_once 'validation.php';
					
					$patFirstName = cleanData(trim($_POST["patFirstName"]));
					$patLastName = cleanData(trim($_POST["patLastName"]));
					
					if ( (!empty($patFirstName)) && (!empty($patLastName)) ) {
					
						$auth_dataArr = array('username' => $_SESSION["username"], 'ip_address' => $_SERVER['REMOTE_ADDR'], 'login_hash' => $_SESSION["loginHash"]);
						$requestArr = array('firstname' => $patFirstName, 'lastname' => $patLastName);
						$arr = array('method' => 'removeprofile', 'auth_data' => $auth_dataArr,'request' => $requestArr );
					
						$requestJSON = json_encode($arr);
						$responseJSON = sendJSONgetJSON($requestJSON);
						$responseArr = json_decode($responseJSON,true);	
						$method = $responseArr["method"];
						$authNum = $responseArr["response"]["removed"];
						
						if ($method == "removeprofile")  {
							if ($authNum === 1) {
								print ("<i>$patFirstName $patLastName</i> was successfuly removoed from the system.");
							} else if ($authNum === 0)
								print ("Error: Could not remove <i>$patFirstName $patLastName</i> from the system.");
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
