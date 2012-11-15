<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
include_once('my_controller.php');
class Users extends My_controller {

	function __construct()
	{ 
		parent::__construct();
		$this->load->model('user_model');
		$this->load->library('session');
		$this->load->library('ion_auth');
        $this->load->helper('common');
	}
	public function index()
	{
		if(!$this->session->userdata('user_id')) 
            redirect('');
		$data_m['message'] =  $this->session->flashdata('message');
        
        $page = $this->uri->segment(3);
        $items_per_page = 10;
        
        if ($page == null)
            $page = 1;
            
        //paginate results
        $this->load->library('pagination');
        $config['base_url'] = base_url() . 'users/index';
        $config['total_rows'] = $this->notifications_model->count_notifications($this->session->userdata['user_id']);
        $config['per_page'] = $items_per_page;
        $config['first_link'] = $this->lang->line('m_first_link');
        $config['last_link'] = $this->lang->line('m_last_link');
        $config['use_page_numbers'] = TRUE;
        $this->pagination->initialize($config);
        $data_m['pagination'] = $this->pagination->create_links();
        
        //get results
        $offset = ($page-1) * $items_per_page;
        
		$data_m['notifications'] = $this->notifications_model->get_processed_notifications($this->session->userdata['user_id'], $items_per_page, $offset);
		$this->data['content']=$this->load->view('users/home',$data_m,true);
		$this->load->view('layout/index',$this->data);

	}
	
	public function register()
	{
	   $user = array();
       $errors = array();
        if ($this->input->post('sign_up')) {
            
            $this->load->helper('email');
            $user['email'] = trim($this->input->post('email'));
    		$user['username'] = trim($this->input->post('username'));
    		$user['password'] = trim($this->input->post('password'));
    		$user['created_on'] = time();
            
            if (!valid_email($this->input->post('email')))
                $errors['email'][] = 'Invalid email';

            if ($this->user_model->is_email_already_used($user['email']))
                $errors['email'][] = 'Email is already used';
                
            if (empty($user['username']))
                $errors['username'][] = 'Username is required';
                 
            if ($this->user_model->is_username_already_used($user['username']))
                $errors['username'][] = 'Username is not available';
            
            if (empty($user['password']))
                $errors['password'][] = 'Password is required';
            
            if (empty($errors)) {
                $user['password'] = md5($user['password']);
                $user_id = $this->user_model->sign_up_user($user);
                $user_row = $this->user_model->get_user_info($user_id);
                $this->session->set_userdata('identity', $user_row->username);
                $this->session->set_userdata('username', $user_row->username);
                $this->session->set_userdata('email', $user_row->email);
                $this->session->set_userdata('user_id', $user_row->id);
                redirect('dashboard');
            }
        }
        $data['user'] = $user;
        $data['errors'] = $errors;
        $this->data['content'] = $this->load->view('home', $data, true);
        $this->load->view('layout/index', $this->data);
	}
	function success()
	{
		$this->data['content']=$this->load->view('users/success','',true);
		$this->load->view('layout/index',$this->data);
	}
	function login()
	{
		if($this->input->post('sbt'))
		{
			if($this->user_model->login())
			{
				redirect('dashboard');
			}
			else
			{
				$db_data['erros_message']= $this->lang->line('log_in_form');
				$data['content']=$this->load->view('users/login',$db_data,true);
				$this->load->view('layout/index',$data);
			}
			
			
		}
		else
		{
			$db_data['erros_message']="";
			$this->data['content']=$this->load->view('users/login',$db_data,true);
			$this->load->view('layout/index',$this->data);
		}
	}
	function logout()
	{
		$site_language=$this->session->userdata('site_language');
		$this->session->sess_destroy();
		//$this->session->set_userdata('site_language',$site_language);
		redirect('');
	}
    
    public function contact_us()
    {   
        $data = array();
        if ($this->input->post('submit')) {
            $data['errors'] = array();
            
            $data['user_message'] = $this->input->post('user_message');
            
            $data['user_message']['name'] = trim($data['user_message']['name']);
            $data['user_message']['email'] = trim($data['user_message']['email']);
            $data['user_message']['message'] = trim($data['user_message']['message']);
            
            if (empty($data['user_message']['name']))
                $data['errors']['name'] = 'This field is required';
            
            $this->load->helper('email');
            if (!valid_email($data['user_message']['email'])) 
                $data['errors']['email'] = 'Email is invalid';
            
            if (empty($data['user_message']['message']))
                $data['errors']['message'] = 'Please do not send an empty message';
            
            if (empty($data['errors'])) {
                $this->load->model('contact_us_model');
                $current_datetime = new \DateTime();
                $data['user_message']['created_at'] = $current_datetime->format('Y-m-d H:i:s');
                $this->contact_us_model->save($data['user_message']);
                redirect('dashboard');
            }
                
        }
        $this->data['content'] = $this->load->view('users/contact_us', $data, true);
        $this->load->view('layout/index', $this->data);
    }
    
    public function screenshots()
    {
        $this->data['content'] = $this->load->view('users/screenshots', array(), true);
        $this->load->view('layout/index', $this->data);
    }
    
    public function account()
    {
        $data['email'] = $this->user_model->get_email($this->session->userdata['user_id']);
        if ($this->input->post('submit')) {
            $this->load->helper('email');
            $email = $this->input->post('email');
            if (!valid_email($email)) {
                $data['message'] = 'Invalid email';
                $data['message_style_class'] = 'text-error';
            }
            else {
                if ($email != $data['email']) {
                    $data['message'] = 'Email successfully changed';
                    $data['message_style_class'] = 'text-success';
                    $data['email'] = $email;
                    $this->user_model->set_email($this->session->userdata['user_id'], $email);
                    $this->session->set_userdata('email', $email);
                }
            }
        } 
        $this->data['content'] = $this->load->view('users/account', $data, true);
        $this->load->view('layout/index', $this->data);
    } 
	public function change_password()
    {
        $data['email'] = $this->user_model->get_email($this->session->userdata['user_id']);
        if ($this->input->post('submit')) {
            $this->load->helper('email');
            $email = $this->input->post('email');
            if (!valid_email($email)) {
                $data['message'] = 'Invalid email';
                $data['message_style_class'] = 'text-error';
            }
            else {
                if ($email != $data['email']) {
                    $data['message'] = 'Email successfully changed';
                    $data['message_style_class'] = 'text-success';
                    $data['email'] = $email;
                    $this->user_model->set_email($this->session->userdata['user_id'], $email);
                    $this->session->set_userdata('email', $email);
                }
            }
        } 
        $this->data['content'] = $this->load->view('users/change_password', $data, true);
        $this->load->view('layout/index', $this->data);
    }
    
    public function dezactivate_account()
    {
        $this->user_model->dezactivate_account($this->session->userdata['user_id']);
        $this->session->sess_destroy();
        redirect('.');
    }
}