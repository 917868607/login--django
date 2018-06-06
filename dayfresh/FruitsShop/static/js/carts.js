window.onload = function (ev) {
    //计算商品总价函数
    function cart_total() {
        //声明变量记录商品总价和商品总个数
        var totalPrice = 0
        var totalCount = 0
        //找到所有的商品小计标签
        //each() 类似于for循环,让找到的每一个标签都去执行某个函数
        $('.col07').each(function () {
            //找到上一个标签中的input
            //prev()找上一个标签 find()找到某个标签中的某个标签
            var count = $(this).prev().find('input').val()
            var price = $(this).prev().prev().text()
            //展示小计价格
            var current_total = parseInt(count) * parseFloat(price)
            //展示小计价格
            $(this).text(current_total.toFixed(2))
            //判断当前商品是否被选中
            //siblings()找到所有的兄弟节点
            //children()找后台的标签
            //prop()获取某个属性值有的返回True.没有返回false, 设置某个属性值
            if($(this).siblings('.col01').children('input').prop('checked')){
                //总计+=小计
                totalPrice += current_total
                //商品总个数
                totalCount += parseInt(count)
                $('#totalprice').text(totalPrice.toFixed(2))
                $('.totalnum').text(totalCount.toFixed(2))
            }
            else {
                $('#totalprice').text(0)
                $('.totalnum').text(0)
            }
        })
    }
    cart_total()

    $('.add').mousedown(function () {
        var stock = $(this).siblings('#stock').attr('class')
        console.log(stock)
        var value = parseInt($(this).siblings('input').attr('value'))
        var good_id = parseInt($(this).siblings('input').attr('id'))
        value += 1
        if (value > parseInt(stock)){
            value = stock
        }
        $(this).siblings('input').attr('value',value)
        cart_total()
        send(good_id,value)

    })
    $('.minus').mousedown(function () {
        var good_id = parseInt($(this).siblings('input').attr('id'))
        var value = parseInt($(this).siblings('input').attr('value'))
        value -= 1
        if (value >= 1){
            $(this).siblings('input').attr('value',value)
            cart_total()
            send(good_id,value)
        }

    })
    $('.num_show').blur(function () {
        var good_id = parseInt($(this).attr('id'))
        var value = parseInt($(this).val())
        var stock = parseInt($(this).siblings('#stock').attr('class'))
        if (value > stock){
            value = stock
        }else if(value < 1){
            value = 1
        }
        $(this).attr('value',value)
        $(this).val(value)
        cart_total()
        send(good_id,value)
    })
    function send(goods_id,num) {
        var csrf = $('form').attr('id')
        console.log(csrf)
        url = '/cart/order_check/'
        data = {
            goods_id:goods_id,
            num:num,
            csrfmiddlewaretoken:$('form').attr('id')

        }
        $.post(url,data,function (data) {
            console.log(data)
            if (data.status == 1){
                console.log(data.Meg)
            }
        else if(data.status == 0){
                consoe.log(data.Meg)

                $(this).siblings('input').attr('value',num)
                cart_total()
                alert('网络原因,请刷新页面')
            }}
        )

    }

    //实现全选择和全消
    $('#checkall').click(function () {
        console.log('点击去哪徐')
        //获取全选和全消
        var is_true = $(this).prop('checked')
        //找到所有的复选框
        $('.check').prop('checked',is_true)
        //全算计算价格
        cart_total()
    })
    //选择或者取消一个框
    $('.check').click(function () {
        //点击当前选框是被选中的状态
        if ($(this).prop('checked')){
            //判断所有的复选框是否被选中
            //找到所有的被选中的复选模
            var check_num = $('.check:checked').length
            if (check_num == $('.check').length){
                //如果都是选中的状态.展示全选状态
                $('#checkall').prop('checked',true)
            }else {
                $('#checkall').prop('checked',false)
            }
        }
        else{
            //点击后复选框没有被选中
            //取消全选状态
            $('#checkall').prop('checked',false)

        }
        cart_total()
    })

    $.ajaxSetup({
    data:{'csrfmiddlewaretoken':$('form').attr('id')}
    })

    //提交订单
    $('from').submit(function (env) {
        env.preventDefault()
        $.ajax({
            url:'/add_order/',
            data:{

            }
        })
    })
}