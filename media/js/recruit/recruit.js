$(document).ready(function(){
	function getCollege()
	{
	    var value=$("#id_apartment").children('option:selected').val();
	    if(value)
	    {
		Dajaxice.common.getCollege(getCollegeCallBack,{"apartment":value});
	    }
	    else
	    {
		$("#id_college").empty();
		$("<option value selected='selected'>---------</option>").appendTo("#id_college");
	    }
	}


	getCollege();
	$("#id_apartment").change(function(){
	    getCollege();
	});
	function getCollegeCallBack(data)
	{
	    var college=data.college;
	    $("#id_college").empty();
	    $("<option value selected='selected'>---------</option>").appendTo("#id_college");
	    for(var v in college)
	    {
		$("<option value="+college[v][0]+">"+college[v][1]+"</option>").appendTo("#id_college");
	    }
	}
    // 隐藏“全院公共课”
    $("#id_wish_first option[value='10'], #id_wish_second option[value='10']").each(function(){
       $(this).hide();
    });
$
});

$("input[name='commit']").click(function(){
    //if(confirm("相同学号再次提交将会覆盖上次的信息, 确认是否提交报名信息...")){
    //   return true;
    //}
    if(confirm("相同学号提交后不能更改，是否继续提交！")){
        return true;
     }
    return false;
});


var u_agent=(navigator.userAgent);
if(u_agent.indexOf("Safari")>-1||u_agent.indexOf("Firefox")>-1||window.opera){}
else if(u_agent.indexOf("MSIE")>0&&!window.innerWidth){
    //document.location.reload(true);
    window.open("http://202.118.67.200:2000/recruit");
    window.opener=null;
    window.open('','_self'); 
    window.close();
}
