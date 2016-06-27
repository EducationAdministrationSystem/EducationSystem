var glob_course_id
var target_row, var_1, var_2, var_3;

$("[name='ratio_set']").click(function(){
    target_row = $(this).parent().parent();
    glob_course_id = $(this).attr("args");
    Dajaxice.teacher.fillForm(fillFormCallBack, {"course_id": glob_course_id,});
});
function fillFormCallBack(data){
    $("div.modal-body").html(data.html);
}

$(document).on("click", "#ratio_save_btn", function(){
   var_1 = $("#id_attendance_rate").val(); 
   var_2 = $("#id_homework_rate").val();
   var_3 = $("#id_final_rate").val();
   Dajaxice.teacher.saveRatio(saveRatioCallBack, {"course_id": glob_course_id, "var_1": var_1, "var_2": var_2, "var_3": var_3});
});
function saveRatioCallBack(data){
    if(data.message == "error"){
        alert("输入不合法");
    }
    else if(data.message == "unfit"){
        alert("输入比例之和不为100");
    }
    else{
        target_row.find("td").eq(1).html(var_1);
        target_row.find("td").eq(2).html(var_2);
        target_row.find("td").eq(3).html(var_3);
        alert("保存成功");
    }
}

