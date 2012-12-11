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
						$timeout = $responseArr["response"]["timeout"];
						if ($method == "getprofile")  {
							if ($authNum === 1) {

									
 								$retData = array(
 									'firstname' => $responseArr["response"]["firstname"],
 									'lastname' => $responseArr["response"]["lastname"],
 									'bloodtype' => $responseArr["response"]["bloodtype"],
 									'allergies' => $responseArr["response"]["allergies"],	
 									'ICE' => $responseArr["response"]["ICEcontact"],
 									'PCP' => $responseArr["response"]["PCP"],
 									'notes' =>  $responseArr["response"]["notes"] 								
 								);

								$retValue = array(
									'result' =>'succ',
									'errMsg' =>'',
									'data' => $retData
								);								

							} else if ($authNum === 0){
								if($timeout ===1){
									$retValue = array(
										'result' =>'fail',
										'errMsg' =>"Your session is timeout, you need relogin",
										'data' => ''
									);
								}else{
									$retValue = array(
										'result' =>'fail',
										'errMsg' =>"This user's profile doesn't exist in the system's record",
										'data' => ''
									);

								}
						
							}
									
								//print ("Could not find <i>$patFirstName $patLastName</i> in the system's records.");
						} else {

							//print("Error: JSON Response");
							$retValue = array(
								'result' =>'fail',
								'errMsg' =>"Data Error, please retry",
								'data' => ''
							);

						}
					} else{
							//print "Please enter valid first and last names.";
						$retValue = array(
							'result' =>'fail',
							'errMsg' =>'Please enter valid first and last names.'.$_POST["patFirstName"].','.$_POST["patLastName"],
							'data' => ''
						);

					} 
			  }else {
				  	if (!empty($_SESSION["errorMsgLogout"]))
				  		//print '<p style="color:#BE2C07;">'.$_SESSION["errorMsgLogout"].'</p>';
				  		$msg = $_SESSION["errorMsgLogout"];

				  		
 					//print "{$_SESSION["username"]}: You are not autherized to use this function. Logging of for security purposes.";
					$retValue = array(
							'result' =>'fail',
							'errMsg' => $msg.'<br>'.'$_SESSION["username"],you are not autherized to use this function. Logging of for security purposes.',
							'data' => ''
					);
						
					
					 session_unset();
					 session_destroy();
			  }
		  }
	
		  else{
		  	//print "You need to login first before using the system.";
		  		$retValue = array(
						'result' =>'fail',
						'errMsg' => 'You need to login first before using the system.',
						'data' => ''
				);
		  } 

 		//$output = json_encode($retValue);
		$output = json_encode($retValue);
		print ($output);
								

		 /* 
		if ($_SESSION["access"] == "readonly")
			   print '<p><a href="home_emt.php">Return to Home Page</a></p>';
		else if ($_SESSION["access"] == "readwrite")
			   print '<p><a href="home_doctor.php">Return to Home Page</a></p>';	
		else if ($_SESSION["access"] == "admin")
			   print '<p><a href="home_admin.php">Return to Home Page</a></p>';		
			*/			 
?>