$(function () {

    // 定义变量记录每一个数据是否有误
    // 用户名错误
    var error_name = false
    // 密码错误
    var error_pwd = false
    // 检查密码
    var error_check_pwd = false
    // 邮箱错误
    var error_email = false
    // 用户协议错误
    var error_check = false

    // 失去焦点,检测用户名
    $('#user_name').blur(function () {
        check_user_name()
    })
    $('#pwd').blur(function () {
        check_pwd()
        check_cpwd()
    })
    $('#cpwd').blur(function () {
        check_cpwd()
    })
    $('#email').blur(function () {
        check_email()
    })

    // 检测用户名是否合法
    function check_user_name() {
        // 获取输入框内容长度
        var len =$('#user_name').val().length
        // 规定用户名不能小于6位 大于20位
        if (len<6 || len>20){
            // next() 获取标签的下一个兄弟标签
            $('#user_name').next().text('请输入5-20个字符的用户名')
            $('#user_name').next().show()
            error_name = true
        }else{
            // 实时检测用户名是否被占用
            var url = '/user/check_user?username='+$('#user_name').val()
            
            $.get(url,function (data) {

                if (data.status == 0){
                    // 用户名被占用
                    error_name = true
                }else{
                    // 用户名未被占用
                    error_name = false
                }
                $('#user_name').next().text(data.msg)
                $('#user_name').next().show()
            })
        }
    }
    // 检测密码是否合法
    function check_pwd() {
        // 获取密码输入框值的长度
        var len = $('#pwd').val().length
        // 不能少于8位 大于20位
        if (len < 8 ||len>20){
            $('#pwd').next().text('密码最少8位,最大20位')
            $('#pwd').next().show()
            error_pwd = true
        }else{
            $('#pwd').next().hide()
            error_pwd = false
        }
    }
    // 检测两次面是否一致
    function check_cpwd() {
        var pwd = $('#pwd').val()
        var cpwd = $('#cpwd').val()
        if(pwd != cpwd) {
            $('#cpwd').next().text('两次密码输入不一致')
            $('#cpwd').next().show()
            error_check_pwd = true
        }else{
            $('#cpwd').next().hide()
            error_check_pwd = false
        }
    }

    // 检测邮箱
    function check_email() {
        // 正则表达式
        var re = /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/
        if (re.test($('#email').val())){
            $('#email').next().hide()
            error_email = false
        }else{
            $('#email').next().text('请输入正确的邮箱地址')
            $('#email').next().show()
            error_email = true
        }
    }

    // 检测是否同意用户协议
    $('#allow').click(check_protocol)
    function check_protocol() {
        // is(:checked)
        if($(this).is(':checked')){
            error_check = false
            $('#allow_err').hide()
        }else{
            error_check = true
            // 找到下一个标签的下一个标签
            // prev()找上一个标签
            // prevent()找父级标签
            // children() 找后代标签
            $('#allow').next().next().text('请勾选同意')
            $('#allow').next().next().show()
        }
    }

    // form表单的提交事件
    $('#reg_form').submit(function (ev) {
        // 禁止默认表单提交事件
        ev.preventDefault()
        // 检测各个数据的可用性
        check_email()
        check_cpwd()
        check_pwd()
        check_user_name()

        if (error_check == false && error_email == false && error_check_pwd == false && error_name == false && error_pwd==false){

            // 提交注册请求
            data = {
                csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val(),
                username:$('#user_name').val(),
                password:$('#pwd').val(),
                email:$('#email').val()
            }
            $.ajax({
                url:'/user/register/',
                data:data,
                type:'POST',
                async:true,
                success:function (data) {
                    if(data.status == 0){
                        $('#user_name').next().text(data.msg)
                        $('#user_name').next().show()
                    }else if(data.status == 500){
                        $('#user_name').next().hide()
                        alert(data.msg)
                    }else {
                        $('#user_name').next().hide()
                        alert(data.msg)
                        window.location.href = '/user/login/'
                    }
                }
            })



        }
    })
    









})