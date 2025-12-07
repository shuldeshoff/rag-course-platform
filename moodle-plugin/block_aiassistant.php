<?php
defined('MOODLE_INTERNAL') || die();

class block_aiassistant extends block_base {
    
    public function init() {
        $this->title = get_string('pluginname', 'block_aiassistant');
    }
    
    public function get_content() {
        global $COURSE, $USER, $PAGE;
        
        if ($this->content !== null) {
            return $this->content;
        }
        
        $this->content = new stdClass();
        
        // Check if RAG service is configured
        $service_url = get_config('block_aiassistant', 'service_url');
        $api_token = get_config('block_aiassistant', 'api_token');
        
        if (empty($service_url) || empty($api_token)) {
            $this->content->text = get_string('notconfigured', 'block_aiassistant');
            return $this->content;
        }
        
        // Load JavaScript module
        $PAGE->requires->js_call_amd('block_aiassistant/chat', 'init', [
            'courseid' => $COURSE->id,
            'userid' => $USER->id
        ]);
        
        // Render template
        $renderer = $PAGE->get_renderer('block_aiassistant');
        $this->content->text = $renderer->render_chat_interface($COURSE->id);
        
        return $this->content;
    }
    
    public function applicable_formats() {
        return [
            'course-view' => true,
            'site' => false,
            'mod' => false,
            'my' => false
        ];
    }
    
    public function has_config() {
        return true;
    }
}

