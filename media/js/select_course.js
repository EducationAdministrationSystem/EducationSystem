$(document).on("click","#select_confirm",function(){
    var select_div = $("#select_course");
    var box = $(select_div).find(".course_checkbox");
    var selected=new Array();
    var plan_id = new Array();
    for(var i=0;i<box.length;++i)
    {
        if(box[i].checked)
        {
            var tr =$(box[i]).parent().parent();
            var val=$(tr).attr("iid");
            var name = $(tr).children(":first").html();
            selected.push(val);
            plan_id.push(name);
        }
    
    }
    if(selected.length===0)
    {
        $("#info_alert").html("没有选定课程！");
        $("#alert_info_modal").modal('show');
        return false;
    }
    var flag = 1;
    for(var i=0;i<plan_id.length;++i)
    {
        iid1 = plan_id[i].substr(0,8);
        for(var j=0;j<plan_id.length;++j)
        {
            if(i==j)continue;
            iid2 = plan_id[i].substr(0,8);
            if(iid1==iid2)
            {
                flag = 0;
                break;
            }
        }
    }
    if(flag==0)alert("不能选择相同课程！");
    if(flag==1)
    {
        var sid=-1;
        if($("#studentid").length>0)
        {
            sid=$("#studentid").val();
        }
        Dajaxice.common.SelectCourseOperation(select_course_callback,{
            "selected":selected,
            "sid":sid
        })
    }
    
});

function select_course_callback(data){

        $("#info_alert").html(data.status);
        $("#alert_info_modal").modal('show');

}
$(document).on("hide.bs.modal","#alert_info_modal",function(e){
    
    location.reload(true);   
});
