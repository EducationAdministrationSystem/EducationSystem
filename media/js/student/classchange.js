$(document).on("click","#btn-delete",function(){
	var student = $("#td-student").text();
	Dajaxice.student.classChangeDelete(delete_callback,{
        "student":student,
    });
})
function delete_callback(){
	var item = $("#td-student").parent().remove();
	alert("撤消成功！");
}