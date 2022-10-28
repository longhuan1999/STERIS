/*错误class  form-control is-invalid
正确class  form-control is-valid*/
var flagZkzh = false;
var flagPas = false;
var flagPass = false;
var flagStuName = false;
var flagEmail = false;
var flagEmailCode = false;
var zkzh, passWord, passWords, studentName, email, emailCode;
var regPasswd = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!|@|#|$|%|^|&|*]).{16,17}$/;
var regEmail = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
var regName = /^[\u4e00-\u9fa5]{2,4}$/;

/*验证准考证号*/
function zkzh_change() {
    zkzh = $("#id_zkzh").val();
    if (!(/^\d{12}$/.test(zkzh))) {
        $("#id_zkzh").removeClass("form-control is-valid");
        $("#id_zkzh").addClass("form-control is-invalid");
        flagZkzh = false;
    } else {
        $("#id_zkzh").removeClass("form-control is-invalid");
        $("#id_zkzh").addClass("form-control is-valid");
        flagZkzh = true;
    }
}

/*验证姓名*/
function student_name_change() {
    studentName = $("#id_student_name").val();
    if (!regName.test(studentName)) {
        $("#id_student_name").removeClass("form-control is-valid");
        $("#id_student_name").addClass("form-control is-invalid");
        flagStuName = false;
    } else {
        $("#id_student_name").removeClass("form-control is-invalid");
        $("#id_student_name").addClass("form-control is-valid");
        flagStuName = true;
    }
}

/*验证邮箱格式*/
function student_email_change() {
    email = $("#id_student_email").val();
    if (!regEmail.test(email)) {
        $("#id_student_email").removeClass("form-control is-valid");
        $("#id_student_email").addClass("form-control is-invalid");
        $("#buttonId").removeClass("btn-primary");
        $("#buttonId").addClass("btn-default");
        document.getElementById("buttonId").setAttribute("disabled", "disabled");
        flagEmail = false;
    } else {
        var buttonText = document.getElementById("buttonId").innerHTML;
        if (buttonText.indexOf("秒后可重发") == -1) {
            $("#buttonId").removeClass("btn-default");
            $("#buttonId").addClass("btn-primary");
            document.getElementById("buttonId").removeAttribute("disabled");
        }
        $("#id_student_email").removeClass("form-control is-invalid");
        $("#id_student_email").addClass("form-control is-valid");
        flagEmail = true;
    }
}

/*验证邮箱验证码*/
function checkcode_change() {
    emailCode = $("#id_checkcode").val();
    if (emailCode.length != 18) {
        $("#id_checkcode").removeClass("form-control is-valid");
        $("#id_checkcode").addClass("form-control is-invalid");
        flagEmailCode = false;
    } else {
        $("#id_checkcode").removeClass("form-control is-invalid");
        $("#id_checkcode").addClass("form-control is-valid");
        flagEmailCode = true;
    }
}

/*验证密码*/
function password1_change() {
    passWord = $("#id_password1").val();
    if (!regPasswd.test(passWord)) {
        $("#id_password1").removeClass("form-control is-valid");
        $("#id_password1").addClass("form-control is-invalid");
        flagPas = false;
    } else {
        $("#id_password1").removeClass("form-control is-invalid");
        $("#id_password1").addClass("form-control is-valid");
        flagPas = true;
    }
}

/*验证确认密码*/
function password2_change() {
    passWords = $("#id_password2").val();
    if (passWord != passWords || !regPasswd.test(passWords)) {
        $("#id_password2").removeClass("form-control is-valid");
        $("#id_password2").addClass("form-control is-invalid");
        flagPass = false;
    } else {
        $("#id_password2").removeClass("form-control is-invalid");
        $("#id_password2").addClass("form-control is-valid");
        flagPass = true;
    }
}

function regbtn_click() {
    zkzh_change();
    student_name_change();
    student_email_change();
    password1_change();
    password2_change();
    checkcode_change();
    if (flagZkzh && flagStuName && flagEmail && flagEmailCode && flagPas && flagPass) {
        $("#regbtn").removeClass("btn-primary");
        $("#regbtn").addClass("btn-default");
        $("#passwdge").removeClass("btn-primary");
        $("#passwdge").addClass("btn-default");
        $("#buttonId").removeClass("btn-primary");
        $("#buttonId").addClass("btn-default");
        $("#regbtn").attr("disabled", true);
        $("#passwdge").attr("disabled", true);
        $("#buttonId").attr("disabled", true);
        if ($("#resent").length > 0) {
            $("#resent").remove();
        }
        $.ajax({
            //几个参数需要注意一下
            url: "", //url
            type: "POST", //方法类型
            dataType: "json", //预期服务器返回的数据类型
            data: $('#signupForm').serialize(),
            success: function(data) {
                if (data["code"] == 1) {
                    commonUtil.message(data["msg"], "warning");
                    grecaptcha_execute()
                } else if (data["code"] == 2) {
                    commonUtil.message(data["msg"], "danger");
                    grecaptcha_execute()
                } else if (data["code"] == 0) {
                    commonUtil.message(data["msg"], "success");
                    window.location.replace("signin");
                }
            },
            error: function(e) {
                commonUtil.message(e, "danger");
                //commonUtil.message("前后端通信异常，请联系管理员！", "danger");
            }
        });
        var recover_signup_time = 50;

        function recover_login() {
            if (recover_signup_time <= 0) {
                $("#regbtn").removeClass("btn-default");
                $("#regbtn").addClass("btn-primary");
                $("#regbtn").removeAttr("disabled");
                $("#passwdge").removeClass("btn-default");
                $("#passwdge").addClass("btn-primary");
                $("#passwdge").removeAttr("disabled");
                student_email_change();
                clearInterval(recover_signup_time_Obj);
            } else {
                $("#regbtn").removeClass("btn-primary");
                $("#regbtn").addClass("btn-default");
                $("#passwdge").removeClass("btn-primary");
                $("#passwdge").addClass("btn-default");
                $("#buttonId").removeClass("btn-primary");
                $("#buttonId").addClass("btn-default");
                $("#regbtn").attr("disabled", true);
                $("#passwdge").attr("disabled", true);
                $("#buttonId").attr("disabled", true);
                recover_signup_time--;
            }
        }
        var recover_signup_time_Obj = setInterval(recover_login, 100);
    } else {
        commonUtil.message("请检查填写的内容", "warning");
    }
}

function grecaptcha_execute() {
    grecaptcha.execute('6LdXNDsaAAAAAA7PYg1n8wj2vAoePky1si63XmrD', { action: 'signin' }).then(function(token) {
        document.querySelectorAll('input.django-recaptcha-hidden-field').forEach(function(value) {
            value.value = token;
        });
        return token;
    })
}

function randomsort(a, b) {
    return Math.random() > .5 ? -1 : 1;
    //用Math.random()函数生成0~1之间的随机数与0.5比较，返回-1或1
}

function randomNum(minNum, maxNum) {
    switch (arguments.length) {
        case 1:
            return parseInt(Math.random() * minNum + 1, 10);
            break;
        case 2:
            return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
            break;
        default:
            return 0;
            break;
    }
}

function password_generate() {
    var passArr_a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
    var passArr_A = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    var passArr_0 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    var passArr_ = ['!', '@', '#', '$', '%', '^', '&', '*'];
    var passArr = [];
    var a_count = randomNum(1, 13);
    var A_count = randomNum(1, 14 - a_count);
    var num_count = randomNum(1, 15 - a_count - A_count);
    var _count = 16 - a_count - A_count - num_count;
    for (var i = 0; i < a_count; i++) {
        var x = Math.floor(Math.random() * 24);
        passArr.push(passArr_a[x]);
    }
    for (var i = 0; i < A_count; i++) {
        var x = Math.floor(Math.random() * 24);
        passArr.push(passArr_A[x]);
    }
    for (var i = 0; i < num_count; i++) {
        var x = Math.floor(Math.random() * 10);
        passArr.push(passArr_0[x]);
    }
    for (var i = 0; i < _count; i++) {
        var x = Math.floor(Math.random() * 8);
        passArr.push(passArr_[x]);
    }
    passArr.sort(randomsort);
    var password = '';
    for (var i = 0; i < 16; i++) {
        password += passArr[i];
    }
    var gen_password1 = document.getElementById("id_password1");
    gen_password1.classList.add("value");
    gen_password1.value = password;
    password1_change();
    var gen_password2 = document.getElementById("id_password2");
    gen_password2.classList.add("value");
    gen_password2.value = password;
    password2_change();
    var gen_passwd_msg = "生成随机密码：" + password + "。不需要特地记忆密码，注册成功后会发送到你邮箱！";
    commonUtil.message(gen_passwd_msg, "success");
    zkzh_change();
    student_name_change();
    student_email_change();
}

function submitonce() {
    $("#regbtn").removeClass("btn-primary");
    $("#regbtn").addClass("btn-default");
    $("#passwdge").removeClass("btn-primary");
    $("#passwdge").addClass("btn-default");
    $("#buttonId").removeClass("btn-primary");
    $("#buttonId").addClass("btn-default");
    $("#regbtn").attr("disabled", true);
    $("#passwdge").attr("disabled", true);
    $("#buttonId").attr("disabled", true);
    $("#signupForm").append($('<input type="hidden" id="resent" name="resent">'));
    $.ajax({
        //几个参数需要注意一下
        url: "", //url
        type: "POST", //方法类型
        dataType: "json", //预期服务器返回的数据类型
        data: $('#signupForm').serialize(),
        success: function(data) {
            var recover_resent_time = 60;
            if (data["code"] == 1) {
                commonUtil.message(data["msg"], "warning");
                grecaptcha_execute();
                recover_resent_time = 50;
            } else if (data["code"] == 2) {
                commonUtil.message(data["msg"], "danger");
                grecaptcha_execute();
                recover_resent_time = 50;
            } else if (data["code"] == 0) {
                commonUtil.message(data["msg"], "success");
                recover_resent_time = 600;
            }

            function recover_resent() {
                if (recover_resent_time <= 0) {
                    $("#regbtn").removeClass("btn-default");
                    $("#regbtn").addClass("btn-primary");
                    $("#regbtn").removeAttr("disabled");
                    $("#passwdge").removeClass("btn-default");
                    $("#passwdge").addClass("btn-primary");
                    $("#passwdge").removeAttr("disabled");
                    var x = "重发验证码";
                    $("#buttonId").text(x);
                    student_email_change();
                    clearInterval(recover_resent_time_Obj);
                } else if (recover_resent_time > 0 && recover_resent_time <= 600) {
                    var t = parseInt(recover_resent_time / 10) + "秒后可重发";
                    $("#buttonId").removeClass("btn-primary");
                    $("#buttonId").addClass("btn-default");
                    $("#regbtn").attr("disabled", true);
                    $("#buttonId").text(t);
                    recover_resent_time--;
                }
                if (recover_resent_time > 540 && recover_resent_time <= 550) {
                    $("#regbtn").removeClass("btn-default");
                    $("#regbtn").addClass("btn-primary");
                    $("#regbtn").removeAttr("disabled");
                    $("#passwdge").removeClass("btn-default");
                    $("#passwdge").addClass("btn-primary");
                    $("#passwdge").removeAttr("disabled");
                }
            }
            var recover_resent_time_Obj = setInterval(recover_resent, 100);


        },
        error: function(e) {
            commonUtil.message(e, "danger");
            grecaptcha_execute();
            $("#regbtn").removeClass("btn-default");
            $("#regbtn").addClass("btn-primary");
            $("#regbtn").removeAttr("disabled");
            $("#passwdge").removeClass("btn-default");
            $("#passwdge").addClass("btn-primary");
            $("#passwdge").removeAttr("disabled");
            student_email_change();
        }
    });
}



window.onload = function() {
    var times = JSON.parse(document.getElementById('left_time').textContent);
    var timeDiv = document.getElementById("buttonId");
    timeDiv.setAttribute("disabled", "disabled");
    var timeObj = null;

    function timer() {
        if (times <= 0) {
            var x = "重发验证码";
            if ($("#id_student_email").hasClass('is-valid')) {
                $("#buttonId").removeClass("btn-default");
                $("#buttonId").addClass("btn-primary");
                timeDiv.removeAttribute("disabled");
            }
            clearInterval(timeObj);
            timeDiv.innerHTML = x;
        }
        if (times > 0 && times <= 600) {
            var t = parseInt(times / 10) + "秒后可重发";
            $("#buttonId").removeClass("btn-primary");
            $("#buttonId").addClass("btn-default");
            timeDiv.setAttribute("disabled", "disabled");
            timeDiv.innerHTML = t;
            times--;
        }
        if (times == 999) {
            var s = "发送验证码";
            clearInterval(timeObj);
            timeDiv.innerHTML = s;
        }
    }
    timeObj = window.setInterval(timer, 100);

    if (document.getElementById('signup_zkzh')) {
        var signup_zkzh = document.getElementById("id_zkzh");
        signup_zkzh.classList.add("value");
        signup_zkzh.value = JSON.parse(document.getElementById('signup_zkzh').textContent);
        zkzh_change();
    }

    if (document.getElementById('signup_student_name')) {
        var signup_student_name = document.getElementById("id_student_name");
        signup_student_name.classList.add("value");
        signup_student_name.value = JSON.parse(document.getElementById('signup_student_name').textContent);
        student_name_change();
    }

    if (document.getElementById('signup_password1')) {
        var signup_password1 = document.getElementById("id_password1");
        signup_password1.classList.add("value");
        signup_password1.value = JSON.parse(document.getElementById('signup_password1').textContent);
        password1_change();
    }

    if (document.getElementById('signup_password2')) {
        var signup_password2 = document.getElementById("id_password2");
        signup_password2.classList.add("value");
        signup_password2.value = JSON.parse(document.getElementById('signup_password2').textContent);
        password2_change();
    }

    if (document.getElementById('signup_student_email')) {
        var signup_student_email = document.getElementById("id_student_email");
        signup_student_email.classList.add("value");
        signup_student_email.value = JSON.parse(document.getElementById('signup_student_email').textContent);
        student_email_change();
    }
}