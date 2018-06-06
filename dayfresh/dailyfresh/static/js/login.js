$(function () {

    var error_name = false
    var error_pwd = false

    $('#username').blur(check_name)
    $('#password').blur(check_pwd)

    function check_name() {
        if ($(username).val() == ''){
            // 没有输入用户名
            $(username).css('border-color','red')
            error_name = true
        }else{
            $(username).css('border-color','rgb(224, 224, 224)')
            error_name = false
        }
    }
    function check_pwd() {
        if ($(password).val() == ''){
            // 没有输入密码
            $(password).css('border-color','red')
            error_pwd = true
        }else{
            $(password).css('border-color','rgb(224, 224, 224)')
            error_pwd = false
        }
    }
    $('form').submit(function (ev) {
        ev.preventDefault()
        check_pwd()
        check_name()
        if (error_name == false && error_pwd == false){

            data = {
                csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val(),
                username:$('#username').val(),
                password:$('#password').val()
            }

            $.ajax({
                url:window.location.href,
                data:data,
                type:'POST',
                async:true,
                success:function (data) {
                    if (data.status){
                        // 登录成功
                        if(data.next == ''){
                            window.location.href = '/goods/'
                        }else{
                            window.location.href = data.next
                        }
                    }else{
                        alert(data.msg)
                    }
                }
            })

        }
    })







})