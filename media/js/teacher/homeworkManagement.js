$("#id_deadline").datetimepicker({

    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:0
});





var cid ="", hid = ""; /// for .addHomework .saveHomework
$(document).on("click", ".addHomework", function()
{
    $('#homework_modal .alert-danger').hide();
    $('#homework_modal .modal-title').text("增加作业");
    $('#homework_modal .form-control').css("background", "white");
    $("#homework_modal .form-control").val("");

    $("#homework_modal [name='is_final']").attr("checked", false);


    cid = $(this).parents("[cid]").attr('cid');
    hid = ""
})


$(document).on("click", ".modifyHomework", function()
{
    cid = $(this).parents("[cid]").attr('cid');
    hid = $(this).attr('hid');
    var cnt = $(this).parents("tr");    

    $('#homework_modal .alert-danger').hide();
    $('#homework_modal .modal-title').text("修改作业");
    $('#homework_modal .form-control').css("background", "white");
    $("#homework_modal [name='name']").val($(cnt).find("td:eq(1)").text());
    $("#homework_modal [name='required']").val($(cnt).find("td:eq(2) button").attr("homework-required"));
    $("#homework_modal [name='deadline']").val($(cnt).find("td:eq(3)").text());

    var checkbox = document.getElementById("homework_is_final");
    if($(cnt).find("td:eq(4)").attr("is_final") == "True")
        checkbox.checked = true
    else 
        checkbox.checked = false
    
})

$(document).on("click", ".saveHomework", function()
{    
    var form = $('#homework_modal form').serialize();
    Dajaxice.teacher.saveHomework(saveHomeworkCallback, 
        {
            'form':form,
            'cid': cid,
            'hid': hid,
        });
})

function saveHomeworkCallback(data)
{
    $('#homework_modal .alert').hide();
    $('#homework_modal .form-control').css("background", "white");
    if(data.status == 0)
    {
        $('#homework_modal').modal("hide");
        $("[cid="+cid+"] div" ).html(data.homework_table);
    }
    else if(data.status == 1)
    {
        $('#homework_modal .alert').html("<h3> "+"您有字段未填写或填写错误"+"</h3>");
        $('#homework_modal .alert').show(1000);
        var error_list = data.error_list.split(",");
        error_list.pop();
        for(var i = 0; i < error_list.length; ++ i)
        {
            $("#homework_modal [name="+error_list[i]+ "]").css("background", "red");
        }        
    }
}

$(document).on("click", ".viewHomeworkRequired", function()
{
    // alert($(this).attr("homework-required"));
    $("#required_modal .modal-body").html($(this).attr("homework-required"));
})

$(document).on("click", ".viewHomeworkSubmit", function()
{
    $("#homework_page").hide();
    $("#homework_submit_page").show();
    Dajaxice.teacher.getHomeworkSubmitTable(getHomeworkSubmitTableCallback, 
        {
            'hid': $(this).attr("hid"),
        });
    

})

function getHomeworkSubmitTableCallback(data)
{
    $("#homework_submit_page div").html(data.homework_submit_table);
}
var hsid, cnt_score_button; // for .modifyScore .saveScore
$(document).on("click", ".modifyScore", function()
{
    // $("#score_error").hide();
    $("#score_modal .alert").hide();
    var score = $(this).attr("score");
    cnt_score_button = this;
    hsid = $(this).attr("hsid");
    if(score)
    {
        $("#score_modal input[name=score]").val(score);
    }
    else 
    {
        $("#score_modal input[name=score]").val("");
    }

})


$(document).on("click", ".saveScore", function() 
{
    Dajaxice.teacher.saveScore(saveScoreCallback, 
    {
        'form':$("#score_modal form").serialize(),
        'hsid': hsid,
    })

})

function saveScoreCallback(data)
{
    if(data.status == 0)
    {
        $("#score_modal .alert").hide();
        $('#score_modal').modal("hide");

        $(cnt_score_button).parents("tr").children("td:eq(3)").text(data.score)
    }
    else if(data.status == 1)
    {
        $("#score_modal .alert").html("<h3>输入了空串</h3>")
        $("#score_modal .alert").show(500);        
    }
    else if(data.status == 2)
    {
        $("#score_modal .alert").html("<h3>输入串过长</h3>")
        $("#score_modal .alert").show(500);
    }
    else if(data.status == 3)
    {
        $("#score_modal .alert").html("<h3>输入的不是合法数字</h3>")
        $("#score_modal .alert").show(500);

    }

}



$(document).on("click", "#homework_submit_page button:first", function()
{
    $("#homework_submit_page").hide();
    $("#homework_page").show();
})