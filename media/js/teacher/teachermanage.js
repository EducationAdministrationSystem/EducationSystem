function add_teacher(){
	$('#teacheradd_error_message').empty();
	Dajaxice.adminStaff.AddTeacher(add_teacher_callback,
								  {'form':$('#teacheraddform').serialize(true)});
}

function add_teacher_callback(data){
	if(data.status =="2"){
		$each(data.error_id,function (i,item){
			object = $('#'+item);
      		object.css("border-color", 'red');
		});
	}
	$('#teacheradd_error_message').append("<strong>"+data.message+"</strong>");
}

function search_teacher(){
	Dajaxice.adminStaff.SearchTeacher(search_teacher_callback,
									 {'form':$('#teacher-search-form').serialize(true)});
}

function search_teacher_callback(data){
	$("#teacher-list-content").html(data.teacherlist_html);
}

$(document).on("click","#delete_Button",function(){
	if(confirm('您确定要删除这位老师吗？')){
		var teacherid=$(this).closest("tr").attr("iid");
		Dajaxice.adminStaff.DeleteTeacher(del_teacher_callback,{'teacherid':teacherid});
	}
});

function del_teacher_callback(data){
	$("#teacher-list-content").html(data.teacherlist_html);
}

$(document).on("click","#detail_Button",function(){
	var teacherid = $(this).closest("tr").attr("iid");
	Dajaxice.adminStaff.DetailTeacher(detail_teacher_callback,{'teacherid':teacherid});
})

function detail_teacher_callback(data){
	$("#detail-content").html(data.detail_html);
}

$(document).on("click","#edit_Button",function(){
	var teacherid = $(this).closest("tr").attr("iid");
	Dajaxice.adminStaff.getEditTeacherForm(getEditTeacherForm_callback,{'teacherid':teacherid});
})

function getEditTeacherForm_callback(data){
	$("#edit-content").html(data.teacherEdit_html);
	$("#teacher_edit_form").attr("iid",data.teacherid);
}

$(document).on("click","#submitBtn",function(){
	Dajaxice.adminStaff.EditTeacher(edit_teacher_callback,
								  {'form':$('#teacher_edit_form').serialize(true),
								   'teacherid':$("#teacher_edit_form").attr("iid")});
})

function edit_teacher_callback(data){
	$("#teacher-list-content").html(data.teacherlist_html);
}
