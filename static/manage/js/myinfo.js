function checker(a) {
    var alertcontainer = document.createElement("div");
    alertcontainer.id = "alertcontainer_id"
    alertcontainer.className = "alertcontainer";
    document.body.appendChild(alertcontainer);
    var popupdiv = document.createElement("div");
    popupdiv.id = "popupdiv";
    popupdiv.className = "row justify-content-between align-items-center";
    alertcontainer.appendChild(popupdiv);
    var loader8 = document.createElement("div");
    loader8.id = "loader8";
    loader8.className = "loader-container col-auto";
    popupdiv.appendChild(loader8);
    var loader_eight = document.createElement("div");
    loader_eight.className = "loader";
    loader_eight.classList.add("eight");
    loader8.appendChild(loader_eight)
    var pop_simple_structure_div = document.createElement("div");
    pop_simple_structure_div.className = "col text-right";
    popupdiv.appendChild(pop_simple_structure_div);
    var pop_simple_structure = document.createElement("p");
    pop_simple_structure.id = "pop_simple_structure";
    pop_simple_structure.textContent = a;
    pop_simple_structure_div.appendChild(pop_simple_structure);

    //$("#pop_simple_structure").text(a)
}


function subscribe_change() {
    checker("操作中请稍后...")
    if ($('#is_subscribe_change').is(':checked')) {
        $.ajax({
            url: "subscribe_change_on", //url
            type: "POST", //方法类型
            dataType: "json", //预期服务器返回的数据类型
            data: $('#is_subscribe_form').serialize(),
            success: function(data) {
                if (data["code"] == 1) {
                    grecaptcha_execute();
                    $("#alertcontainer_id").remove();
                    commonUtil.message(data["msg"], "warning");
                    $('#is_subscribe_change').removeAttr("checked");
                } else if (data["code"] == 2) {
                    grecaptcha_execute();
                    $("#alertcontainer_id").remove();
                    commonUtil.message(data["msg"], "danger");
                    $('#is_subscribe_change').removeAttr("checked");
                } else if (data["code"] == 0) {
                    $("#alertcontainer_id").remove();
                    commonUtil.message(data["msg"], "success");
                    window.location.reload();
                }

            },
            error: function(e) {
                //commonUtil.message(e, "danger");
                grecaptcha_execute();
                $("#alertcontainer_id").remove();
                commonUtil.message("前后端通信异常，请联系管理员！", "danger");
                $('#is_subscribe_change').removeAttr("checked");
            }
        });
    } else {
        $.ajax({
            url: "subscribe_change_off", //url
            type: "POST", //方法类型
            dataType: "json", //预期服务器返回的数据类型
            data: $('#is_subscribe_form').serialize(),
            success: function(data) {
                if (data["code"] == 1) {
                    grecaptcha_execute();
                    $("#alertcontainer_id").remove();
                    commonUtil.message(data["msg"], "warning");
                    $('#is_subscribe_change').attr("checked", "true");
                } else if (data["code"] == 2) {
                    grecaptcha_execute();
                    $("#alertcontainer_id").remove();
                    commonUtil.message(data["msg"], "danger");
                    $('#is_subscribe_change').attr("checked", "true");
                } else if (data["code"] == 0) {
                    $("#alertcontainer_id").remove();
                    commonUtil.message(data["msg"], "success");
                    window.location.reload();
                }
            },
            error: function(e) {
                //commonUtil.message(e, "danger");
                grecaptcha_execute();
                $("#alertcontainer_id").remove();
                commonUtil.message("前后端通信异常，请联系管理员！", "danger");
                $('#is_subscribe_change').attr("checked", "true");
            }
        });
    }
}

function grecaptcha_execute() {
    grecaptcha.execute('6LdXNDsaAAAAAA7PYg1n8wj2vAoePky1si63XmrD', { action: 'myinfo' }).then(function(token) {
        document.querySelectorAll('input.django-recaptcha-hidden-field').forEach(function(value) {
            value.value = token;
        });
        return token;
    })
}

$(function() {
    $("a.nav-link").removeClass("active");
    $("a.nav-link[href='/']").addClass("active");
});