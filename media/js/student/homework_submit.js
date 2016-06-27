






// $(document).on("click", "#test", function()
// {
// 	// alert("SSSS");
// 	// $("#test_checkbox").trigger("click");
// 	var check_box = document.getElementById("test_checkbox");
// 	check_box.checked ^= 1;
// 	// if(check_box.checked) check_box.checked= false;
// 	// else check_box.checked = true;
// 	// check_box.checked = check_box.checked ^ 1;

// })

$(document).on("click", ".saveHomework", function()
{    
    $('#homework_modal').modal("hide");
})

$(document).on("click", ".viewHomeworkContent", function()
{
	$("#homework_modal .modal-title").text("作业内容");
    $("#homework_modal [name='name']").val($(this).attr("homework-name"));
    $("#homework_modal [name='required']").val($(this).attr("homework-required"));
    $("#homework_modal [name='deadline']").val($(this).attr("homework-deadline"));


    var checkbox = document.getElementById("homework_is_final");
    if($(this).attr("homework-is_final") == "True")
        checkbox.checked = true
    else 
        checkbox.checked = false


})