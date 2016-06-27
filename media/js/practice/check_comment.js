$(document).on("click","#lookup_comment",function(){
	var cid=$(this).closest('tr').attr("iid");
	Dajaxice.practice.getComment(showComment,{"courseid":cid});
});


function showComment(data){
	$("#comment_content").html(data.form_html);
}