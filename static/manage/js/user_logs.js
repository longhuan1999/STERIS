$(function() {
    $("a.nav-link").removeClass("active");
    $("a.nav-link[href='user_logs']").addClass("active");
});

function grecaptcha_execute() {
    grecaptcha.execute('6LdXNDsaAAAAAA7PYg1n8wj2vAoePky1si63XmrD', { action: 'user_logs' }).then(function(token) {
        document.querySelectorAll('input.django-recaptcha-hidden-field').forEach(function(value) {
            value.value = token;
        });
        return token;
    })
}

function checker(a) {
    alertcontainer = document.createElement("div");
    alertcontainer.id = "alertcontainer_id"
    alertcontainer.className = "alertcontainer";
    document.body.appendChild(alertcontainer);
    popupdiv = document.createElement("div");
    popupdiv.id = "popupdiv";
    alertcontainer.appendChild(popupdiv);
    pop_simple_structure = document.createElement("p");
    pop_simple_structure.id = "pop_simple_structure";
    pop_simple_structure.textContent = a;
    popupdiv.appendChild(pop_simple_structure)
    $("#pop_simple_structure").innerHTML = '<div id="loader8" class="loader-container"><div class="loader eight"></div>'
}