$('#encrypted_content').text(CryptoJS.AES.decrypt($('#encrypted_content').text(), "My Secret Passphrase").toString(CryptoJS.enc.Utf8));
