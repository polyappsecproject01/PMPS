<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
include_once('my_controller.php');
class contact extends My_controller {

	/**
	 * Index Page for this controller.
	 *
	 * Maps to the following URL
	 * 		http://example.com/index.php/welcome
	 *	- or -  
	 * 		http://example.com/index.php/welcome/index
	 *	- or -
	 * Since this controller is set as the default controller in 
	 * config/routes.php, it's displayed at http://example.com/
	 *
	 * So any other public methods not prefixed with an underscore will
	 * map to /index.php/welcome/<method_name>
	 * @see http://codeigniter.com/user_guide/general/urls.html
	 */
	function __construct()
	{ 
		parent::__construct();
		$this->load->library('upload');
		$this->load->library('ion_auth');
		$this->load->helper('form');
		$this->load->helper('url');
		$this->load->model('contact_model');
        $this->load->helper('common');
		//if(!$this->session->userdata('id')) redirect('');
	}
	public function index()
	{
		$info['group_id'] = $this->uri->segment(3);
		if ($info['group_id'] == 0) {
            $info['query'] = $this->contact_model->get_all_contacts1(5000, 0);
            $info['query1'] = $this->contact_model->get_all_contacts2(5000,0);
		} else {
            $info['query'] = $this->contact_model->get_contacts_in_group($info['group_id'], $this->session->userdata['user_id']);
            $info['query1'] = array();
		}
		
		
		$user = $this->ion_auth->user()->row();
		$user_id=$user->id;
		$e_profile=$this->contact_model->e_profile($user_id, 'users');
		if($e_profile== true){
			redirect('contact/set_profile');
		} 	
		$info['personal_info'] = $this->contact_model->get_personal_info($user_id,'users');
		$info['personal_info1'] = $this->contact_model->get_personal_user_group_info($user_id , 'profile_users_group_info');
		$info['personal_info2'] = $this->contact_model->get_personal_friends_group_info($user_id , 'profile_users_group');
        $this->load->model('user_model');
        $info['user_groups'] = $this->contact_model->get_all_user_groups($user_id);
		$this->data['content']=$this->load->view('contact/home',$info,true);
		$this->load->view('layout/index',$this->data);

	}
	public function set_profile()
	{
		$user = $this->ion_auth->user()->row();
		$user_id=$user->id;
		$user_data['user_data'] = $this->contact_model->get_user_data($user_id);
		$user_data['languages']=$this->menu_model->get_languages();
        $this->load->model('countries_model');
        $user_data['countries'] = $this->countries_model->get_all();
		$this->data['content']=$this->load->view('contact/set_profile',$user_data,true);
		$this->load->view('layout/index',$this->data);
	}
	public function edit_profile()
	{
		$user = $this->ion_auth->user()->row();
		$user_id=$user->id;
		$user_data['user_data'] = $this->contact_model->get_user_data($user_id);
		$user_data['languages']=$this->menu_model->get_languages();
        $user_data['countries'] = $this->countries_model->get_all();
        $this->data['content']=$this->load->view('contact/edit_profile',$user_data,true);
		//$data['content']= "Set profile please";
		$this->load->view('layout/index',$this->data);
	}
	public function update_profile()
	{
		//print_r($_POST);die;
		if(isset($_FILES['image_path']['name']) && !empty($_FILES['image_path']['name'])){
			$config['upload_path'] = './public/users/profile_pic/';
			$config['allowed_types'] = 'gif|jpg|png';
			$config['overwrite']	= FALSE;
			$config['max_size']	= '100000';

			$this->load->library('upload', $config);
			$this->upload->initialize($config);
			if ( ! $this->upload->do_upload('image_path'))
			{
				$this->session->set_userdata('error_message',$this->upload->display_errors());
				//echo $this->upload->display_errors();
				$this->session->set_userdata('user_data',$_POST);
				redirect('contact/edit_profile');
			}
			else
			{
				$data =  $this->upload->data();
			//print_r($data['file_name']);
			//die;
				$_POST['image_path']='public/users/profile_pic/'.$data['file_name'];
			}
        } //else echo "Wrong try <br/>";
		
		//print_r($_POST);die;
		if(!empty($_POST['image_path'])){
			$language_ids='';
		    if($this->input->post('language'))
			{
				$language_ids=implode(',',$this->input->post('language'));
			}
			$fields = array(
				 'fullname'     => $this->input->post('fullname'),
				 'email'     => $this->input->post('email'),
				 'phone'     => $this->input->post('phone'),
				 'gender'     => $this->input->post('gender'),
				 'date_of_birth'     => $this->input->post('date_of_birth'),
				 'date2'     => $this->input->post('date2'),
				 'date3'     => $this->input->post('date3'),
				 'date_of_birth'     => $this->input->post('date_of_birth'),
				 'country_id'     => $this->input->post('country_id'),
				 'zip_code'     => $this->input->post('zip_code'),
				 'language_ids'     => $language_ids,
				 'image_path'     =>  $_POST['image_path'],
				 'about'     =>  $_POST['about'],
                 'profile_is_set' => 1
			);
		} else {
			$language_ids='';
		    if($this->input->post('language'))
			{
				$language_ids=implode(',',$this->input->post('language'));
			}
			$fields = array(
				 'fullname'     => $this->input->post('fullname'),
				 'email'     => $this->input->post('email'),
				 'phone'     => $this->input->post('phone'),
				 'gender'     => $this->input->post('gender'),
				 'date_of_birth'     => $this->input->post('date_of_birth'),
				 'date2'     => $this->input->post('date2'),
				 'date3'     => $this->input->post('date3'),
				 'country_id'     => $this->input->post('country_id'),
				 'zip_code'     => $this->input->post('zip_code'),
				 'language_ids'     => $language_ids,
				 'about'     =>  $_POST['about'],
                 'profile_is_set' => 1
			);
		}
		//print_r($_POST);die;
		$user = $this->ion_auth->user()->row();
		
		$where=$user->id;
		$query 	= $this->contact_model->update_profile('users', $fields, $where);
		if($query){
			$this->session->set_userdata('success_message', $this->lang->line('Successfuly_updated'));
			redirect('messages');
		}else{
                $this->session->set_userdata('error_message', $this->lang->line('Data_insert_error!'));
                $this->session->set_userdata('user_data',$_POST);
                redirect('contact/edit_profile');
        }
		
	}
	
	public function all_contacts()
	{
		$this->load->library('pagination');
		$config['base_url'] = base_url().'contact/all_contacts/';
		$totalr=$this->contact_model->get_all_contacts_count1() + $this->contact_model->get_all_contacts_count2();
		$config['total_rows'] = $totalr;
		$config['per_page'] = '16';
		$config['full_tag_open'] = '<span class="alert alert-info">';
		$config['full_tag_close'] = '</span>';
		$config['uri_segment'] = 3;  
		$this->pagination->initialize($config);
		
		//load the model and get results
		$query['query'] = $this->contact_model->get_all_contacts1($config['per_page']/2,$this->uri->segment(3));
		$query['query1'] = $this->contact_model->get_all_contacts2($config['per_page']/2,$this->uri->segment(3));
				
		$this->data['content']=$this->load->view('contact/all_contacts',$query,true);
		$this->load->view('layout/index',$this->data);
	}
	
	public function contact_search()
	{
		$this->load->library('pagination');
		$config['base_url'] = base_url().'contact/contact_search/';
		$config['total_rows'] = $this->contact_model->get_contact_search_count();
		$config['per_page'] = '16';
		$config['full_tag_open'] = '<span class="alert alert-info">';
		$config['full_tag_close'] = '</span>';
		$config['uri_segment'] = 3;  
		$this->pagination->initialize($config);
		
		//load the model and get results
		$query['query'] = $this->contact_model->get_contact_search($config['per_page'],$this->uri->segment(3));
		$query['fr_q'] = $this->contact_model->get_all_friends_count();
		$this->data['content']=$this->load->view('contact/contact_search',$query,true);
		$this->load->view('layout/index',$this->data);
	}
	
	public function add_group()
	{	
		$segment3=$this->uri->segment(3);
		$segment4=$this->uri->segment(4);
		if($segment3=='action-delete'){
			if(is_numeric($segment4)){
				$truefolse=$this->contact_model->delete_group('profile_users_group_info' , $this->uri->segment(4));
				if($truefolse)
				$this->session->set_userdata('success_message', $this->lang->line('Successfuly_deleted'));
				else$this->session->set_userdata('success_message', $this->lang->line('Something_is_wrong!'));
			}
		}
		//die;
		if($_POST['group_name']!=''){
			$query=$this->db->insert('profile_users_group_info' , $_POST);
			
			if($query){
				$this->session->set_userdata('success_message', $this->lang->line('Successfuly_Created'));
				redirect('contact');
			}else{
					$this->session->set_userdata('error_message', $this->lang->line('Data_insert_error!'));
					redirect('contact');
			}
		}redirect('contact');
	}
	public function send_friend_req($obj_id,$key)
	{
		$user = $this->ion_auth->user()->row();
		$fields=array(
				'id'		 =>  '',
				'key'	 	 =>  $key,
				'sub_id'	 =>  $user->id,
				'obj_id'	 =>  $obj_id,
				'status'	 =>  '0'
		);
		$query=$this->db->insert('profile_users_friend' , $fields);
		$notification=array(
			'id' => '',
			'user_id' => $obj_id,
			'desc' => $user->username . $this->lang->line('contact_sent_request'),
			'time' => time(),
			'custom' => 'pending_request'
		);
		$info = $this->db->insert('profile_notification', $notification);

		if($query){
			$this->session->set_userdata('success_message', 'Request successfully sent');
			redirect('contact/contact_search');
		}else{
			$this->session->set_userdata('error_message', 'Opps! request didnt sent...');
			redirect('contact/contact_search');
		}

		//$this->load->view('layout/index',$data);
	}
	public function add_friends_group()
	{
		
		$segment3=$this->uri->segment(3);
		$segment4=$this->uri->segment(4);
		if($segment3=='action-deletex'){
			if(is_numeric($segment4)){
				$truefolse=$this->contact_model->delete_friends_group('profile_users_group' , $this->uri->segment(4));
				if($truefolse)
				$this->session->set_userdata('success_message', $this->lang->line('Successfuly_deleted'));
				else$this->session->set_userdata('success_message', $this->lang->line('Something_is_wrong!'));
				redirect('contact');
			}
		}
	
		
		$user = $this->ion_auth->user()->row(); $u=$user->id;
		$fields=array(
			'id' => '',
			'sub_id' => $u,
			'obj_id' => $this->input->post('obj_id'),
			'gr_id' => $this->input->post('gr_name')
		);
		//print_r($fields);die;
		$query = $this->db->insert('profile_users_group', $fields);
		if($query){
			$this->session->set_userdata('success_message', 'Contact added to the group!');
			redirect('contact');
		}else{
			$this->session->set_userdata('error_message', 'Opps! request didnt sent...');
			redirect('contact');
		}
		
	}
	
	public function pending_request()
	{
		$this->load->library('pagination');
		$config['base_url'] = base_url().'contact/pending_request/';
		$config['total_rows'] = $this->contact_model->get_pending_request_count();
		$config['per_page'] = '16';
		$config['full_tag_open'] = '<span class="alert alert-info">';
		$config['full_tag_close'] = '</span>';
		$config['uri_segment'] = 3;  
		$this->pagination->initialize($config);
		
		$user = $this->ion_auth->user()->row();
		$user_id=$user->id;
		$info['pending_request']=$this->contact_model->pending_request($config['per_page'],$this->uri->segment(3));
		
		$this->data['content']=$this->load->view('contact/pending_request', $info , true);
		
		$this->load->view('layout/index',$this->data);
	}
	
	public function pending_approval()
	{
		$this->load->library('pagination');
		$config['base_url'] = base_url().'contact/pending_request/';
		$config['total_rows'] = $this->contact_model->get_pending_approval_count();
		$config['per_page'] = '16';
		$config['full_tag_open'] = '<span class="alert alert-info">';
		$config['full_tag_close'] = '</span>';
		$config['uri_segment'] = 3;  
		$this->pagination->initialize($config);
		
		$user = $this->ion_auth->user()->row();
		$user_id=$user->id;
		$info['pending_request']=$this->contact_model->pending_approval($config['per_page'],$this->uri->segment(3));
		
		$this->data['content']=$this->load->view('contact/pending_approval', $info , true);
		
		$this->load->view('layout/index',$this->data);
	}
	
	public function send_message(){
	
		$this->data['content']= "please set message system <br> " . anchor('contact' , 'back to the main');
		
		$this->load->view('layout/index',$this->data);
	
	}
	
	public function cancell_request($id)
	{
		//print_r($_POST);die;
		$this->db->where('id', $id);
		$query=$this->db->delete('profile_users_friend');
		if($query){
			$this->session->set_userdata('success_message', 'Successfuly Cancelled');
			redirect('contact/contact_search');
		}else{
                $this->session->set_userdata('error_message', 'Sorry! something wrong...');
                redirect('contact/contact_search');
        }
	}
	public function remove_contacts($id)
	{
		$this->db->where('id' , $id);
        $query = $this->db->delete('profile_users_friend');
		if($query){
			$this->session->set_userdata('success_message', 'Successfuly removed from contact');
			redirect('contact/contact_search');
		}else{
                $this->session->set_userdata('error_message', 'Sorry! something wrong...');
                redirect('contact/contact_search');
        }
	}
	public function accept_req($id, $user)
	{
		$users = $this->ion_auth->user()->row();
		$user_name=$users->username;
		$fields=array(
			'status' => '1',
			'time' => time()
		);
		$this->db->where('id' , $id);
        $update = $this->db->update('profile_users_friend', $fields);
		$notification=array(
			'id' => '',
			'user_id' => $user,
			'desc' => $user_name ." ". $this->lang->line('contact_accepted request'),
			'time' => time()
		);
		$info = $this->db->insert('profile_notification', $notification);
		if($update and $info){
			//$this->session->set_userdata('success_message', 'Successfuly you accepted the request');
			redirect('contact/contact_search');
		}else{
                $this->session->set_userdata('error_message', 'Sorry! something wrong...');
                redirect('contact/contact_search');
        }
	}
	
	public function success()
	{
		$this->data['content']=$this->lang->line('update_successful');
		$this->load->view('layout/index',$this->data);
	}
}

/* End of file welcome.php */
/* Location: ./application/controllers/welcome.php */