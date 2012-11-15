<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Login extends CI_Controller {

	public function __construct()
	{
		parent::__construct();
		$this->load->library('upload');
		$this->load->helper('date');
		$this->load->helper('form');
		$this->load->helper('url');

		//If the current page the user is on is not the login page, and they aren't logged in via a session, redirect them to the login page.
		if ($this->session->userdata('logged_in') == FALSE && ($this->router->class != 'login' || $this->router->method != 'index')) {
			//redirect('/login');
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

	//log the user in
	
	//log the user in
	function login()
	{
		
		$this->data['title'] = "Login";
		
		$this->data['first_name'] = array('name' => 'first_name',
			'id' => 'first_name',
			'type' => 'text',
			'value' => $this->form_validation->set_value('first_name'),
		);
		$this->data['email'] = array('name' => 'email',
			'id' => 'email',
			'type' => 'text',
			'value' => $this->form_validation->set_value('email'),
		);
		
		//validate form input
		$this->form_validation->set_rules('identity', 'Identity', 'required');
		$this->form_validation->set_rules('password', 'Password', 'required');

		if ($this->form_validation->run() == true)
		{ //check to see if the user is logging in
			//check for "remember me"
			$remember = (bool) $this->input->post('remember');

			if ($this->ion_auth->login($this->input->post('identity'), $this->input->post('password'), $remember))
			{ //if the login is successful
				//redirect them back to the home page
				if (!$this->ion_auth->is_admin())
                {
                    
                    $this->load->model('user_model');
                    $selected_language = $this->user_model->get_selected_language_id_and_name($this->session->userdata['user_id']);
					$this->session->set_userdata('site_language', $selected_language['selected_language_id']);
                    $this->config->set_item('language', strtolower($selected_language['language_name']));
					redirect('dashboard', 'refresh');
				}else {
                    $this->session->set_flashdata('message', $this->ion_auth->messages());
                    redirect($this->config->item('site_url').'admin', 'refresh');
                }
			}
			else
			{ //if the login was un-successful
				//redirect them back to the login page
				$this->session->set_flashdata('message', $this->ion_auth->errors());
				redirect('auth/login', 'refresh'); //use redirects instead of loading views for compatibility with MY_Controller libraries
			}
		}
		else
		{  //the user is not logging in so display the login page
			//set the flash data error message if there is one
			$this->data['message'] = (validation_errors()) ? validation_errors() : $this->session->flashdata('message');

			$this->data['identity'] = array('name' => 'identity',
				'id' => 'identity',
				'type' => 'text',
				'value' => $this->form_validation->set_value('identity'),
			);
			$this->data['password'] = array('name' => 'password',
				'id' => 'password',
				'type' => 'password',
			);

			//$data['content']=$this->load->view('auth/login', $this->data);
			$this->data['content']=$this->load->view('users/login',$this->data,true);
			$this->load->view('layout/index',$this->data);
		}
	}
	function login_check(){
		
		 $this->db->select('messages.id, messages.title, messages.created_at, users.username as sent_to_username, users.fullname as sent_to_fullname');
        $this->db->from('users');
        $this->db->where('sender_id', $user_id);
        $this->db->where('is_deleted_by_sender', 0);
        $this->db->order_by('created_at', 'desc');
        $this->db->limit($limit, $offset);
	
			// User doesn't match, set error message and present login page again
			if ($this->input->post('username') != $valid_login['username'] || $this->input->post('password') != $valid_login['password']) {
				$this->session->set_flashdata('login_error', 'Invalid login information. Please try again.');
			}else {
				$this->session->set_userdata('logged_in', TRUE);
				
				redirect('/backend');
			}
	}
	
	//log the user out
	function logout()
	{
		$this->data['title'] = "Logout";

		//log the user out
		$logout = $this->ion_auth->logout();

		//redirect them back to the page they came from
		redirect('', 'refresh');
	}

	//change password
	function change_password()
	{
		$this->form_validation->set_rules('old', 'Old password', 'required');
		$this->form_validation->set_rules('new', 'New Password', 'required|min_length[' . $this->config->item('min_password_length', 'ion_auth') . ']|max_length[' . $this->config->item('max_password_length', 'ion_auth') . ']|matches[new_confirm]');
		$this->form_validation->set_rules('new_confirm', 'Confirm New Password', 'required');

		if (!$this->ion_auth->logged_in())
		{
			redirect('auth/login', 'refresh');
		}

		$user = $this->ion_auth->user()->row();

		if ($this->form_validation->run() == false)
		{ //display the form
			//set the flash data error message if there is one
			$this->data['message'] = (validation_errors()) ? validation_errors() : $this->session->flashdata('message');

			$this->data['min_password_length'] = $this->config->item('min_password_length', 'ion_auth');
			$this->data['old_password'] = array(
				'name' => 'old',
				'id'   => 'old',
				'type' => 'password',
			);
			$this->data['new_password'] = array(
				'name' => 'new',
				'id'   => 'new',
				'type' => 'password',
				'pattern' => '^.{'.$this->data['min_password_length'].'}.*$',
			);
			$this->data['new_password_confirm'] = array(
				'name' => 'new_confirm',
				'id'   => 'new_confirm',
				'type' => 'password',
				'pattern' => '^.{'.$this->data['min_password_length'].'}.*$',
			);
			$this->data['user_id'] = array(
				'name'  => 'user_id',
				'id'    => 'user_id',
				'type'  => 'hidden',
				'value' => $user->id,
			);

			//render
			//$this->load->view('auth/change_password', $this->data);
			
			$this->data['content']=$this->load->view('users/change_password',$this->data,true);
			$this->load->view('layout/index',$this->data);
			
		}
		else
		{
			$identity = $this->session->userdata($this->config->item('identity', 'ion_auth'));

			$change = $this->ion_auth->change_password($identity, $this->input->post('old'), $this->input->post('new'));

			if ($change)
			{ //if the password was successfully changed
				$this->session->set_flashdata('message', $this->ion_auth->messages());
				redirect('contact', 'refresh');
				//$this->logout();
			}
			else
			{
				$this->session->set_flashdata('message', $this->ion_auth->errors());
				redirect('auth/change_password', 'refresh');
			}
		}
	}

}