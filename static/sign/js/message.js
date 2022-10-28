if(JSON.parse(document.getElementById('message').textContent) == "邮箱验证码已发送，请注意查收！"){
    commonUtil.message(JSON.parse(document.getElementById('message').textContent), "success");
}
else if(JSON.parse(document.getElementById('message').textContent) == "密码不正确！"){
    commonUtil.message(JSON.parse(document.getElementById('message').textContent), "warning");
}
else if(JSON.parse(document.getElementById('message').textContent) == "信息不存在！"){
    commonUtil.message(JSON.parse(document.getElementById('message').textContent), "danger");
}
else{
      commonUtil.message(JSON.parse(document.getElementById('message').textContent), "warning");
  
}