$(document).ready(function() {
    if (window.location.hash === '') {
        window.location.hash = localStorage.getItem('poss.key');
        localStorage.setItem('poss.key', '');
    }
    $('#encrypted_content').text(CryptoJS.AES.decrypt($('#encrypted_content').text(), window.location.hash.substring(1)).toString(CryptoJS.enc.Utf8));
});
