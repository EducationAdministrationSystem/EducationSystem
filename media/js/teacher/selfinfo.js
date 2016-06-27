$(document).on("click","#selfinfo_edit",function(){
	Dajaxice.teacher.getEditform(editInfo_callback);
});

function editInfo_callback(data){
	$("#edit-content").html(data.teacherEdit_html);
    $("#small_class").attr("disabled",true);

}

$(document).on("click","#submitBtn",function(){
	Dajaxice.teacher.EditSelfInfo(edit_selfinfo_callback,
								  {'form':$('#teacher_edit_form').serialize(true),});
})

function edit_selfinfo_callback(data){
	$("#selfInfo").html(data.selfinfo_html);
	$("#message").html(data.message);
}
