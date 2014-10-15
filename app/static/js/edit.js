$('.btn-delete').click(function(e) {
    if (!confirm('Do you realy want to delete this item?')) {
        e.preventDefault();
    }
});

$('.select-on-click').click(function(e) {
    e.target.select();
});
