<?php

	// Generate key and convert it to 24 bytes characters to be used for TCP internal communication encryption & decryption between
	// Front-End and Back-End (private-key shared encyption)
	function hexToChar($hex) {
	   $rv = '';
	   foreach(str_split($hex, 2) as $b) {
			   $rv .= chr(hexdec($b));
	   }
	   return $rv;
	}	
	$keyaschii = "014ef7bc441754e45e3a53496a4028469a166a11172ff6c6"; // key can be up to 24 bytes
	$ks = hexToChar($keyaschii);
	
	// Clean data to protect against Injection Attacks
	function cleanData($string) {
		if(get_magic_quotes_gpc())  // prevents duplicate backslashes
			$string = stripslashes($string);
			
		$string = mysql_escape_string($string);

		return $string;
	} 
	
	function sendJSONgetJSON($jsonData) {
		
		// Create the socket
		// Address Family : AF_INET (this is IP version 4)
		// Type : SOCK_STREAM (this means connection oriented TCP protocol)
		// Protocol : 0 [ or IPPROTO_IP This is IP protocol]
		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		if ($socket === false) {
			echo "socket_create() failed: reason: " . 
				 socket_strerror(socket_last_error()) . "\n";
		}
		// Connect to the socket
		$result = socket_connect($socket, 'localhost' , 1390);
		if ($result === false) {
			echo "socket_connect() failed.\nReason: ($result) " . 
				  socket_strerror(socket_last_error($socket)) . "\n";
		}
			
		// Send JSON over socket connection
		if (!socket_write($socket, $jsonData, strlen($jsonData)))
			echo "Error: JSON could not be sent.";
		
		
		$response = '';
		while ($response_line = socket_read($socket, 1390)) 
		{
			$response .= $response_line;
		}
		
		socket_close($socket);
		
		return $response;
	}

	
	// Connects to a session and checks that the user has
	// authenticated and that the remote IP address matches
	// the address used to create the session.
	
	function sessionAuthenticateEMT() {
	  // Check if the user hasn't logged in
	  if (!isset($_SESSION["loginHash"]) || ($_SESSION["access"] != "readonly"))
	  {
		// The request does not identify a session
		$_SESSION["errorMsgLogout"] = "Hi There:) You are not authorized to access this URL. Sorry!";
		header("Location: logout.php");
		exit;
	  }
	
	  // Check if the request is from a different IP address to previously
	  if (!isset($_SESSION["loginIP"]) || 
		 ($_SESSION["loginIP"] != $_SERVER["REMOTE_ADDR"]))
	  {
		// The request did not originate from the machine
		// that was used to create the session.
		// THIS IS POSSIBLY A SESSION HIJACK ATTEMPT
	
		$_SESSION["access"] = "none";
		$_SESSION["errorMsgLogout"] = "You are not authorized to access the URL 
								{$_SERVER["REQUEST_URI"]} from the address 
								{$_SERVER["REMOTE_ADDR"]}";
	
		header("Location: logout.php");
		exit;
	  }
	}
	
	function sessionAuthenticateDoctor() {
	  // Check if the user hasn't logged in
	  if (!isset($_SESSION["loginHash"]) || ($_SESSION["access"] != "readwrite"))
	  {
		// The request does not identify a session
		$_SESSION["errorMsgLogout"] = "Hi There:) You are not authorized to access this URL. Sorry!";
	
		header("Location: logout.php");
		exit;
	  }
	
	  // Check if the request is from a different IP address to previously
	  if (!isset($_SESSION["loginIP"]) || 
		 ($_SESSION["loginIP"] != $_SERVER["REMOTE_ADDR"]))
	  {
		// The request did not originate from the machine
		// that was used to create the session.
		// THIS IS POSSIBLY A SESSION HIJACK ATTEMPT
	
		$_SESSION["access"] = "none";
		$_SESSION["errorMsgLogout"] = "Hi There:) You are not authorized to access the URL 
								{$_SERVER["REQUEST_URI"]} from the address 
								{$_SERVER["REMOTE_ADDR"]}";
	
		header("Location: logout.php");
		exit;
	  }
	}
	
	function sessionAuthenticateAdmin() {
	  // Check if the user hasn't logged in
	  if (!isset($_SESSION["loginHash"]) || ($_SESSION["access"] != "admin"))
	  {
		// The request does not identify a session
		$_SESSION["errorMsgLogout"] = "Hi There:) You are not authorized to access this URL. Sorry!";
	
		header("Location: logout.php");
		exit;
	  }
	
	  // Check if the request is from a different IP address to previously
	  if (!isset($_SESSION["loginIP"]) || 
		 ($_SESSION["loginIP"] != $_SERVER["REMOTE_ADDR"]))
	  {
		// The request did not originate from the machine
		// that was used to create the session.
		// THIS IS POSSIBLY A SESSION HIJACK ATTEMPT
	
		$_SESSION["access"] = "none";
		$_SESSION["errorMsgLogout"] = "You are not authorized to access the URL 
								{$_SERVER["REQUEST_URI"]} from the address 
								{$_SERVER["REMOTE_ADDR"]}";
	
		header("Location: logout.php");
		exit;
	  }
	}

?>