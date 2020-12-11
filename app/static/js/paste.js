$(document).ready(function() {
    var textarea = $('#paste-input-textarea').addClass("hidden");
    $('#paste-input-editor').removeClass("hidden");
    var editor = ace.edit("paste-input-editor");
    editor.getSession().setValue(textarea.val());
    editor.getSession().on('change', function(){
        textarea.val(editor.getSession().getValue());
    });
    editor.focus();

    // $('#expire_type').change(function() {
    //     type = $('#expire_type').val();
    //     if(type == 'view') {
    //         $('#expire_view').show();
    //         $('#expire_time').hide();
    //     } else if(type == 'time') {
    //         $('#expire_view').hide();
    //         $('#expire_time').show();
    //     } else {
    //         $('#expire_view').hide();
    //         $('#expire_time').hide();
    //     }
    // });

    window.poss_encrypt = function (key, data) {
        return btoa(data);
    }
});
