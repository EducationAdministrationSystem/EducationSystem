if(!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'
                ? args[number] : match;
        });
    };
}

function toggle(){
    $("#div_total_score_checkin").toggle();
    $('#div_sub_score_checkin').toggle();
}

$("#checkbox_select_total").click(function(){
    toggle();
});

function get_statistics(){
    var course_id = $("#course_select").val();
    Dajaxice.teacher.getStatistics(getStatisticsCallBack, {"course_id": course_id, });
}
function getStatisticsCallBack(data){
    $("#statistics").html(data);
}
$("#course_select").change(function(){
    alert("dddddddd");
    var course_id = $(this).val();
    Dajaxice.teacher.getCourseMembers(getCourseMembersCallBack, {"course_id": course_id,});
});
function getCourseMembersCallBack(data){
    $("#div_sub_score_checkin").html(data.sub_html);
    $("#div_total_score_checkin").html(data.total_html);
    get_statistics();
}

$(document).ready(function(){
    if($("#course_select").length==0)return false;
    var course_id = $("#course_select").val(); 
    Dajaxice.teacher.getCourseMembers(getCourseMembersCallBack, {"course_id": course_id,});
    
});

var tr, var_1, var_2, var_3;

$(document).on("blur", "input[name='sub_input']", function(){
    tr = $(this).parent().parent();
    var select_id = tr.attr("args");
    var_1 = tr.find("input").eq(0).val();
    var_2 = tr.find("input").eq(1).val();
    var_3 = tr.find("input").eq(2).val();
    Dajaxice.teacher.scoreCheckIn(subScoreCheckInCallBack, {"select_id": select_id, 
                                                         "var_1": var_1,
                                                         "var_2": var_2,
                                                         "var_3": var_3,});
});
function subScoreCheckInCallBack(data){
    if(data.message == "error"){
        alert("输入不合法！");   
    }
    else if(data.message == "overflow"){
        alert("输入越界！");
    }
    else{
        tr.find("td").eq(5).html(data.total);    
        pair_tr = $("#div_total_score_checkin tr[args='{0}']".format(tr.attr("args")));
        pair_tr.find("td").eq(2).html(var_1);
        pair_tr.find("td").eq(3).html(var_2);
        pair_tr.find("td").eq(4).html(var_3);
        pair_tr.find("input").eq(0).val(data.total);
        get_statistics();
    }
}

$(document).on("blur", "input[name='total_input']", function(){
    tr = $(this).parent().parent();
    var select_id = tr.attr("args");
    var_1 = $(this).val();
    Dajaxice.teacher.scoreCheckIn(totalScoreCheckInCallBack, {"select_id": select_id, 
                                                         "var_1": var_1,
                                                         "var_2": var_1,
                                                         "var_3": var_1,});

});
function totalScoreCheckInCallBack(data){
    if(data.message == "error"){
        alert("输入不合法！");   
    }
    else if(data.message == "overflow"){
        alert("输入越界！");
    }
    else{
        tr.find("td").eq(2).html(var_1);
        tr.find("td").eq(3).html(var_1);
        tr.find("td").eq(4).html(var_1);

        pair_tr = $("#div_sub_score_checkin tr[args='{0}']".format(tr.attr("args")));
        pair_tr.find("input").eq(0).val(var_1);
        pair_tr.find("input").eq(1).val(var_1);
        pair_tr.find("input").eq(2).val(var_1);
        pair_tr.find("td").eq(5).html(var_1);

        get_statistics();
    }
}


$(document).on("click", ".submit_btn", function(){
    course_id = $(this).attr("args"); 
    Dajaxice.teacher.submitCourse(submitCourseCallBack, {"course_id": course_id});
});
function submitCourseCallBack(data){
    Dajaxice.teacher.getCourseMembers(getCourseMembersCallBack, {"course_id": data.course_id,});
}
