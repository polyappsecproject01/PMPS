<?php $this->load->view('header'); ?>

<script type="text/javascript">
function whenHover(p) {
	p.src="assets/images/logo_pmpsc_on.png";
}

function afterHover(p) {
	p.src="assets/images/logo_pmpsc.png";
}
</script>

<div id="container">
    <header>
       <img id="logoPic" src="assets/images/logo_pmpsc.png" onmouseover="whenHover(this)" onmouseout="afterHover(this)"/>
    </header>
	<section id="main">
	<div style="border: 1px solid black; color:red;background-color: #00FF00; width: 600px;">	
		<?php echo validation_errors(); ?>
	</div>
	<?php
		$login_error = $this->session->flashdata('login_error');
		if ($login_error) {
	?>
	<div style="color:red;background-color: #00FF00; width: 600px;">
		<?php echo $login_error; ?>
	</div>
	<?php } ?>
    <form method="post" id="loginform" action="<?php echo current_url(); ?>">
        <input type="text" class="inp" name="username" placeholder="Username" />
		<input type="password" class="inp" name="password" placeholder="Password" />
        <input type="button" id="login"  value="Login" class="submitlogin" >
    </form>
	<p style="color:#FFF; font-family:Verdana, Geneva, sans-serif; font-size:12px"><a href="../home_emt.php" class="links" style="color:#039">EMT Control Panel</a> | <a href="../home_doctor.php" style="color:#039">Doctor Control Panel</a> | <a href="../home_admin.php" style="color:#039">Admin Control Panel</a></p>
	</section>
   	<footer>
    	<p>Copyright 2012 Team PMPS</p>
    </footer>
</div>
<!-- This is just to deal with placeholder in IE !-->
<script src="jquery.placeholder.js"></script>
<script>
	$(function() { 
		//$('input').placeholder();
		$(".submitlogin").click(function(){

			$.ajax({
			  type: "POST",
			  url: "<?php echo site_url();?>login/login_check",
			//this data is mendetory when u want post data when posting page by ajax.
			//after that ur data send to that page. now in backend page echo json data.if your //data is in array format the use json_encode() function then echo that json data
			//now you find tht json in your success that can you use by taking a loop.
			  data: $("#loginform").serialize(),
			  cache: false,
			 datatype: 'json',
			  success: function(html){
			  $("ul#update").append(html);
			
			   alert(html);   
			  }
			 });
				
		});
		
	});
</script>

<?php $this->load->view('footer'); ?>