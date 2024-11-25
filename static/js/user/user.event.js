var gSelection = null;

  // 스크롤 여부 (true of false)
  $.fn.hasScrollBar = function() {
    return (this.prop("scrollHeight") == 0 && this.prop("clientHeight") == 0) || (this.prop("scrollHeight") > this.prop("clientHeight"));
  };

var user_event = user_event || (function(){
	var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    console.dir(this.document.currentScript.src);
    return{
        init: function(){
            console.log('user_event init!!!!!!!!!!!!!!!');
            console.dir(this.document.currentScript.src);
        },
        init_keyboard : function(paramId, url){
            console.log('user_event nit_keyboard');
            window.addEventListener("keydown", (e) => {

                if(e.shiftKey && e.key === 'ArrowUp'){
                    var rowCnt = $(paramId).prop('rows').length;
                    for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                        if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx-1 > 0) {
                            $($(paramId).prop('rows')[rowIdx-1]).removeClass('before_searched');
                            $($(paramId).prop('rows')[rowIdx-1]).addClass('selected').siblings().removeClass('selected');
                            var details_json=$($(paramId).prop('rows')[rowIdx-1]).find('td:nth-child(5)').find('div').html();
                            var details_json2=$($(paramId).prop('rows')[rowIdx-1]).find('td:nth-child(4)').find('div').html();
                            if(checkUrl()) clickTableRow(details_json);
                            else clickTableRow2(details_json2);
                            $(paramId).prop('rows')[rowIdx-1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                            break;
                        }
                    }
                }
                else if (e.shiftKey && e.key === 'ArrowDown'){
                    var rowCnt = $(paramId).prop('rows').length;
                    for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                        if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx+1 < rowCnt) {
                            $($(paramId).prop('rows')[rowIdx]).removeClass('before_searched');
                            $($(paramId).prop('rows')[rowIdx+1]).addClass('selected').siblings().removeClass('selected');
                            var details_json=$($(paramId).prop('rows')[rowIdx+1]).find('td:nth-child(5)').find('div').html();
                            var details_json2=$($(paramId).prop('rows')[rowIdx+1]).find('td:nth-child(4)').find('div').html();
                            if(checkUrl()) clickTableRow(details_json);
                            else clickTableRow2(details_json2);
                            $(paramId).prop('rows')[rowIdx+1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                            break;
                        }
                    }
                }
                else if(e.key === 'ArrowUp'){
                    try {
//                        var selObj = window.getSelection();
//                        gSelection = selObj
//                        var seleParenElement = selObj.baseNode.parentElement
//                        for(;seleParenElement.nodeName != 'TD' ; seleParenElement=seleParenElement.parenElement);
                        if($(window.getSelection()).hasScrollBar() == true) return;
                        // 포커스가 있어야 키보드 내려올때 모든화면이 내려오지않음
                        $("#focusInput").focus();
                        var rowCnt = $(paramId).prop('rows').length;
                        for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                            if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx-1 > 0) {
                                $($(paramId).prop('rows')[rowIdx-1]).removeClass('before_searched');
                                $($(paramId).prop('rows')[rowIdx-1]).addClass('selected').siblings().removeClass('selected');
                                var details_json=$($(paramId).prop('rows')[rowIdx-1]).find('td:nth-child(5)').find('div').html();
                                var details_json2=$($(paramId).prop('rows')[rowIdx-1]).find('td:nth-child(4)').find('div').html();
                                if(checkUrl()) clickTableRow(details_json);
                                else clickTableRow2(details_json2);

                                $(paramId).prop('rows')[rowIdx-1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                                break;
                            }
                        }
                    } catch (e){
                    }
                }
                else if(e.key === 'ArrowDown'){
                    try {
//                        var selObj = window.getSelection();
//                        gSelection = selObj
//                        var seleParenElement = selObj.baseNode.parentElement
//                        for(;seleParenElement.nodeName != 'TD' ; seleParenElement=seleParenElement.parenElement);
                        if($(window.getSelection()).hasScrollBar() == true) return;
                        // 포커스가 있어야 키보드 내려올때 모든화면이 내려오지않음
                        $("#focusInput").focus();
                        var rowCnt = $(paramId).prop('rows').length;
                        for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                            if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx+1 < rowCnt) {
                                $($(paramId).prop('rows')[rowIdx]).removeClass('before_searched');
                                $($(paramId).prop('rows')[rowIdx+1]).addClass('selected').siblings().removeClass('selected');
                                var details_json=$($(paramId).prop('rows')[rowIdx+1]).find('td:nth-child(5)').find('div').html();
                                var details_json2=$($(paramId).prop('rows')[rowIdx+1]).find('td:nth-child(4)').find('div').html();
                                if(checkUrl()) clickTableRow(details_json);
                                else clickTableRow2(details_json2);

                                $(paramId).prop('rows')[rowIdx+1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                                break;
                            }
                        }
                    } catch(e){
                    }
                }
            });
        },
        init_mouse : function(paramId){
            console.log('user_event init_mouse');
            $(window).bind('wheel', function(event){
                if (event.shiftKey && event.originalEvent.wheelDelta) {
                    if (event.originalEvent.wheelDelta > 0 || event.originalEvent.detail < 0) {
                        // scroll up
                        var rowCnt = $(paramId).prop('rows').length;
                        for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                            if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx-1 > 0) {
                                $($(paramId).prop('rows')[rowIdx-1]).removeClass('before_searched');
                                $($(paramId).prop('rows')[rowIdx-1]).addClass('selected').siblings().removeClass('selected');
                                var details_json =$($(paramId).prop('rows')[rowIdx-1]).find('td:nth-child(5)').find('div').html();
                                var details_json2 =$($(paramId).prop('rows')[rowIdx-1]).find('td:nth-child(4)').find('div').html();
                                if(checkUrl()) clickTableRow(details_json);
                                else clickTableRow2(details_json2);
                                $(paramId).prop('rows')[rowIdx-1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                                break;
                            }
                        }
                    }
                    else {
                        // scroll down
                        var rowCnt = $(paramId).prop('rows').length;
                        for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                            if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx+1 < rowCnt) {
                                $($(paramId).prop('rows')[rowIdx]).removeClass('before_searched');
                                $($(paramId).prop('rows')[rowIdx+1]).addClass('selected').siblings().removeClass('selected');
                                var details_json = $($(paramId).prop('rows')[rowIdx+1]).find('td:nth-child(5)').find('div').html();
                                var details_json2 = $($(paramId).prop('rows')[rowIdx+1]).find('td:nth-child(4)').find('div').html();
                                if(checkUrl()) clickTableRow(details_json);
                                else clickTableRow2(details_json2);

                                $(paramId).prop('rows')[rowIdx+1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                                break;
                            }
                        }
                    }
                }
            });
        },
        init_refresh : function(paramId) {
            console.log('user_event init_refresh');
            window.addEventListener("keydown", (e) => {
                if (e.key === 'Enter'){
                    console.log('enter')
                    $(paramId).click();
                } else if (e.shiftKey && e.key === 'Enter'){
                    console.log('enter')
                    $(paramId).click();
                }
            });

            // shift + mouse left click
            document.onmousedown = function(e) {
                if (e.shiftKey && e.which == 1) {
                    $(paramId).click();
                }
            };
        },
        init_key_up_down : function(paramId){
            console.log('user_event init_key_up_down');
            window.addEventListener("keydown", (e) => {

                if(e.shiftKey && e.key === 'ArrowUp'){
                    var rowCnt = $(paramId).prop('rows').length;
                    for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                        if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx-1 > 0) {
                            $($(paramId).prop('rows')[rowIdx-1]).removeClass('before_searched');
                            $($(paramId).prop('rows')[rowIdx-1]).addClass('selected').siblings().removeClass('selected');
                            // var details_json=$($(paramId).prop('rows')[rowIdx-1]).find('td:nth-child(5)').find('div').html();
                            // clickTableRow(details_json);
                            $(paramId).prop('rows')[rowIdx-1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                            break;
                        }
                    }
                }
                else if (e.shiftKey && e.key === 'ArrowDown'){
                    var rowCnt = $(paramId).prop('rows').length;
                    for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                        if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx+1 < rowCnt) {
                            $($(paramId).prop('rows')[rowIdx]).removeClass('before_searched');
                            $($(paramId).prop('rows')[rowIdx+1]).addClass('selected').siblings().removeClass('selected');
                            // var details_json=$($(paramId).prop('rows')[rowIdx+1]).find('td:nth-child(5)').find('div').html();
                            // clickTableRow(details_json);
                            $(paramId).prop('rows')[rowIdx+1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                            break;
                        }
                    }
                }
                else if(e.key === 'ArrowUp'){
                    try {
                        if($(window.getSelection()).hasScrollBar() == true) return;
                        $("#viewOSText").focus();
                        var rowCnt = $(paramId).prop('rows').length;
                        for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                            if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx-1 > 0) {
                                $($(paramId).prop('rows')[rowIdx-1]).removeClass('before_searched');
                                $($(paramId).prop('rows')[rowIdx-1]).addClass('selected').siblings().removeClass('selected');
                                var details_json=$($(paramId).prop('rows')[rowIdx-1]).find('td:nth-child(5)').find('div').html();
                                var details_json2=$($(paramId).prop('rows')[rowIdx-1]).find('td:nth-child(4)').find('div').html();
                                 if(checkUrl()) clickTableRow(details_json);
                                else clickTableRow2(details_json2);

                                $(paramId).prop('rows')[rowIdx-1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                                break;
                            }
                        }
                    } catch (e){
                    }
                }
                else if(e.key === 'ArrowDown'){
                    try {
                        if($(window.getSelection()).hasScrollBar() == true) return;
                        $("#viewOSText").focus();
                        var rowCnt = $(paramId).prop('rows').length;
                        for (var rowIdx = 0; rowIdx < rowCnt; rowIdx++){
                            if($(paramId).prop('rows')[rowIdx].classList.length > 0 && rowIdx+1 < rowCnt) {
                                $($(paramId).prop('rows')[rowIdx]).removeClass('before_searched');
                                $($(paramId).prop('rows')[rowIdx+1]).addClass('selected').siblings().removeClass('selected');
                                var details_json=$($(paramId).prop('rows')[rowIdx+1]).find('td:nth-child(5)').find('div').html();
                                var details_json2=$($(paramId).prop('rows')[rowIdx+1]).find('td:nth-child(4)').find('div').html();
                                if(checkUrl()) clickTableRow(details_json);
                                else clickTableRow2(details_json2);

                                $(paramId).prop('rows')[rowIdx+1].scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"})
                                break;
                            }
                        }
                    } catch(e){
                    }
                }
            });
        },
	}
})();

