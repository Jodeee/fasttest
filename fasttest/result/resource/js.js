$(document).ready(function(){
    var imgdivx = 0
    $('td.module_name').click(function(){
                var data_tag = $(this).attr('data-tag')
                var txt = $(this).text();
                if(txt == "Open") {
                    $(this).text("Close");
                    $('tr.'+data_tag).show()
                } else {
                    $(this).text("Open");
                    $('tr.'+data_tag).hide()
                    var _td = $('tr.'+data_tag).children('td.module_td_view')
                    for (bottomtd in _td) {
                        var closetr = _td.eq(bottomtd).attr('data-tag')
                        if (typeof(closetr) != "undefined")
                            $(_td.eq(bottomtd)).text("Open")
                            $('.' + closetr).hide()
                    }
                }
            })

    $('td.module_td_view').click(function(){
                var data_tag = 'tr.' + $(this).attr('data-tag')
                var txt = $(this).text();
                if(txt == "Open") {
                    $(this).text("Close");
                    $(data_tag).show()
                } else {
                    $(this).text("Open");
                    $(data_tag).hide()
                }
            })


    $('pre.StepsdetailsPre').click(function(){
        var img = $(this).parent('.steps').next();
        if (img.is(":hidden")){
            img.show()
        }else {
            img.hide()
        }
    })
})