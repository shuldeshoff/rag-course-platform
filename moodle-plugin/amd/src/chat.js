define(['jquery', 'core/ajax', 'core/notification'], function($, ajax, notification) {
    
    return {
        init: function(params) {
            var courseid = params.courseid;
            var userid = params.userid;
            
            var questionInput = $('#aiassistant-question-' + courseid);
            var submitBtn = $('#aiassistant-submit-' + courseid);
            var answerArea = $('#aiassistant-answer-' + courseid);
            var loadingArea = $('#aiassistant-loading-' + courseid);
            var errorArea = $('#aiassistant-error-' + courseid);
            
            submitBtn.on('click', function() {
                var question = questionInput.val().trim();
                
                if (!question) {
                    return;
                }
                
                // Show loading
                answerArea.hide();
                errorArea.hide();
                loadingArea.show();
                submitBtn.prop('disabled', true);
                
                // Call AJAX
                ajax.call([{
                    methodname: 'block_aiassistant_ask_question',
                    args: {
                        courseid: courseid,
                        question: question
                    },
                    done: function(response) {
                        loadingArea.hide();
                        submitBtn.prop('disabled', false);
                        
                        if (response.status === 'success') {
                            answerArea.find('.answer-content').html(
                                '<p>' + response.answer.replace(/\n/g, '<br>') + '</p>'
                            );
                            answerArea.show();
                            
                            // Show chunks if available
                            if (response.chunks_used && response.chunks_used.length > 0) {
                                var chunksHtml = '<div class="chunks-info"><small><em>Источники: ';
                                response.chunks_used.forEach(function(chunk, index) {
                                    if (index > 0) chunksHtml += ', ';
                                    chunksHtml += chunk.source;
                                });
                                chunksHtml += '</em></small></div>';
                                answerArea.find('.answer-content').append(chunksHtml);
                            }
                        } else {
                            showError('Ошибка: ' + (response.error || 'Неизвестная ошибка'));
                        }
                    },
                    fail: function(error) {
                        loadingArea.hide();
                        submitBtn.prop('disabled', false);
                        showError('Сервис временно недоступен. Попробуйте позже.');
                    }
                }]);
            });
            
            // Submit on Enter (Ctrl+Enter)
            questionInput.on('keydown', function(e) {
                if (e.key === 'Enter' && e.ctrlKey) {
                    submitBtn.click();
                }
            });
            
            function showError(message) {
                errorArea.find('.alert').text(message);
                errorArea.show();
            }
        }
    };
});

