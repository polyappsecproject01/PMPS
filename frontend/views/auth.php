<?php

	require_once 'validation.php';
	
	$initialUsername = $_POST["username"];
	$initialPassword = $_POST["password"];
	
	$username = cleanData(trim($initialUsername));
	$password = cleanData(trim($initialPassword));
	
	$connectArr = array('username' => $username, 'password' => $password, 'ip_address' => $_SERVER['REMOTE_ADDR']);
	$arr = array('method' => 'login', 'request' => $connectArr );

	$requestJSON = json_encode($arr);
	$responseJSON = sendJSONgetJSON($requestJSON);
	$responseArr = json_decode($responseJSON,true);
	
	$authNum = $responseArr["response"]["authenticated"];
	$loginHash = $responseArr["response"]["login_hash"];
	
	session_start();
	if ($authNum === 1) {
		$accessLevel = $responseArr["response"]["accesslevel"];
		
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