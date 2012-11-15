<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed'); 

class Zeromq {

	const 		REQ_TIMEOUT	= 2500; // Timeout length in milliseconds (ms)
	const 		REQ_RETRIES	= 3;	// Number of times to attempt to receive a message

	private 	$CI;
	private 	$host 		= 'localhost';
	private 	$port 		= 1390;
	private 	$mode 		= ZMQ::SOCKET_REQ;
	protected 	$conn 		= NULL;
	private 	$last_error = NULL;


    public function __construct($host = NULL, $port = NULL, $mode = NULL)
    {
		// Set ZMQ variables if parameters passed
		if ($host)
			$this->host = $host;
		if ($port)
			$this->port = $port;
		if ($this->is_valid_mode($mode))
			$this->mode = $mode;

		// Grab the CI object by reference, so we can work directly on the original copy if needed
		$this->CI = &get_instance();
	}

	private function connect()
	{
		// Initialize as empty to start fresh connection attempt
		$this->conn = NULL;

		// Initiate a new ZMQ connection, with the appropriate mode (subscribe, request, reply, etc.)
		$context = new ZMQContext();
		$this->conn = new ZMQSocket($context, $this->mode);
		$this->conn->connect("tcp://{$this->host}:{$this->port}");

		// Configure socket to not wait at close time
		$this->conn->setSockOpt(ZMQ::SOCKOPT_LINGER, 0);
	}

	public function server()
	{
		// Initialize as empty to start fresh connection attempt
		$this->conn = NULL;

		// Initiate a new ZMQ connection, with the appropriate mode (subscribe, request, reply, etc.)
		$context = new ZMQContext();
		$this->conn = new ZMQSocket($context, ZMQ::SOCKET_REP);
		$this->conn->bind("tcp://{$this->host}:{$this->port}");
	}

	public function send($data = NULL)
	{
		if (!$data) {
			$this->last_error = 'Invalid action. Cannot send empty data request.';
			return FALSE;
		}
		
		if (!$this->conn) {
			// Form 0MQ connection
			$this->connect();
		}

		// Set number of retries based on class constant, init blank response, and blank arrays for polling for responses
		$attempts = Zeromq::REQ_RETRIES;
		$response = NULL;
		$keep_polling = TRUE;
		$read = $write = array();

		// Send request
		$this->conn->send($data);

		// Attempt to get a reply
		while ($keep_polling) {
			// Poll socket for a reply, awaiting for class defined timeout period
			$poller = new ZMQPoll();
			$poller->add($this->conn, ZMQ::POLL_IN);
			$events = $poller->poll($read, $write, Zeromq::REQ_TIMEOUT);

			// Reply received, process it and break out of loop
			if ($events > 0) {
				$response = $this->conn->recv();
				$keep_polling = FALSE;
			} else {
				// No response received, decrement retry counter, and re-send request on newly opened socket
				$attempts--;

				if ($retries_left == 0) {
					// Reached retry limit, abandon attempts with error
					$this->last_error = sprintf("Could not communicate with server. Request abandoned after %d unsuccessful attempts.", Zeromq::REQ_RETRIES);
					$keep_polling = FALSE;
				} else {
					// Open new socket for new request attempt, send data
					$this->connect();
					$this->conn->send($data);
				}
			}
		}

		if ($response)
			return $response;
		else
			return FALSE;
	}

	public function get_last_error()
	{
		return $this->last_error;
	}

	private function is_valid_mode($mode = NULL)
	{
		// Only supporting a request/receive model for time being
		$valid_modes = array(
			ZMQ::SOCKET_REQ
		);

		// If mode is within the array of valid, supported modes, return boolean TRUE
		if (isset($mode) && in_array($mode, $valid_modes))
			return TRUE;
		else
			return FALSE;
	}

}