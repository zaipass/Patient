$(function () {
    // $(".user-div").mouseout(show_or_hide);

  var jwt = getCookie("token");
  $("#pagination").pagination({
    dataSource: "/info/",
    locator: "data",
    showGoInput: true,
    showGoButton: true,
    totalNumberLocator: function (resp) {
      $(".user-info-name").text(resp.username);
      return resp.total_numbers;
    },
    formatAjaxError: function (jqXHR, textStatus, errorThrown) {
      alert(jqXHR.responseText);
      window.location.href = "/manage/";
    },
    ajax: {
      type: "GET",
      headers: {
        "JWT-Token": jwt
      }
    },
    callback: function (data, pagination) {
      var inhtml = "";
      var innertext = [
        "<tr>" +
        "<th>诊所名称</th>" +
        "<th>医生姓名</th>" +
        "<th>医生电话</th>" +
        "<th>患者姓名</th>" +
        "<th>年龄/性别</th>" +
        "<th>患者电话</th>" +
        "<th>患者描述</th>" +
        "</tr>"
      ];
      for (var i = 0; i < data.length; i++) {
        inhtml += "<a>" + data[i].clinical_name + "</a><br/>";

        innertext.push(
          "<tr>" +
          "<td>" +
          data[i].clinical_name +
          "</td>" +
          "<td>" +
          data[i].doc_name +
          "</td>" +
          "<td>" +
          data[i].doc_phone +
          "</td>" +
          "<td>" +
          data[i].patient_name +
          "</td>" +
          "<td>" +
          data[i].sex_age +
          "</td>" +
          "<td>" +
          data[i].patient_phone +
          "</td>" +
          "<td>" +
          data[i].patient_detail +
          "</td>" +
          "</tr>"
        );
      }

      $(".info-table").html(innertext.join(""));
    }
  });
});

function logout() {
  var jwt = getCookie("token");
  var is_out = confirm("是否退出当前账号");

  if (is_out) {
    $.ajax({
      url: "/logout/",
      type: "get",
      headers: {
        "JWT-Token": jwt
      },
      success: function (resp, txt, xhr) {
        window.location.href = "/manage/";
      },
      error: function (jqXHR, txt, status) {
        alert(jqXHR.responseText);
        window.location.href = "/manage/";
      }
    });
  }
}

function show_or_hide() {
  var param = $(".func-inner-box").css("display");
  if (param == "flex") {
    $(".func-inner-box").css("display", "none");
  } else {
    $(".func-inner-box").css("display", "flex");
  }
}

function file_out(){
  var is_file_out = confirm("是否导出全部数据");
  var jwt = getCookie("token");

  if (is_file_out) {
    $.ajax({
      url: "/file-out/",
      type: "get",
      headers: {
        "JWT-Token": jwt
      },
      success: function (resp, txt, xhr) {
        window.location.href = "/download/"+resp.filename;
      },
      error: function (jqXHR, txt, status) {
        if(jqXHR.responseText){
            alert(jqXHR.responseText);
        }
        if(jqXHR.responseJSON.detail){
            alert(jqXHR.responseJSON.detail);
        }
      }
    });
  }
}