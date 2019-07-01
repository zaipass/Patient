function submit_form() {
    clear_all();
    var csrftoken = getCookie('csrftoken');
    $(".submit-btn").removeAttr("onclick");
    $(".submit-btn").attr("value", "提交中");
    var data = $("#form-into").serialize();
    $.ajax({
        url: "/create-info/",
        type: "post",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: data,
        success: function (resp, txt, xhr) {
            $(".submit-btn").attr("onclick", "submit_form()");
            $(".submit-btn").prop("value", "提交");
            $(".right-msg").html('*** ' + resp.detail + ' ***');
            reset_form();
        },
        error: function (jqXHR, txt, status) {
            $(".submit-btn").attr("onclick", "submit_form()");
            $(".submit-btn").prop("value", "提交");
            $(".error-msg").html('错误:<br />' + jqXHR.responseJSON.detail);
        },
    })
}

function reset_form() {
    $("#form-into").trigger("reset");
}

function click_input() {
    $(".right-msg").text("");
}

function clear_all() {
    $(".right-msg").text("");
    $(".error-msg").text("");
}

$(function () {
    $(".normal").click(click_input);
})
