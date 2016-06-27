var uid=0;
function refreshMutilipSelect(){
  var build = function(select, tr) {
    select.multiselect();
    return false;
  }($('#id_course_to_class'));
  var build = function(select, tr) {
    select.multiselect();
    return false;
  }($('#id_class_week'));
  var build = function(select, tr) {
    select.multiselect();
    return false;
  }($('#id_class_time'));
}
$(document).ready(function() {
  refreshMutilipSelect();
});


$('#course_info_modal #save_course').click(function(){
  page = $(".course_paginator").find(".disabled").attr("value");
  Dajaxice.adminStaff.CourseInfo(Course_callback,{'filter_form':$("#course_filter_form").serialize(true),'form':$("#course_form").serialize(true),'uid':uid,'page':page})
})


$(document).on("click","table td",function(){
  uid=$(this).parent().find("button").attr("uid");
  if($(this).find("button").length >0){
    page = $(".course_paginator").find(".disabled").attr("value");
    if(confirm("确认删除此门课程吗？与该门课程相关数据同时删除。")) Dajaxice.adminStaff.DeleteCourse(Course_callback,{'filter_form':$("#course_filter_form").serialize(true),'uid':uid,'page':page});
  }else{
    Dajaxice.adminStaff.GetCourseForm(CourseForm_callback,{'uid':uid});
  }
})

function Course_callback(data){
  if(data.status=='1'){
    $("#course_section").html(data.table);
    $("#course_info_modal").modal('hide');
    $('#course_form_div').html(data.form);
    uid=0;
  }else if(data.status =='0'){
    $('#course_form_div').html(data.form);
  }else if(data.status=='2'){
    $("#course_section").html(data.table);
  }
  refreshMutilipSelect();
  if(data.message.length() !=0){
    alert(data.message);
  }
}

function CourseForm_callback(data){
  $('#course_form_div').html(data.form);
  refreshMutilipSelect();
  $("#course_info_modal").modal('show');
}
$(document).on("click",".course_paginator .item_page",function(){
      page = $(this).attr("arg");
      Dajaxice.adminStaff.CoursePagination(Course_callback,{'filter_form':$("#course_filter_form").serialize(true),'page':page});
})
$(".course_filter").change(function(){
      Dajaxice.adminStaff.CoursePagination(Course_callback,{'filter_form':$("#course_filter_form").serialize(true),'page':1});
});

$("#exportCourse").on("click",function(){
  Dajaxice.adminStaff.exportSearchCourse(export_search_course_callback,{'filter_form':$("#course_filter_form").serialize(true)});
})

function export_search_course_callback(data){
  location.href = data.path;
}

var options={
  url:"/adminStaff/importCourseData",
  clearForm:true,
  resetForm:true,
  error:function(data){
  },
  success:function(data){
    if(data.status=='0'){
      location.href = data.path;
    }else if(data.status=='1'){
      $("#course_section").html(data.table);
    }
    alert(data.message);
    $("#course_importdata_modal").modal('hide');
  },
  };
$('#course_importdata_form').submit(function(){
  $('#course_importdata_form').ajaxSubmit(options);
  return false;
})
