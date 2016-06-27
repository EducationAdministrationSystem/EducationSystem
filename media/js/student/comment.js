
$(document).on("click","#comment_button",function(){
	var cid=$(this).closest("tr").attr("iid");
	$("#form_courseid").val(cid);
});

$(document).on("click","#lookup_comment",function(){
	var cid=$(this).closest('tr').attr("iid");
	Dajaxice.student.getComment(showComment,{"courseid":cid});
});


function showComment(data){
	$("#comment_content").html(data.form_html);
}

