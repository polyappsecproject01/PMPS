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
	<section id="logout">
    <br />
	<?php
		  require_once 'validation.php';
		  session_start();
		
		  // An authenticated user has logged out -- be polite and thank them for
		  // using your application.
		  if (!empty($_SESSION["access"]))
		  {
			  if ($_SESSION["access"] != "none") {
				
				if (!empty($_SESSION["errorMsgLogout"]))
					print '<p style="color:#BE2C07;">'.$_SESSION["errorMsgLogout"].'</p>';
					
				$auth_dataArr = array('username' => $_SESSION["username"], 'ip_address' => $_SERVER['REMOTE_ADDR'], 'login_hash' => $_SESSION["loginHash"]);
				$arr = array('method' => 'logout', 'auth_data' => $auth_dataArr);
				$requestJSON = json_encode($arr);
				$requestJSONEnc = mcrypt_encrypt(MCRYPT_3DES,$ks,$requestJSON,MCRYPT_MODE_ECB);
				$responseJSONEnc = sendJSONgetJSON($requestJSONEnc);
				$responseJSON = mcrypt_decrypt(MCRYPT_3DES,$ks,$responseJSONEnc,MCRYPT_MODE_ECB);
				// Encryption/Decryption algorithm is adding padding to conform to the block-size. Null-characters are needed to be removed from the end by rtrim function
				$responseArr = json_decode(rtrim($responseJSON, "\0"),true);
				$authNum = $responseArr["response"]["logged_out"];
				session_unset();
				session_destroy();	
				
				if ($authNum === 1) {
				
					print "Thank you {$_SESSION["username"]} for using PMPS. You are now logged off.";
					
				} else print "Error: Problem with JSON.";
				
			  }
			  else print "You need to login first before logging out.";
		  }
		  else print "You need to login first before logging out.";			 
	?>

    <p><a href="index.php">Return to Main Page</a></p>
	</section>
   	<footer>
    	<p>Copyright © Team PMPS</p>
    </footer>
</div>
</body>
</html>
