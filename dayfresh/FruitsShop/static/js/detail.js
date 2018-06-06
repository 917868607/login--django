function cprice(type) {
        var stock = parseInt($('#stock').text())
        if (type=='add'){
            input = document.getElementsByTagName('input')
            var num = parseInt($('.num_show').attr('value'))
            if (num < stock){
                num += 1
            }
        }else if(type=="minus"){
            var num = parseInt($('.num_show').attr('value'))
            if (num >1 ){
                num -= 1
            }
        }
        $('.num_show').attr('value',num)
        $('.num_show')[0].value=num
        // 展示数量
        $('.num_name').text('数量: '+num)
        //价格
        var price = $('.show_pirze > em')[0].textContent
        price = parseFloat(price)
        var price = price * num
         price = price.toFixed(2)
        console.log(price)
        $('.total > em').text(price)
    }
window.onload = function (ev) {
    function add() {
        console.log('add函数')
        var num = $('.num_show').val()
    }
    var num = 1
    $('#add_cart').mousedown(function () {
        // 发请求添加购物车
        // 商品数量,商品id
        //post请求
        var num = $('.num_show').val()
        var good_id = $('.operate_btn').attr('id')
        var url="/cart/add_cart/"
        var csrf_token = $('#csrf_token').text()
        $.ajax({
            url:url,
            data:{
                //总价
                s_money: $('.total > em').text(),
                //库存
                stock: $('#stock').text(),
                good_id:good_id,
                num:num,
                next_href:window.location.href,
                csrfmiddlewaretoken: csrf_token
            },
            type:'POST',
            async:true,
            success:function (data) {
                alert(data.Meg)
                if (data.url){
                    window.location.href =data.url
                }else if (data.status == 1){
                    $('#show_count').text(data.count)
                }

            },
            error :function (data) {
                console.log(data)
            }

        })
    })
    $('.num_show').blur(function (ev) {
        var stock = parseInt($('#stock').text())
        var num = parseInt($(this).val())
        if (num <1){
            num = 1
        }else if(num > stock){
            num = stock
        }
        $('.num_show').val(num)
        $('.num_show').attr('value',num)
         // 展示数量
        $('.num_name').text('数量: '+num)
        //价格
        var price = $('.show_pirze > em')[0].textContent
        price = parseFloat(price)
        var price = price * num
         price = price.toFixed(2)
        console.log(price)
        $('.total > em').text(price)
    })
    $('.add').mousedown(function () {
        cprice('add')
    })
    $('.minus').mousedown(function () {
        cprice('minus')
    })
    // 添加购物车

    //点击购物车没有登录的状态
    // $('.cart_name').mousedown(function (env) {
    //     user_id = $(this).attr('id')
    //     if (user_id == None){
    //         //get请求,带着本业网址
    //         url='/cart/cartinfo/?next='+ window.location.href
    //         $.get(url,function (data) {
    //
    //         })
    //
    //
    //     }
    // })
}