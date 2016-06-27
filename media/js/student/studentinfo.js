$(function(){
    $('#id_baseinfo_birth').datetimepicker({format:"yyyy-mm-dd",minView:2});
});

window.onload = function(){
    var issave = $("#studentinfo").attr("fid");
    if(issave=="True")
        alert("信息更新成功");
    // $("#studentinfo").attr("fid","False");
}
