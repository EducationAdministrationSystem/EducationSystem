function add_class(){
	Dajaxice.adminStaff.AddClass(add_class_callback,
								  {'form':$('#class-add-form').serialize(true)});
}

function add_class_callback(data){
	$("#classlist-content").html(data.classlist_html);
	$("#class-add-message").html("<strong>"+data.message+"</strong>");
}

function add_smallclass(){
	Dajaxice.adminStaff.AddSmallClass(add_smallclass_callback,
								  {'form':$('#smallclass-add-form').serialize(true)});
}

function add_smallclass_callback(data){
	$("#smallclass-add-message").html("<strong>"+data.message+"</strong>");
}

$(document).on("click","#delete_Button",function(){
	if(confirm("删除班级会使得关于该班级的所有东西都被删除，您确定要这么做吗？")){
		var classid=$(this).closest("tr").attr("iid");
		Dajaxice.adminStaff.DeleteClass(delete_class_callback,
										{'classid':classid});
	}
});

function delete_class_callback(data){
	$("#classlist-content").html(data.classlist_html);
}
