$(function(){
    var is_token = getCookie('csrftoken');
    if(is_token == null){
        $.ajax({
            url: "/token/",
            type: "get"
        })
    }
})