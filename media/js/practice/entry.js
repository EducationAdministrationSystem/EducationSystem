$(document).ready(function(){
	Dajaxice.practice.getApplys(getApplysCallBack, {"page": "1", })
});
function getApplysCallBack(data){
    $("#applys").html(data);
}


$(document).on("click", "div#paginator .item_page", function(){
	Dajaxice.practice.getApplys(getApplysCallBack, {"page": $(this).attr("arg"), })
});

$(document).on("click", "input#select_all", function(){
    var target = this.checked;
    $("input[type='checkbox']").each(function(){
        this.checked = target;
    });
});

$(document).on("click", "#entry_modal_btn", function(){
    var checked_cnt = 0;
    $("input[name='check_entry']").each(function(){
        if(this.checked) checked_cnt++;
    });
    $(".modal-title").html("学生录入（本批次选择了" + checked_cnt + "个)");
});

$(document).on("click", "#entry_btn", function(){
    var apply_list = []
    $("input[name='check_entry']").each(function(){
        if(this.checked) apply_list.push($(this).attr("args"));
    })
    var small_class_id = $("#id_small_classes").val();
    Dajaxice.practice.studentEntry(studentEntryCallBack, {"apply_list": apply_list, "small_class_id": small_class_id, });
});
function studentEntryCallBack(data){
    Dajaxice.practice.getApplys(getApplysCallBack, {"page": $("div#paginator .disabled").val(), })
}


$(document).on("click", "#export_btn", function(){
    Dajaxice.practice.exportEntryList(exportEntryListCallBack, {});
});
function exportEntryListCallBack(url){
    location.href = url;
}

$(document).on("click", "#backout_btn", function(){
	if(confirm("确定批量撤消吗？")){
		var backout_list = [];
		$("input[name='check_entry']").each(function(){
			if(this.checked) backout_list.push($(this).attr("args"));
		});
		Dajaxice.practice.backOutEntry(studentEntryCallBack, {"backout_list":backout_list});
	}
});
