<?php
require_once(__DIR__ . '/../../config.php');

$courseid = required_param('courseid', PARAM_INT);
$question = required_param('question', PARAM_TEXT);

require_login($courseid);
require_sesskey();

$context = context_course::instance($courseid);
require_capability('block/aiassistant:askquestion', $context);

header('Content-Type: application/json');

try {
    global $USER, $DB;
    
    // Validate question length
    $maxlength = get_config('block_aiassistant', 'maxquestionlength') ?: 500;
    if (strlen($question) > $maxlength) {
        throw new moodle_exception('questiontoolong', 'block_aiassistant', '', $maxlength);
    }
    
    // Call RAG service
    $client = new \block_aiassistant\api_client();
    $result = $client->ask_question($USER->id, $courseid, $question);
    
    // Log if enabled
    if (get_config('block_aiassistant', 'enablelogging')) {
        $log = new stdClass();
        $log->userid = $USER->id;
        $log->courseid = $courseid;
        $log->question = $question;
        $log->answer = $result['answer'];
        $log->responsetime = $result['response_time_ms'] ?? 0;
        $log->status = 'success';
        $log->timecreated = time();
        $DB->insert_record('block_aiassistant_logs', $log);
    }
    
    echo json_encode($result);
    
} catch (Exception $e) {
    // Log error
    if (get_config('block_aiassistant', 'enablelogging')) {
        $log = new stdClass();
        $log->userid = $USER->id;
        $log->courseid = $courseid;
        $log->question = $question;
        $log->status = 'error';
        $log->errormessage = $e->getMessage();
        $log->timecreated = time();
        $DB->insert_record('block_aiassistant_logs', $log);
    }
    
    echo json_encode([
        'status' => 'error',
        'error' => get_string('serviceunavailable', 'block_aiassistant')
    ]);
}

