<?php
defined('MOODLE_INTERNAL') || die();

if ($ADMIN->fulltree) {
    
    // Service URL
    $settings->add(new admin_setting_configtext(
        'block_aiassistant/service_url',
        get_string('serviceurl', 'block_aiassistant'),
        get_string('serviceurl_desc', 'block_aiassistant'),
        'http://localhost:8000',
        PARAM_URL
    ));
    
    // API Token
    $settings->add(new admin_setting_configpasswordunmask(
        'block_aiassistant/api_token',
        get_string('apitoken', 'block_aiassistant'),
        get_string('apitoken_desc', 'block_aiassistant'),
        ''
    ));
    
    // Request timeout
    $settings->add(new admin_setting_configtext(
        'block_aiassistant/timeout',
        get_string('timeout', 'block_aiassistant'),
        get_string('timeout_desc', 'block_aiassistant'),
        '10',
        PARAM_INT
    ));
    
    // Enable logging
    $settings->add(new admin_setting_configcheckbox(
        'block_aiassistant/enablelogging',
        get_string('enablelogging', 'block_aiassistant'),
        get_string('enablelogging_desc', 'block_aiassistant'),
        '1'
    ));
    
    // Max question length
    $settings->add(new admin_setting_configtext(
        'block_aiassistant/maxquestionlength',
        get_string('maxquestionlength', 'block_aiassistant'),
        get_string('maxquestionlength_desc', 'block_aiassistant'),
        '500',
        PARAM_INT
    ));
}

