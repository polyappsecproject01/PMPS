<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Backend extends CI_Controller {

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
		$this->search();
	}

	public function search()
	{
		$this->load->library('zeromq');
		//$this->zeromq->send('BLAH!');
	
		$this->load->view('backend/search');
	}

}