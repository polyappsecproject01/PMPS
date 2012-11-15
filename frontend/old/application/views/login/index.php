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
	<?php echo validation_errors(); ?>

	<?php
		$login_error = $this->session->flashdata('login_error');
		if ($login_error) {
	?>
	<div style="border: 1px solid black; background-color: #00FF00; width: 600px;">
		<?php echo $login_error; ?>
	</div>
	<?php } ?>
    <form method="post" action="<?php echo current_url(); ?>">
        <input type="text" class="inp" name="username" placeholder="Username" />
		<input type="password" class="inp" name="password" placeholder="Password" />
        <input type="submit" id="login"  value="Login" >
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
	$(function() { $('input').placeholder();});
</script>

<?php $this->load->view('footer'); ?>