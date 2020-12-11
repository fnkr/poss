function updateQueryStringParameter(uri, key, value) {
    var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
    var separator = uri.indexOf('?') !== -1 ? "&" : "?";
    if (uri.match(re)) {
        return uri.replace(re, '$1' + key + "=" + value + '$2');
    }
    else {
        return uri + separator + key + "=" + value;
    }
}

function updateURL(url) {
    window.history.pushState(null, document.title, url);
}

$('pre>span').click(function(event) {
   $(event.target).toggleClass('hll');
    window.H_IDs = [];
    $('pre>span.hll').each(function(_, element) {
        H_IDs.push($(element).attr('id').split('-')[1]);
    });
    updateURL(updateQueryStringParameter(window.location.href, 'H', H_IDs.join(',')));
});

$('.hll').parent().each(function(_, element) {
    $(element).addClass('hll');
});

window.onpopstate = function() {
    window.location.reload();
};

window.poss_decrypt = function (key, data) {
    return atob(data);
}
