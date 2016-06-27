$("#commit_button").click(function(){
    var student_name=$("#id_student_name").val();
    var student_id=$("#id_student_id").val();
    var sex=$("#id_sex").val();
    var tel_num=$("#id_tel_num").val();
    Dajaxice.common.StudentRegistration(registrationcallback,{
        "student_name":student_name,
        "student_id":student_id,
        "sex":sex,
        "tel_num":tel_num
    });
});
function registrationcallback(data){
    if(data.status===0){
        alert(" 注册成功！密码为学号。");
        location.href="/";
    }
    else{
        alert(data.message);
    }
}
