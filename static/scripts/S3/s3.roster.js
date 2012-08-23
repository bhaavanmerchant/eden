    var current_cell={"r":0,
                      "c":0};
jQuery(document).ready(function(){
    $("#newrole").hide();
    $("#r_varea").hide();
    $(".rems").hide();
    $(".addpf").hide();
    $(".rempf").show();
    $("#addrow").click(function()
        {
        $("#newrole").toggle();
        $("#addrow").hide();
        });
    $("#new_job_title").change(function()
        {
        $("#roster_info_form").submit();
        });
    $("#event").change(function()
        {
        $("#table_info_form").submit();
        });
    $("#project_selector").change(function()
        {
        $("#table_info_form").submit();
        });
    $("#timeframe").change(function()
        {
        $("#table_info_form").submit();
        });
    $("#timeslot").change(function()
        {
        $("#table_info_form").submit();
        });
    $("#vn").on("keypress","#volunteer_quick_search",function(event){
        $(".volunteer_names").each(function(){
            if($("#volunteer_quick_search").val()=="")
            {
            $(this).show();
            }
            else
            {
                if ($(this).html().toLowerCase().search($("#volunteer_quick_search").val().toLowerCase()) == -1)
                {
                $(this).hide();
                }
                else
                {
                $(this).show();
                }
            }
        });
    });

    $(".adds").click(function()
        {
        var cell=$(this).parent();
        cell.addClass("sloted");
        cell.data("sloted",1);
        cell.children(".scelln").html('<a class="addv">Assign</a> {{=IMG(_src="/eden/static/img/star.png",_alt="star",_class="star")}}');
        cell.children(".adds").hide();
        cell.children(".rems").show();
        $("#r_varea").hide();
        $(".aside").show();
        });
    $("#r_table").on("click",".addv",function(event)
       {
        $("#r_varea").show();
        
        $(".aside").hide();
        var cell=$(this).parent().parent();
        current_cell.r=cell.data("row");
        current_cell.c=cell.data("col");
        $.ajax(
            {
            type: "POST",
            url: "{{=URL(c='roster', f='people', args=[table_id, instance_id])}}",
            data: { row: current_cell.r }
            }).done(function( msg ) 
                {
                $("#vn").html(msg);
                });

        });
    $(".remrole").click(function()
        {
        var cell=$(this).parent();
        var url="{{=URL(c='roster', f='del_role', args=[table_id, instance_id])}}"+"/"+cell.data('pos');
        $(location).attr("href",url);
        });
    $("#vn").on("click",".volunteer_names",function(event)
        {
        var vname=$(this).html();
        var vid=$(this).attr("id");
        var duplicate=0;
        $(".vcell").each(function()
            {
            if($(this).data("col")==current_cell.c && $(this).data("vid")==vid)
                {
                duplicate=1;
                };
            });
        if(duplicate==1)
            {
                alert("The same person cannot do more than one role in a given slot.");
            }
        else
            {
            $(".vcell").each(function()
                {
                if($(this).data("row")==current_cell.r && $(this).data("col")==current_cell.c)
                    {
                    var cell_c=vname;
                    $(this).children(".vcelln").html(cell_c);
                    $(this).children(".scelln").html("<a class='remv'>Release</a>");
                    $(this).data("vid",vid);
                    $(this).addClass("allotted");
                    $(this).removeClass("sloted");
                    }; 
                });
           };
        });
    $("#r_table").on("click",".remv",function(event)
        {
        var cell=$(this).parent().parent();
        cell.children(".vcelln").html("");
        cell.removeClass("allotted");
        cell.addClass("sloted");
        cell.data("vid",0);
        $(this).parent().html('<a class="addv">Assign</a> {{=IMG(_src="/eden/static/img/star.png",_alt="star",_class="star")}}');
        });
    $(".rems").click(function()
        {
        $(this).parent().children(".scelln").html("");
        $(this).parent().children(".vcelln").html("");
        $(this).parent().children(".rems").hide();
        $(this).parent().children(".adds").show();
        $(this).parent().data("vid",0);
        $(this).parent().data("sloted",0);
        $(this).parent().removeClass("sloted");
        $(this).parent().removeClass("allotted");
        $(this).parent().removeClass("essential");
        });
    $("#r_table").on("click",".star",function(event)
        {
        $(this).parent().parent().addClass("essential");
        $(this).parent().parent().data("sloted",2)
        });
    $("#cross").click(function()
        {
        $("#r_varea").hide();
        $(".aside").show();
        });
    $("#save").click(function()
    {
    var roster_array=new Array();
    var i=0;
    $(".allotted").each(function()
        {
        var v_json= {
                    "row":$(this).data("row"),
                    "col":$(this).data("col"),
                    "vid":$(this).data("vid"),
                    "slot_level":$(this).data("row")
                    };
        roster_array[i]=v_json;
        i=i+1;
        });
    $(".sloted").each(function()
        {
        var v_json= {
                    "row":$(this).data("row"),
                    "col":$(this).data("col"),
                    "vid":"",
                    "slot_level":$(this).data("sloted")
                    };
        roster_array[i]=v_json;
        i=i+1;
        });
    var roster_dets={"array":roster_array};
    $.ajax(
            {
            type: "POST",
            url: "{{=URL(c='roster', f='roster_submit', args=[table_id, instance_id])}}",
            data: roster_dets
            }).done(function( msg ) 
                {
                $("#flash_message").html(msg);
                });
    });
    
});
