$("#id_score_search_button").click(function(){
    $("#student_score_table").html("");
    var search_value = $("#id_score_search_input").val();
    Dajaxice.common.searchStudent(searchStudentCallBack, {"search_value": search_value,});
});
function searchStudentCallBack(data){
    $("#student_set_table").html(data);
}
$(document).on("click", "tr.show_student_detail", function(){
    studentid = $(this).attr("args");
    Dajaxice.common.getStudentScore(getStudentScoreCallBack, {"studentid": studentid, });
});
function getStudentScoreCallBack(data){
    $("#student_score_table").html(data);
}
