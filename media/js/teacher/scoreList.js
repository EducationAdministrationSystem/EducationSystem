$(document).ready(function(){
    get_course_table("1");   
})


$(".course_filter").change(function(){
    get_course_table("1");
    $("#score_info_table").html("");
});
function get_course_table(page){
    var year = $("#id_years").val();
    var term = $("#id_terms").val();
    var grade = $("#id_grades").val();
    var page_numbers = $("#id_page_numbers").val();
    var cls = "";
    if($("#id_classes").val()) cls = $("#id_classes").val();
   
    Dajaxice.common.getCourseList(getCourseListCallBack, {
                                                "year": year,
                                                "term": term,
                                                "grade": grade,
                                                "page_numbers": page_numbers,
                                                "cls": cls,
                                                "page": page,
                                                });
}
function getCourseListCallBack(data){
    $("#course_set_table").html(data.html);
}
$(document).on("click", "div#paginator .item_page", function(){
    page = $(this).attr("arg");
    $("#score_info_table").html("");
    get_course_table(page);
});

var course_id;
$(document).on("click", ".show_course_detail", function(){
    course_id = $(this).attr("args");   
    get_course_detail(course_id, "1");
})
function get_course_detail(course_id, page){
    Dajaxice.common.getCourseScores(getCourseScoresCallBack, {"course_id": course_id, "page": page, });   
}
function getCourseScoresCallBack(data){
    $("#score_info_table").html(data.html);
}


$(document).on("click", "div#paginator2 .item_page", function(){
    page = $(this).attr("arg");
    Dajaxice.common.getCourseScores(getCourseScoresCallBack, {"course_id": course_id, "page": page, });   
});



$(document).on("click", "#scores_export_btn_simple", function(){
    var course_id = $(this).attr("args");
    Dajaxice.common.exportSimpleCourseScores(exportCallBack, {"course_id": course_id, });
})

$(document).on("click", "#scores_export_btn", function(){
    var course_id = $(this).attr("args");
    Dajaxice.common.exportCourseScores(exportCallBack, {"course_id": course_id, });

});
$(document).on("click", "#export_all", function(){
    Dajaxice.common.exportAll(exportCallBack, {});  
});

function exportCallBack(url){
    location.href = url;
};
