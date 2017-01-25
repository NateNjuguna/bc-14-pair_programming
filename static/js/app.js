'use strict';

var codeKS = {
    encodePassword: function() {
        document.getElementsByName('password')[0].value = btoa(document.getElementsByName('raw_password')[0].value);
    }
};
