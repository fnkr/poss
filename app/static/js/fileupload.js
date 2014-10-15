// Constants
// var MAX_UPLOAD_FILE_SIZE = 1024*1024*20; // 20 MB
var UPLOAD_URL = $('#upload-form').attr('action');
var $dropbox = $("#dropbox");

// List of pending files to handle when the Upload button is finally clicked.
var PENDING_FILES  = [];

$(document).ready(function() {
    // On drag enter...
    $dropbox.on("dragenter", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).addClass("active");
    });

    // On drag over...
    $dropbox.on("dragover", function(e) {
        e.stopPropagation();
        e.preventDefault();
    });

    // On drop...
    $dropbox.on("drop", function(e) {
        e.preventDefault();
        $(this).removeClass("active");

        // Get the files.
        var files = e.originalEvent.dataTransfer.files;
        handleFiles(files);

        // Update the display to acknowledge the number of pending files.
        updatePendingfilesText();
    });

    // If the files are dropped outside of the drop zone, the browser will
    // redirect to show the files in the window. To avoid that we can prevent
    // the 'drop' event on the document.
    function stopDefault(e) {
        e.stopPropagation();
        e.preventDefault();
    }
    $(document).on("dragenter", stopDefault);
    $(document).on("dragover", stopDefault);
    $(document).on("drop", stopDefault);

    $dropbox.click(function() {
        $("input[type='file']").trigger('click');
    });

    $('#file-picker').hide();

    // Set up the handler for the file input box.
    $("#file-picker").on("change", function() {
        handleFiles(this.files);
    });

    // Handle the submit button.
    $("#upload-button").on("click", function(e) {
        // If the user has JS disabled, none of this code is running but the
        // file multi-upload input box should still work. In this case they'll
        // just POST to the upload endpoint directly. However, with JS we'll do
        // the POST using ajax and then redirect them ourself when done.
        e.preventDefault();
        doUpload();
    })
});

function doUpload() {
    $("#progress").show();
    var $progressBar   = $("#progress-bar");

    // Gray out the form.
    $("#upload-form :input").attr("disabled", "disabled");

    // Initialize the progress bar.
    $progressBar.css({"width": "0%"});

    // Collect the form data.
    fd = collectFormData();

    // Attach the files.
    for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
        // Collect the other form data.
        fd.append("files[]", PENDING_FILES[i]);
    }

    // Inform the back-end that we're doing this over ajax.
    fd.append("__ajax", "true");

    var xhr = $.ajax({
        xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                xhrobj.upload.addEventListener("progress", function(event) {
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total    = event.total;
                    if (event.lengthComputable) {
                        percent = Math.ceil(position / total * 100);
                    }

                    // Set the progress bar.
                    $progressBar.css({"width": percent + "%"});
                    $progressBar.text(percent + "%");
                }, false)
            }
            return xhrobj;
        },
        url: UPLOAD_URL,
        method: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: fd,
        success: function(data) {
            $progressBar.css({"width": "100%"});
            data = JSON.parse(data);

            PENDING_FILES = [];
            $("#upload-form :input").removeAttr("disabled");
            $('#uploaded').show();
            updatePendingfilesText();

            for(var i = 0; i < data.length; i++) {
                if(data[i].error) {
                    // todo: handle error
                } else {
                    $('#files-table').append(
                        '<tr>'+
                        '  <td><a href="'+data[i].link+'" target="_blank">/'+data[i].oid+'</a></td>'+
                        '  <td>'+data[i]['input-name']+'</td>'+
                        '  <td>'+data[i].name+'</td>'+
                        '  <td>'+data[i].size+'</td>'+
                        '  <td>'+
                        '      <a href="/'+data[i].oid+'/stats" class="btn btn-default" target="_blank"><i class="icon-chart-bar"></i></a>'+
                        '      <a href="/'+data[i].oid+'/edit" class="btn btn-default" target="_blank"><i class="icon-edit"></i></a>'+
                        '      <a href="/'+data[i].oid+'/delete" class="btn btn-default btn-delete" target="_blank"><i class="icon-trash"></i></a>'+
                        '  </td>'+
                        '</tr>'
                    );
                }
            }

            $('.btn-delete').click(function(e) {
                if (!confirm('Do you realy want to delete this item?')) {
                    e.preventDefault();
                }
            });
        },
        error: function() {
            PENDING_FILES = [];
            $("#upload-form :input").removeAttr("disabled");
            updatePendingfilesText();
            alert('Upload failed.');
        }
    });
}

function updatePendingfilesText() {
    if(PENDING_FILES.length === 0) {
        $dropbox.text("Drag and Drop Files Here");
        $('#upload-button').attr('disabled', true);
    } else {
        PENDING_FILES_UL = "<ul>";
        for(var i = 0; i < PENDING_FILES.length; i++) {
            PENDING_FILES_UL += "<li>" + PENDING_FILES[i].name + "</li>";
        }
        PENDING_FILES_UL += '</ul>';

        $dropbox.html(PENDING_FILES_UL);

        $('#upload-button').attr('disabled', false);
    }
}

function collectFormData() {
    // Go through all the form fields and collect their names/values.
    var fd = new FormData();

    $("#upload-form :input").each(function() {
        var $this = $(this);
        var name  = $this.attr("name");
        var type  = $this.attr("type") || "";
        var value = $this.val();

        // No name = no care.
        if (name === undefined) {
            return;
        }

        // Skip the file upload box for now.
        if (type === "file") {
            return;
        }

        // Checkboxes? Only add their value if they're checked.
        if (type === "checkbox" || type === "radio") {
            if (!$this.is(":checked")) {
                return;
            }
        }

        fd.append(name, value);
    });

    return fd;
}

function handleFiles(files) {
    // Add them to the pending files list.
    for (var i = 0, ie = files.length; i < ie; i++) {
        PENDING_FILES.push(files[i]);
        updatePendingfilesText();
    }
}
