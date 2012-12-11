<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Patient Medical Profile System</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.js"></script>
<!-- Google Customized Web Fonts !-->
<link href='https://fonts.googleapis.com/css?family=Raleway:200' rel='stylesheet' type='text/css'>
<link href='https://fonts.googleapis.com/css?family=Candal' rel='stylesheet' type='text/css'>
<script type="application/javascript" src="indexInitialValidation.js"></script>

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
	<section id="main">
    <form method="post" action="auth2.php">
        <input type="text" class="inp" name="username" placeholder="Username" onchange="initialUserValidation(this.form)" />
		<input type="password" class="inp" name="password" placeholder="Password" onchange="initialPassValidation(this.form)" />
        <input type="hidden" name="errUser" value="true">
        <input type="hidden" name="errPass" value="true">
        <input type="submit" id="login"  value="Login" >
    </form>
    <?php
		session_start();
		if (!empty($_SESSION["access"])) {
			if ($_SESSION["access"] == "readonly")
				header( 'Location: ./home_emt2.php' );
			else if ($_SESSION["access"] == "readwrite")
				header( 'Location: ./home_doctor2.php' );
			else if ($_SESSION["access"] == "admin")
				header( 'Location: ./home_admin2.php' );
			else if ($_SESSION["access"] == "none") {
				print '<p id="loginError">'.$_SESSION["errorMsg"].'</p>';
				unset($_SESSION["errorMsg"]);
			}
		}
	 ?>
     <br />
     <p><a style="font-size:12px; color:#93A9F7; font-weight:bold;" href="https://github.com/polyappsecproject01/PMPS/blob/master/Project_Documentation/BugTracker-PMPS.pdf"/>Latest Bug Tracker Update</a></p>
	</section>
   	<footer>
    	<p>Copyright © Team PMPS</p>
    </footer>
</div>
<!-- This is just to deal with placeholder in IE !-->
<script src="jquery.placeholder.js"></script>
<script>
	$(function() { $('input').placeholder();});
</script>
</body>
</html>