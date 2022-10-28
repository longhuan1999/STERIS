$(function() {
        /*判断上次是否勾选记住密码和自动登录*/
        var check1s = localStorage.getItem("check1");
        var check2s = localStorage.getItem("check2");
        var oldName = localStorage.getItem("zkzh");
        var oldPass = localStorage.getItem("password");
        if (check1s == "true") {
            $("#id_zkzh").val(oldName);
            $("#id_password").val(oldPass);
            $("#check1").prop('checked', true);
        } else {
            $("#id_zkzh").val('');
            $("#id_password").val('');
            $("#check1").prop('checked', false);
        }
        if (check2s == "true") {
            $("#check2").prop('checked', true);
            $("#signinFrom").submit();
            //location="https://www.baidu.com?zkzh="+oldName+"&password="+oldPass;//添加退出当前账号功能
        } else {
            $("#check2").prop('checked', false);
        }
        /*拿到刚刚注册的账号*/
        /*if(localStorage.getItem("name")!=null){
            $("#id_zkzh").val(localStorage.getItem("name"));
        }*/


        /*$("#check2").click(function(){
            var flag=$('#check2').prop('checked');
            if(flag){
                var zkzh=$("#id_zkzh").val();
                var password=$("#id_password").val();
                $.ajax({
                    type:"post",
                    url:"http://localhost:8080/powers/pow/regUsers",
                    data:{"zkzh":zkzh,"password":password},
                    async:true,
                    success:function(res){
                        alert(res);
                    }
                });
            }
        })*/
    })
    /*登录*/
function login_click() {
    var zkzh = $("#id_zkzh").val();
    var password = $("#id_password").val();
    /*获取当前输入的账号密码*/
    localStorage.setItem("zkzh", zkzh)
    localStorage.setItem("password", password)
        /*获取记住密码  自动登录的 checkbox的值*/
    var check1 = $("#check1").prop('checked');
    var check2 = $('#check2').prop('checked');
    localStorage.setItem("check1", check1);
    localStorage.setItem("check2", check2);
    $("#login").removeClass("btn-primary");
    $("#login").addClass("btn-default");
    $("#login").attr("disabled", true);
    //$("#login").attr("disabled","disabled");
    //document.getElementById("signinForm").submit();
    $.ajax({
        //几个参数需要注意一下
        url: "", //url
        type: "POST", //方法类型
        dataType: "json", //预期服务器返回的数据类型
        data: $('#signinForm').serialize(),
        success: function(data) {
            if (data["code"] == 1) {
                commonUtil.message(data["msg"], "warning");
                grecaptcha_execute();
            } else if (data["code"] == 2) {
                commonUtil.message(data["msg"], "danger");
                grecaptcha_execute();
            } else if (data["code"] == 0) {
                commonUtil.message(data["msg"], "success");
                window.location.replace("/");
            }
            var recover_login_time = 50;

            function recover_login() {
                if (recover_login_time <= 0) {
                    $("#login").removeClass("btn-default");
                    $("#login").addClass("btn-primary");
                    $("#login").removeAttr("disabled");
                    clearInterval(recover_login_time_Obj);
                } else {
                    $("#login").removeClass("btn-primary");
                    $("#login").addClass("btn-default");
                    $("#login").attr("disabled", true);
                    recover_login_time--;
                }
            }
            var recover_login_time_Obj = setInterval(recover_login, 100);


        },
        error: function(e) {
            commonUtil.message(e, "danger");
            commonUtil.message("前后端通信异常，请联系管理员！", "danger");
            grecaptcha_execute();
            var recover_login_time = 100;

            function recover_login() {
                if (recover_login_time <= 0) {
                    $("#login").removeClass("btn-default");
                    $("#login").addClass("btn-primary");
                    $("#login").removeAttr("disabled");
                    clearInterval(recover_login_time_Obj);
                } else {
                    $("#login").removeClass("btn-primary");
                    $("#login").addClass("btn-default");
                    $("#login").attr("disabled", true);
                    recover_login_time--;
                }
            }
            var recover_login_time_Obj = setInterval(recover_login, 100);
        }
    });

    /* fetch(URL, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
    },
        body: JSON.stringify({'post_data':'Data to post'}) //JavaScript object of data to POST
    })
    .then(response => {
          return response.json() //Convert response to JSON
    })
    .then(data => {
    //Perform actions with the response data from the view
    }) */

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function grecaptcha_execute() {
    grecaptcha.execute('6LdXNDsaAAAAAA7PYg1n8wj2vAoePky1si63XmrD', { action: 'signin' }).then(function(token) {
        document.querySelectorAll('input.django-recaptcha-hidden-field').forEach(function(value) {
            value.value = token;
        });
        return token;
    })
}