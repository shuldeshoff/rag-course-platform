<?php
namespace block_aiassistant\output;

defined('MOODLE_INTERNAL') || die();

class renderer extends \plugin_renderer_base {
    
    public function render_chat_interface($courseid) {
        $data = [
            'courseid' => $courseid,
            'placeholder' => get_string('questionplaceholder', 'block_aiassistant'),
            'submitlabel' => get_string('submitbutton', 'block_aiassistant'),
            'asklabel' => get_string('askquestion', 'block_aiassistant')
        ];
        
        return $this->render_from_template('block_aiassistant/chat_interface', $data);
    }
}

