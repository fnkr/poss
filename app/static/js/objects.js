$.fn.selectRange = function(start, end) {
    if(!end) end = start;
    return this.each(function() {
        if (this.setSelectionRange) {
            this.focus();
            this.setSelectionRange(start, end);
        } else if (this.createTextRange) {
            var range = this.createTextRange();
            range.collapse(true);
            range.moveEnd('character', end);
            range.moveStart('character', start);
            range.select();
        }
    });
};

window.term = $('#term');
term.focus();
term.selectRange(term.val().length);

window.add_term = function(new_term, select_start, select_stop) {
    if(select_start === undefined) select_start = 1;
    if(select_stop === undefined) select_stop = select_start;

    pre = term.val() === '' ? '' : ' ';
    post = select_start == 1 ? ' ' : '';
    if(term.val().slice(-1) != ' ') term.val(term.val() + pre);

    start = term.val().length;

    term.val(term.val() + new_term);

    term.val(term.val() + post);

    term.selectRange(start + new_term.length + select_start,
                     start + new_term.length + select_stop);
};

$('.btn-delete').click(function(e) {
    if (!confirm('Do you realy want to delete this item?')) {
        e.preventDefault();
    }
});

$('#filter_str').click(function() {
    add_term('""', -1);
});
$('#filter_views').click(function() {
    add_term('views:<0', -2, 0);
});

$('#order_created').click(function() {
    add_term('by:created');
});
$('#order_modified').click(function() {
    add_term('by:modified');
});
$('#order_views').click(function() {
    add_term('by:views');
});
$('#order_lastview').click(function() {
    add_term('by:lastviewed');
});
$('#order_size').click(function() {
    add_term('by:size');
});

$('#is_file').click(function() {
    add_term('is:file');
});
$('#is_link').click(function() {
    add_term('is:link');
});
$('#is_deleted').click(function() {
    add_term('is:deleted');
});
$('#is_notdeleted').click(function() {
    add_term('is:deleted:no');
});
