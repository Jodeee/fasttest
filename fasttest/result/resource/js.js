$(document).ready(function(){
    var imgdivx = 0
    $('td.result_css_module_name').click(function(){
                var data_tag = $(this).attr('data-tag')
                var txt = $(this).text();
                if(txt == "Open") {
                    $(this).text("Close");
                    $("tr[module-data-tag*='"+data_tag+"']").show()
                } else {
                    $(this).text("Open");
                    $("tr[module-data-tag*='"+data_tag+"']").hide()
                    var _td = $("tr[module-data-tag*='"+data_tag+"']").children('td.result_css_module_td_view')
                    for (bottomtd in _td) {
                        var closetr = _td.eq(bottomtd).attr('data-tag')
                        if (typeof(closetr) != "undefined")
                            $(_td.eq(bottomtd)).text("Open")
                            $("tr[module-td-data-tag='" + closetr + "']").hide()
                            var imgview = $("tr[module-td-data-tag='" + closetr + "']").find('.img_errorp')
                            imgview.hide()
                    }
                }
            })

    $('td.result_css_module_td_view').click(function(){
                var data_tag = $("tr[module-td-data-tag*='"+$(this).attr('data-tag')+"']")
                var txt = $(this).text();
                if(txt == "Open") {
                    $(this).text("Close");
                    $(data_tag).show()
                } else {
                    $(this).text("Open");
                    $(data_tag).hide()
                    var imgview = $(data_tag).find('.img_errorp')
                    imgview.hide()
                }
     })


    $('pre.result_css_StepsdetailsPre').click(function(){
        var img = $(this).parent('.result_css_steps').next();
        if (img.is(":hidden")){
            img.show()
        }else {
            img.hide()
        }
    })
})