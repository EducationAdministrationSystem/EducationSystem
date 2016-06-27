var cb = "input[type='checkbox']";
$(document).on("click", ".checkbox", function() {
  var cnt = 0;
  $(cb).each(function() {
    if (this.checked) cnt++;
  });
  if (cnt > 2) {
    $(this).find(cb).eq(0).attr('checked', false);
    alert("一周最多选择两个课时");
  }
});

$(document).on("click","#submit",function(){
	alert("选课成功");
});