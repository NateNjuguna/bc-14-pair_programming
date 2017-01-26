'use strict';

var elements = {
    email: document.getElementsByName('email')[0] || null,
    errorMessage: document.getElementById('error_messages') || null,
    raw_password: document.getElementById('raw_password') || null,
    repeat_password: document.getElementById('repeat_password') || null,
    password: document.getElementsByName('password')[0] || null,
    submit: document.getElementsByName('submit')[0] || null
};

var codeKS = {
    checkErrors: function() {
        if(elements.errorMessage.innerHTML.indexOf('<ul></ul>') > -1) {
            elements.errorMessage.style = 'display:none;';
        }else {
            elements.errorMessage.style = '';
        }
    },
    checkPasswordMatch: function(self) {
        if(elements.raw_password.value !== self.value) {
            elements.submit.style = 'opacity:0.5;z-index:-5;';
            elements.submit.type = 'button';
            elements.errorMessage.innerHTML = elements.errorMessage.innerHTML.replace('l><', 'l><li>Passwords do not Match</li><');
        }else {
            elements.submit.style = '';
            elements.submit.type = 'submit';
            elements.errorMessage.innerHTML = elements.errorMessage.innerHTML.replace('<li>Passwords do not Match</li>', '');
        }
        this.checkErrors();
    },
    encodePassword: function(self) {
        elements.password.value = btoa(self.value);
    },
    validateEmail: function(self){
        this.validateHasNoSpace(self, 'Email');
        if(self.value.split('@').length !== 2 || self.value.indexOf('.') < 1 || self.value[self.value.length - 1] !== '.') {
            self.focus();
            elements.errorMessage.innerHTML = elements.errorMessage.innerHTML.replace('l><', 'l><li>Email provided is invalid</li><');
        }else {
            elements.errorMessage.innerHTML = elements.errorMessage.innerHTML.replace('<li>Email provided is invalid</li>', '');
        }
        this.checkErrors();
    },
    validateHasNoSpace: function(self, type) {
        if(!type) type = 'Name';
        if(self.value.indexOf(' ') > -1) {
            self.focus();
            elements.errorMessage.innerHTML = elements.errorMessage.innerHTML.replace('l><', 'l><li>' + type + ' cannot contain a space</li><');
        }else {
            elements.errorMessage.innerHTML = elements.errorMessage.innerHTML.replace('<li>' + type + ' cannot contain a space</li>', '');
        }
        this.checkErrors();
    }
};
