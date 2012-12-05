<?php

	require_once 'validation.php';
	
	$initialUsername = $_POST["username"];
	$initialPassword = $_POST["password"];
	
	$username = cleanData(trim($initialUsername));
	$password = cleanData(trim($initialPassword));
	
	$connectArr = array('username' => $username, 'password' => $password, 'ip_address' => $_SERVER['REMOTE_ADDR']);
	$arr = array('method' => 'login', 'request' => $connectArr );
	$requestJSON = json_encode($arr);
	$requestJSONEnc = mcrypt_encrypt(MCRYPT_3DES,$ks,$requestJSON,MCRYPT_MODE_ECB);
	$responseJSONEnc = sendJSONgetJSON($requestJSONEnc);
	$responseJSON = mcrypt_decrypt(MCRYPT_3DES,$ks,$responseJSONEnc,MCRYPT_MODE_ECB);
	// Encryption/Decryption algorithm is adding padding to conform to the block-size. Null-characters are needed to be removed from the end by rtrim function
	$responseArr = json_decode(rtrim($responseJSON, "\0"),true);
	$authNum = $responseArr["response"]["authenticated"];
	$loginHash = $responseArr["response"]["login_hash"];

	session_start();
	if ($authNum === 1) {
		$accessLevel = $responseArr["response"]["accesslevel"];
		print $accessLevel;
		
		$_SESSION["loginIP"] = $_SERVER['REMOTE_ADDR'];
		$_SESSION["loginHash"] = $loginHash;
		$_SESSION["username"] = $username;
		
		if ($accessLevel === "admin") {
			$_SESSION["access"] = "admin";
			header( 'Location: ./home_admin.php' );
		}
		else if ($accessLevel === "readwrite") {
			$_SESSION["access"] = "readwrite";
			header( 'Location: ./home_doctor.php' );
		}
		else if ($accessLevel === "readonly") {
			$_SESSION["access"] = "readonly";
			header( 'Location: ./home_emt.php' );
		}
		else {
			$_SESSION["access"] = "none";
			$_SESSION["errorMsg"] = "Login Failed: Invalid Username/Password";
			header( 'Location: ./index.php' );
			
		}
	} else {
		$_SESSION["access"] = "none";
		$_SESSION["errorMsg"] = "Login Failed: Invalid Username/Password";
		header( 'Location: ./index.php' );
	} 
	
	
?>