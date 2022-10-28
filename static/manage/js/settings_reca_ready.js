grecaptcha.ready(function() {
    var grecaptcha_execute = function() {
        grecaptcha.execute('6LdXNDsaAAAAAA7PYg1n8wj2vAoePky1si63XmrD', { action: 'settings' }).then(function(token) {
            document.querySelectorAll('input.django-recaptcha-hidden-field').forEach(function(value) {
                value.value = token;
            });
            return token;
        })
    };
    grecaptcha_execute()
    setInterval(grecaptcha_execute, 120000);
});