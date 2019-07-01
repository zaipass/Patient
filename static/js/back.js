function sub(){
    var csrftoken = getCookie('csrftoken');
    var data = $("#ad-form-login").serialize();
    $.ajax({
        url: "/login/",
        type: "post",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: data,
        success: function(resp, txt, xhr){
            window.location.href="/info-list/";
        },
        error: function(jqXHR, txt, status){
            $(".error-info").html(jqXHR.responseJSON.detail);
        },
    })
}
