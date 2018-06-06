// $('body').ready(function () {
window.onload = function (ev) {


    // alert('页面加载完成')
    function remove() {
        $('h6').remove()
    }
    $('.ch').blur(function (ev) {
        console.log($(this).val())
        console.log($(this))
        // id值
        console.log($(this)[0].id)
        var url = "/user/checkuser/"
        if ($(this)[0].id == 'user_name'){
            var data = {'user_name':$(this).val()}
        }else if($(this)[0].id == 'email'){
            var data={'email':$(this).val()}
        }else if($(this)[0].id == 'cpwd'){
            var data = {'cpwd':$(this).val(),'pwd':$('#pwd').val()}
        }
        console.log(data)
        $.get(url,data,function (data) {
            remove()
            console.log(data)
            if (data){
                var h6 = '<h6>'+data.Meg.err+'</h6>'
                console.log($("#"+data.name))
                $($("#"+data.name)).after(h6)
            }else{
                console.log(data)
            }

        })

    })


    $.ajaxSetup({
        data: {
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        }
    })
    $('#reg_form').submit(function (even) {
        even.preventDefault()
        $.ajax({
            url:'/user/checkuser/',
            data:$('form').serialize(),
            type:'POST',
            async:true,
            success:function (data,status,xhr) {
                remove()
                console.log(data)
                if (data.name == 0){
                    // 数据不合法
                    for (key in data.Meg){
                        var h6 = '<h6>'+data.Meg[key]+'</h6>'
                        $('#'+key).after(h6)
                    }
                }
                else if(data.status == 0){
                    h6 = '<h6>'+data.Meg.err+'</h6>'
                    $('#'+data.name).after(h6)
                }
                else if (data.status == 1){
                    // 注册成功
                    console.log('注册成功')
                    window.location.href = '/user/login'
                }
            },
            error:function (status,xhr,errorThrown) {
                console.log(status,xhr,errorThrown)
            },
            complate:function () {
                console.log('请求完成')
            }
    })
    })



}


// })