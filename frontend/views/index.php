<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Patient Medical Profile System</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.js"></script>
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
	<section id="main">
    <form method="post" action="auth.php">
        <input type="text" class="inp" name="username" placeholder="Username"  />
		<input type="password" class="inp" name="password" placeholder="Password"/>
        <input type="submit" id="login"  value="Login" >
    </form>
    <?php
		session_start();
		if (!empty($_SESSION["access"])) {
			if ($_SESSION["access"] == "readonly")
				header( 'Location: ./home_emt.php' );
			else if ($_SESSION["access"] == "readwrite")
				header( 'Location: ./home_doctor.php' );
			else if ($_SESSION["access"] == "admin")
				header( 'Location: ./home_admin.php' );
			else if ($_SESSION["access"] == "none") {
				print '<p id="loginError">'.$_SESSION["errorMsg"].'</p>';
				unset($_SESSION["errorMsg"]);
			}
		}
	 ?>
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