<?php
namespace block_aiassistant;

defined('MOODLE_INTERNAL') || die();

class api_client {
    
    private $service_url;
    private $api_token;
    private $timeout;
    
    public function __construct() {
        $this->service_url = get_config('block_aiassistant', 'service_url');
        $this->api_token = get_config('block_aiassistant', 'api_token');
        $this->timeout = get_config('block_aiassistant', 'timeout') ?: 10;
    }
    
    public function ask_question($userid, $courseid, $question) {
        $url = rtrim($this->service_url, '/') . '/ask';
        
        $data = [
            'user_id' => (int)$userid,
            'course_id' => (int)$courseid,
            'question' => $question
        ];
        
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_TIMEOUT, $this->timeout);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $this->api_token
        ]);
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        if ($error) {
            throw new \moodle_exception('connectionerror', 'block_aiassistant', '', $error);
        }
        
        if ($http_code !== 200) {
            throw new \moodle_exception('serviceerror', 'block_aiassistant', '', $http_code);
        }
        
        $result = json_decode($response, true);
        
        if (!$result || !isset($result['status'])) {
            throw new \moodle_exception('invalidresponse', 'block_aiassistant');
        }
        
        if ($result['status'] !== 'success') {
            throw new \moodle_exception('serviceunavailable', 'block_aiassistant');
        }
        
        return $result;
    }
}

