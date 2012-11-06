<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Login extends CI_Controller {

	public function __construct()
	{
		parent::__construct();

		//If the current page the user is on is not the login page, and they aren't logged in via a session, redirect them to the login page.
		if ($this->session->userdata('logged_in') == FALSE && ($this->router->class != 'login' || $this->router->method != 'index')) {
			redirect('/login');
		}
	}

	public function index()
	{
		$this->form_validation->set_rules('username', 'Username', 'required');
		$this->form_validation->set_rules('password', 'Password', 'required');

		// If form validation fails, load login page again until user fills form properly
		if ($this->form_validation->run() == FALSE) {
			$this->load->view('login/index');
		// Form filled properly, attempt to login the user
		} else {
			$valid_login = array('username' => 'admin', 'password' => 'yoshi');

			// User doesn't match, set error message and present login page again
			if ($this->input->post('username') != $valid_login['username'] || $this->input->post('password') != $valid_login['password']) {
				$this->session->set_flashdata('login_error', 'Invalid login information. Please try again.');
				
				redirect('/login');
			// Inputted data is a match, set session and redirect to backend page
			} else {
				$this->session->set_userdata('logged_in', TRUE);
				
				redirect('/backend');
			}
		}
	}
	
	public function logout()
	{
		// Destroy session data
		$this->session->sess_destroy();

		// Redirect back to login page
		redirect('/login');
	}

}