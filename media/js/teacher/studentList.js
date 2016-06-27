$(document).ready(function(){
    get_student_table("1");
});

function get_student_table(page){
    $("#student_score_table").html("");
    var year = $("#id_years").val();
    var page_numbers = $("#id_page_numbers").val();
    var cls = "";
    if($("#id_classes").val()) cls = $("#id_classes").val();
    Dajaxice.common.getStudentList(getStudentListCallback, {"year": year, 
                                                            "page_numbers": page_numbers,
                                                            "cls": cls, 
                                                            "page": page});

}
function getStudentListCallback(data){
    $("#student_set_table").html(data);
}
$(".student_filter").change(function(){
    get_student_table("1");    
});

$(document).on("click", "div#paginator .item_page", function(){
    get_student_table($(this).attr("arg")); 
});
$(document).on("click", "tr.show_student_detail", function(){
    studentid = $(this).attr("args");
    Dajaxice.common.getStudentScore(getStudentScoreCallBack, {"studentid": studentid, });
});
function getStudentScoreCallBack(data){
    $("#student_score_modal .modal-body").html(data);
    $("#student_score_modal").modal();
}
