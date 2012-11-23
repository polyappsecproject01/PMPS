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
			  if (($_SESSION["access"] == "admin") || ($_SESSION["access"] == "readwrite")) {
					require_once 'validation.php';
					$patFirstName = cleanData(trim($_POST["patFirstName"]));
					$patLastName = cleanData(trim($_POST["patLastName"]));
					$patBloodType = $_POST["patBloodType"];
					$patAllergies = cleanData(trim($_POST["patAllergies"]));
					$patICEFirstName = cleanData(trim($_POST["patICEFirstName"]));
					$patICELastName = cleanData(trim($_POST["patICELastName"]));
					$patICEPhone = cleanData(trim($_POST["patICEPhone"]));
					$patPCPFirstName = cleanData(trim($_POST["patPCPFirstName"]));
					$patPCPLastName  = cleanData(trim($_POST["patPCPLastName"]));
					$patPCPPhone = cleanData(trim($_POST["patPCPPhone"]));
					$patNotes = cleanData(trim($_POST["patNotes"]));
		
					
					if ( (!empty($patFirstName)) && (!empty($patLastName)) && (!empty($patBloodType)) && (!empty($patAllergies)) && (!empty($patICEFirstName)) && (!empty($patICELastName)) && (!empty($patICEPhone)) && (!empty($patPCPFirstName)) && (!empty($patPCPLastName)) && (!empty($patPCPPhone)) && (!empty($patNotes)) ) {
					
						$auth_dataArr = array('username' => $_SESSION["username"], 'ip_address' => $_SERVER['REMOTE_ADDR'], 'login_hash' => $_SESSION["loginHash"]);
						$ICEArr = array('firstname' => $patICEFirstName , 'lastname' => $patICELastName , 'phone' => $patICEPhone );
						$PCPArr = array('firstname' => $patPCPFirstName , 'lastname' => $patPCPLastName , 'phone' => $patPCPPhone );
						$requestArr = array('firstname' => $patFirstName, 'lastname' => $patLastName, 'bloodtype' => $patBloodType, 'allergies' => $patAllergies, 'ICEcontact' => $ICEArr, 'PCP' => $PCPArr, 'notes' => $patNotes  );
						$arr = array('method' => 'updateprofile', 'auth_data' => $auth_dataArr,'request' => $requestArr );
						$requestJSON = json_encode($arr);		
						$responseJSON = sendJSONgetJSON($requestJSON);
						$responseArr = json_decode($responseJSON,true);	
						$method = $responseArr["method"];
						$authNum = $responseArr["response"]["updated"];
						
						if ($method == "updateprofile")  {
							if ($authNum === 1) {
								print ("<i>$patFirstName $patLastName</i> profile is now updated with new data.");
							} else if ($authNum === 0)
								print ("Error: Could not update the profile of <i>$patFirstName $patLastName</i>. Please check if patient profile exists.");
						} else print("Error: JSON Response");
					} else print "Please enter valid info in all fields.";
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
