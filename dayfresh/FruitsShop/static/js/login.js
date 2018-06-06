window.onload = function (ev) {
    console.log($('.ch'))
    $.ajaxSetup({
        data:{'csrfmiddlewaretoken':'{{csrf_token}}'}
    })
    $('.ch').blur(function (eve) {
        var url = 'http://127.0.0.1:8000/user/checklogin/'
        if ($(this)[0].id=='username'){
            var data = {'username':$(this).val()}
        }
        $.get(url,data,function (data) {
            console.log(data)
            if (data.status ==0){
                $('#user_error').css('display','block')
            }

        })
    })
    // 提交数据
    $('form').submit(function (eve) {
        eve.preventDefault()
        console.log(window.location.href)
        $.ajax({
            url:window.location.href,
            data:$(this).serialize(),
            type:"POST",
            success:function (data,status,xhr) {
                console.log(data)
                // 表单不合法
                if (data.name==0){
                    if (data.Meg.pwd){
                        $('#pwd_error').css('display','block')
                    }
                }
                else if(data.name == 'pwd'){
                    $('#pwd_error').css('display','block')
                }
                else if(data.status == 1){
                    if (data.next){
                         window.location.href= data.next
                    }else {
                        window.location.href= '/'
                    }


                }
            },
            error:function (status,xhr,errorThrow) {
                console.log(status.xhr,errorThrow)
            },
            commplate:function () {
                console.log('请求完成')
            }

        })
    })
}
