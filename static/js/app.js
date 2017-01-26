'use strict';

var codeKS = {
    encodePassword: function() {
        document.getElementsByName('password')[0].value = btoa(document.getElementById('raw_password').value);
    }
};
