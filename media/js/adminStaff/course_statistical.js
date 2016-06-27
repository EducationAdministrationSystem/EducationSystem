$(document).on("change","#GradeYearSelect",function(){
    val=$("#GradeYearSelect").val();
    if(val==-1)
    {
        location.reload(true);
    }
    else{
        Dajaxice.adminStaff.CourseStatistical(statisticalcallback,{
            "rid":val
        });
    }
});
function statisticalcallback(data){
    $("#statistical_div").html(data.html);
}
